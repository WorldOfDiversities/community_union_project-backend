from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.parsers import MultiPartParser, FormParser


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
        # Only allow admin roles to view pending approvals
        if request.user.role not in ['super_admin', 'executive', 'secretary']:
            return Response(
                {'detail': 'You do not have permission to view pending approvals.'},
                status=status.HTTP_403_FORBIDDEN
            )

        User = get_user_model()
        # Get users who submitted onboarding but are not yet approved
        pending = User.objects.filter(
            onboarding_submitted=True,
            is_approved=False
        ).order_by('-updated_at')

        serializer = UserSerializer(pending, many=True)
        return Response({
            'count': pending.count(),
            'pending_approvals': serializer.data,
        })


class PendingApprovalsSummaryView(APIView):
    """Lightweight summary of pending approvals for dashboard widgets."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        User = get_user_model()
        pending_qs = User.objects.filter(onboarding_submitted=True, is_approved=False).order_by('-updated_at')
        count = pending_qs.count()
        sample = pending_qs[:3]
        # Return minimal data for widget consumption
        data = [
            {
                'id': u.id,
                'full_name': u.get_full_name() or u.email,
                'email': u.email,
                'avatar_url': getattr(u, 'avatar_url', None),
                'updated_at': u.updated_at,
            }
            for u in sample
        ]
        return Response({'count': count, 'sample': data})


class ApproveUserView(APIView):
    """Approve a pending user"""
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        """Approve a specific user"""
        # Only allow admin roles
        if request.user.role not in ['super_admin', 'executive', 'secretary']:
            return Response(
                {'detail': 'You do not have permission to approve users.'},
                status=status.HTTP_403_FORBIDDEN
            )

        User = get_user_model()
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'detail': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Approve the user
        user.is_approved = True
        user.save()

        return Response({
            'message': f'User {user.email} has been approved.',
            'user': UserSerializer(user).data,
        }, status=status.HTTP_200_OK)


class RejectUserView(APIView):
    """Reject a pending user"""
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        """Reject/deactivate a specific pending user"""
        # Only allow admin roles
        if request.user.role not in ['super_admin', 'executive', 'secretary']:
            return Response(
                {'detail': 'You do not have permission to reject users.'},
                status=status.HTTP_403_FORBIDDEN
            )

        User = get_user_model()
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'detail': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Reject by deactivating and resetting onboarding flag
        user.is_active = False
        user.onboarding_submitted = False
        user.is_approved = False
        user.save()

        return Response({
            'message': f'User {user.email} has been rejected.',
            'user': UserSerializer(user).data,
        }, status=status.HTTP_200_OK)

