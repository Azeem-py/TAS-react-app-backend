from rest_framework import serializers, validators
from .models import *



valid = {"required": True,}

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchInfo
        fields = '__all__'
        # valid = {
        #     "required": True
        # }

        extra_kwargs = {
            "locationAddress": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(BranchInfo.objects.all(), "Location already exits")
                ]
            },

            'branchName': {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(BranchInfo.objects.all(), "Location already exits")
                ]
            },


        }

        def create(self, validated_data):
            # locationAddress = validated_data.get('locationAddress')
            # locationName = validated_data.get('branchName')


            newBranch = BranchInfo.objects.create(**validated_data)

            return newBranch



class BranchAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = BranchAdminInfo

        fields = '__all__'

        extra_kwargs = {
            'firstName': valid,
            'lastName': valid,
            'email': {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(BranchAdminInfo.objects.all(), "email has been used by another admin"),
                ]
                },
            'phoneNumber':{
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(BranchAdminInfo.objects.all(), "Number has been used by another admin"),
                ]
                },
            'address': valid,
            
        }

  

    def create(self, validated_data):
        newAdmin = BranchAdminInfo.objects.create(**validated_data)

        return newAdmin



