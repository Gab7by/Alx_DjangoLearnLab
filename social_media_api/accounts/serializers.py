from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import serializers

User = get_user_model()

class RegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password", "bio", "profile_picture"]
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data.get("username"),
            email = validated_data["email"],
            password = validated_data["password"],
            bio = validated_data.get("bio", ""),
            profile_picture = validated_data.get("profile_picture"),
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(blank = False, null=False)
    password = serializers.CharField(write_only = True)
    
    def validate(self, data):
        user = authenticate(
            email=data["email"],
            password=data["password"]
        )
        
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        
        token, _ = Token.objects.get_or_create(user=user)
        
        return {
            "user": user,
            "token": token.key
        }