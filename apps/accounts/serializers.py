from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model - excludes sensitive fields"""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'role', 'phone', 'is_active', 'created_at', 'avatar_url', 'is_superuser', 'is_staff']
        read_only_fields = ['id', 'created_at']
    
    def get_full_name(self, obj):
        """Get full name from first_name and last_name"""
        return obj.get_full_name() or obj.email


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    full_name = serializers.CharField(required=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=False)
    
    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'password2', 'role']
    
    def validate(self, data):
        """Validate password fields match"""
        if data['password'] != data['password2']:
            raise serializers.ValidationError({
                'password2': 'Passwords do not match.'
            })
        return data
    
    def validate_email(self, value):
        """Check if email already exists"""
        normalized_email = value.strip().lower()
        if User.objects.filter(email__iexact=normalized_email).exists():
            raise serializers.ValidationError('Email already registered.')
        return normalized_email
    
    def create(self, validated_data):
        """Create user with validated data"""
        validated_data.pop('password2')
        password = validated_data.pop('password')
        full_name = validated_data.pop('full_name', '')
        role = validated_data.pop('role', None)
        email = validated_data.pop('email', '').strip().lower()
        
        # Split full_name into first_name and last_name
        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # If role is supplied, it will be set here; view may override based on requester's permissions
        user_kwargs = {
            'username': email,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
        }
        if role:
            user_kwargs['role'] = role

        user = User.objects.create(**user_kwargs)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        """Authenticate user with email and password"""
        email = data.get('email', '').strip().lower()
        password = data.get('password')
        
        if not email or not password:
            raise serializers.ValidationError('Email and password are required.')
        
        try:
            user = User.objects.get(email__iexact=email)
            if not user.check_password(password):
                raise serializers.ValidationError('Invalid email or password.')
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid email or password.')
        
        if not user.is_active:
            raise serializers.ValidationError('User account is inactive.')
        
        data['user'] = user
        return data

