from rest_framework import serializers, validators
from .models import CustomUser, OTPModel



valid = {"required": True,}

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser

        fields = '__all__'

        extra_kwargs = {
            'email': {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(CustomUser.objects.all(), "email has been used by another admin"),
                ]
                },
            'password': valid,
        }
    
    def create(self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username')
        password = validated_data.get('password')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')

        user = CustomUser.objects.create(
            email=email, username=username, first_name=first_name, last_name=last_name
        )
        user.isBranchAdmin = True
        user.set_password(raw_password=password)
        user.save()
        return user



class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPModel

        fields = '__all__'
        extra_kwargs = {
            'email': {
                "required": True,
                "allow_blank": False,
                },
        }

        def create(self, validated_data):
            user_otp = OTPModel.objects.create(
                **validated_data
            )         
            user_otp.save()
            return user_otp
        
        
            
        

        
    
