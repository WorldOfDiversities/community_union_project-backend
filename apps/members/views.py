from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from apps.accounts.models import User
from apps.media_utils import resolve_media_url, storage_object_name_from_url

from .serializers import MemberDetailSerializer, MemberSerializer


class MemberListView(generics.ListCreateAPIView):
	"""List active members for dashboard consumption.

	Returns active users ordered by newest first. Uses pagination if configured
	in the project settings (DRF pagination).
	"""
	permission_classes = [permissions.IsAuthenticated]
	parser_classes = [MultiPartParser, FormParser]
	serializer_class = MemberSerializer

	def get_queryset(self):
		return User.objects.filter(is_active=True).order_by("-created_at")

	def create(self, request, *args, **kwargs):
		# Expecting multipart/form-data from admin UI or user onboarding. Create a User or update self.
		data = request.data
		email = (data.get('email') or '').strip().lower()
		first_name = data.get('first_name') or data.get('firstName') or ''
		last_name = data.get('last_name') or data.get('lastName') or ''
		phone = data.get('phone') or ''
		role = data.get('role') or 'member'

		if not email:
			return Response({'detail': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

		# If the requester is an authenticated user and the email matches theirs (onboarding self-update),
		# update the existing user instead of creating a new one.
		requester = request.user if hasattr(request, 'user') else None
		is_self_update = requester and getattr(requester, 'is_authenticated', False) and requester.email.lower() == email.lower()

		if is_self_update:
			# Self-update path: user completing their onboarding form
			user = requester
			user.first_name = first_name or user.first_name
			user.last_name = last_name or user.last_name
			user.phone = phone or user.phone
			# Mark that user has submitted onboarding; they remain unapproved until admin approves
			user.onboarding_submitted = True
			# preserve role unless explicitly set by an admin
			if request.user.role in ['super_admin', 'executive', 'secretary'] and role:
				user.role = role
		else:
			# New user creation path: admin creating a member
			if User.objects.filter(email__iexact=email).exists():
				return Response({'detail': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

			user_kwargs = {
				'username': email,
				'email': email,
				'first_name': first_name,
				'last_name': last_name,
				'phone': phone,
				'role': role,
			}

			user = User.objects.create(**user_kwargs)
			# set unusable password for admin-created accounts (they can reset later)
			user.set_unusable_password()

		# handle avatar file
		avatar_file = None
		if hasattr(request, 'FILES'):
			avatar_file = request.FILES.get('avatar')

		if avatar_file:
			try:
				from django.core.files.storage import default_storage
				from django.conf import settings
				import os
				import urllib.parse

				filename = f"avatars/{email}-{avatar_file.name}"
				previous_avatar = getattr(user, 'avatar_url', None)
				saved_path = default_storage.save(filename, avatar_file)
				try:
					avatar_url = default_storage.url(saved_path)
				except Exception:
					avatar_url = os.path.join(getattr(settings, 'MEDIA_URL', '/media/'), saved_path)
				# Some storage backends may return URL-encoded paths; store a decoded URL
				try:
					avatar_url = urllib.parse.unquote(avatar_url)
				except Exception:
					pass
				resolved_avatar_url = resolve_media_url(
					raw_url=avatar_url,
					storage_name=saved_path,
					endpoint_url=getattr(settings, 'AWS_S3_ENDPOINT_URL', None),
					bucket_name=getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None),
					storage=default_storage,
				)
				if resolved_avatar_url:
					user.avatar_url = resolved_avatar_url
					old_name = storage_object_name_from_url(previous_avatar)
					if old_name and old_name != saved_path:
						try:
							default_storage.delete(old_name)
						except Exception:
							pass
			except Exception:
				# ignore storage errors; save without avatar
				pass

		user.save()
		serializer = self.get_serializer(user)
		return Response(serializer.data, status=status.HTTP_201_CREATED)


class MemberDetailView(generics.RetrieveAPIView):
	"""Retrieve a single member's details.

	Returns full member information including profile, contact, and status details.
	"""
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = MemberDetailSerializer
	queryset = User.objects.all().select_related("standing").prefetch_related(
		"dues_payments",
		"assignments",
		"certifications",
		"activity_attendance__activity",
	)
	lookup_field = 'id'
