from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model


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


