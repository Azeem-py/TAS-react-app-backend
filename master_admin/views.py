from rest_framework.response import Response
from rest_framework import viewsets, views, status, permissions
from rest_framework.decorators import permission_classes, action
from auth_api.custom_permissions import *
from .serializers import *
from auth_api.serializers import UserSerializer
from auth_api.models import *
from django.contrib.auth import get_user_model
from django.http import QueryDict
from django.shortcuts import get_object_or_404


# Create your views here.


# this viewset creates and can get list of all branch admins create and is only accessible by branch admins.
class BranchAdminView(viewsets.ViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    def create(self, request):
        data = request.data.copy()
        try:
            password, confirmPassword, email, first_name, last_name = [
                data.pop("password"),
                data.pop("confirmPassword"),
                data.get("email"),
                data.get("firstName"),
                data.get("lastName"),
            ]
        except Exception as e:
            return Response({"status": "invalid login details"})

        if password == confirmPassword:
            serializer = BranchAdminSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            userData = {
                "username": email,
                "email": email,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
            }
            query_dict = QueryDict("", mutable=True)
            query_dict.update(userData)
            auth_serializer = UserSerializer(data=query_dict)
            auth_serializer.is_valid(raise_exception=True)
            auth_serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        queryset = BranchAdminInfo.objects.all()
        serializer = BranchAdminSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = BranchAdminInfo.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = BranchAdminSerializer(user)
        return Response(serializer.data)

    def partial_update(self, request, email=None):
        # user_email = request.data.get('email')
        user_otp = get_object_or_404(OTPModel, email=email)
        print(user_otp)
        try:
            if user_otp.otp == request.data.get("otp"):
                User = get_user_model()
                user = get_object_or_404(User, email=email)
                user.isVerified = True
                user.save()
                return Response(data={"status": "user is verified"})
            else:
                return Response(
                    {"otp error": "opt does not match"},
                )
        except Exception as e:
            return Response(data={"error": e})

    def validate_if_branch(self, request, email=None):
        queryset = BranchAdminInfo.objects.all()
        branchAdmin = get_object_or_404(queryset, email=email)
        serializer = BranchAdminSerializer(branchAdmin)
        branchAdminID = serializer.data["id"]
        print("branch admin id", branchAdminID)

        queryset = BranchInfo.objects.all()
        branch = get_object_or_404(queryset, branchAdmin=branchAdminID)
        serializer = BranchSerializer(branch)
        print(serializer.data)
        return Response(serializer.data)


# this viewset can create new branch and also get list of all branches.
class BranchView(viewsets.ViewSet):
    # permission_classes = (permissions.IsAuthenticated,)

    @permission_classes([permissions.IsAdminUser])
    def create(self, request):
        data = dict(request.data)
        print(data)
        BranchAdminEmail = data["email"]
        del data["email"]
        try:
            checkEmail = BranchAdminInfo.objects.get(email=BranchAdminEmail)
        except Exception as e:
            return Response({"error": "Admin email error"})
        data["branchAdmin"] = checkEmail.id
        newData = {key: value for (key, value) in data.items()}
        qdict = QueryDict("", mutable=True)
        qdict.update(newData)
        serializer = BranchSerializer(data=qdict)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        queryset = BranchInfo.objects.all()
        serializer = BranchSerializer(queryset, many=True)
        return Response(serializer.data)

    @permission_classes(
        [
            isBranchAdmin,
        ]
    )
    @action(
        detail=True,
        methods=[
            "get",
        ],
    )
    def getInfo(self, request, pk=None):
        queryset = BranchInfo.objects.all()
        user = get_object_or_404(queryset, branchAdmin=pk)
        serializer = BranchSerializer(user)
        print(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
