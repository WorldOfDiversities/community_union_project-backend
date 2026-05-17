from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.conf import settings
import os
import urllib.parse
from apps.media_utils import resolve_media_url, storage_object_name_from_url


class DashboardSummaryView(APIView):
    """Simple dashboard summary endpoint"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        User = get_user_model()
        total = User.objects.count()
        active = User.objects.filter(is_active=True).count()
        recent_qs = User.objects.order_by('-created_at')[:6]
        recent = UserSerializer(recent_qs, many=True).data
        return Response({
            'total_members': total,
            'active_members': active,
            'recent_members': recent,
            'current_user': UserSerializer(request.user).data,
        })



class RegisterView(APIView):
    """User registration endpoint"""
    # AllowAny for creating basic member accounts; Role assignment enforced server-side
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        """Create a new user account"""
        # Pass request in context so serializer or view logic can inspect requester
        serializer = RegisterSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            # If the request includes a role, only allow assignment if the requester is permitted
            requested_role = serializer.validated_data.get('role')
            user = serializer.save()
            if requested_role:
                requester = request.user
                if not (requester and getattr(requester, 'is_authenticated', False)):
                    # Unauthenticated registrations cannot set roles; default to 'member'
                    user.role = 'member'
                    user.save()
                else:
                    # Only allow role assignment when requester is super_admin/executive/secretary
                    if requester.role in ['super_admin', 'executive', 'secretary']:
                        user.role = requested_role
                        user.save()
                    else:
                        user.role = 'member'
                        user.save()
            return Response(
                {
                    'message': 'User registered successfully.',
                    'user': UserSerializer(user).data,
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    """User login endpoint - returns JWT tokens"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Authenticate user and return JWT tokens"""
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response(
                {
                    'message': 'Login successful.',
                    'user': UserSerializer(user).data,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                },
                status=status.HTTP_200_OK
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class PendingApprovalsView(APIView):
    """List users pending approval (submitted onboarding but not approved)"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get all pending approval users"""
        # Approvals are temporarily disabled; return empty results
        return Response({'count': 0, 'pending_approvals': []})


class PendingApprovalsSummaryView(APIView):
    """Lightweight summary of pending approvals for dashboard widgets."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Approvals disabled: return empty summary
        return Response({'count': 0, 'sample': []})


class ApproveUserView(APIView):
    """Approve a pending user"""
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        """Approve a specific user"""
        # Approvals are disabled; return success but do not change state
        return Response({'message': 'Approvals are temporarily disabled.'}, status=status.HTTP_200_OK)


class RejectUserView(APIView):
    """Reject a pending user"""
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        """Reject/deactivate a specific pending user"""
        # Approvals are disabled; return success but do not change state
        return Response({'message': 'Approvals are temporarily disabled.'}, status=status.HTTP_200_OK)


class ProfileView(APIView):
    """Get or update current user profile"""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        """Get current user profile"""
        user = request.user
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    def put(self, request):
        """Update current user profile"""
        user = request.user
        
        # Update user fields
        if 'first_name' in request.data:
            user.first_name = request.data['first_name']
        if 'last_name' in request.data:
            user.last_name = request.data['last_name']
        if 'email' in request.data:
            user.email = request.data['email']
        
        # Update profile fields if they exist on the User model
        if 'date_of_birth' in request.data and hasattr(user, 'date_of_birth'):
            user.date_of_birth = request.data['date_of_birth']
        if 'occupation' in request.data and hasattr(user, 'occupation'):
            user.occupation = request.data['occupation']
        if 'gender' in request.data and hasattr(user, 'gender'):
            user.gender = request.data['gender']
        if 'phone' in request.data:
            user.phone = request.data['phone']
        if 'address' in request.data and hasattr(user, 'address'):
            user.address = request.data['address']
        
        # Handle avatar upload
        if 'avatar' in request.FILES:
            avatar_file = request.FILES['avatar']
            try:
                filename = f"avatars/{user.email}-{avatar_file.name}"
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
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

