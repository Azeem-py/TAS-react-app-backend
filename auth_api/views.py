from django.contrib.auth import login
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, views, status, permissions
from rest_framework.response import Response
from .serializers import OTPSerializer, UserSerializer
from .models import OTPModel, CustomUser
from master_admin.models import *
from branch_admin.models import *

from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from django.http import QueryDict

from .custom_permissions import *
import pyotp
from .send_otp import send_otp_email


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class UserInfoView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def getInfo(self, request, email=None):
        queryset = CustomUser.objects.all()
        user = get_object_or_404(queryset, username=email)
        serializer = UserSerializer(user)
        new_data = serializer.data
        new_data.pop("password")
        new_data.pop("last_login")
        name = ""
        if new_data["isBranchAdmin"]:
            name = list(
                BranchAdminInfo.objects.filter(email=email).values(
                    "firstName", "lastName"
                )
            )[0]
            print(name)
        elif new_data["isParent"]:
            name = list(
                ParentInfo.objects.filter(email=email).values("firstName", "lastName")
            )[0]
        elif new_data["isTutor"]:
            name = list(
                EmployeeInfo.objects.filter(email=email).values("firstName", "lastName")
            )[0]
        elif new_data["isStudent"]:
            name = list(
                StudentInfo.objects.filter(email=email).values("firstName", "lastName")
            )[0]

        new_data["first_name"], new_data["last_name"] = (
            name["firstName"],
            name["lastName"],
        )

        print(new_data)
        return Response(new_data)


class CheckAuth(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def isValid(self, request):
        return Response(data={"auth": True}, status=status.HTTP_200_OK)


class OTPView(viewsets.ViewSet):
    def create(self, request):
        # generating otp
        secret_key = pyotp.random_base32()
        totp = pyotp.TOTP(secret_key, interval=3600)
        otp = totp.now()

        # making query dict of otp and email
        email = request.data["email"]
        otp_data = QueryDict("", mutable=True)
        otp_data.update({"email": email, "otp": otp})

        try:
            user_otp_obj = OTPModel.objects.get(email=email)
            # print('in if')
            user_otp_obj.otp = otp
            user_otp_obj.save()
            send_otp_email(to_email=email, otp=otp)
            return Response(data={"otp": otp, "email": email})
        except Exception as e:
            serializer = OTPSerializer(data=otp_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            send_otp_email(to_email=email, otp=otp)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        # if user_otp_obj:
        #     print('in if')
        #     user_otp_obj.otp = otp
        #     user_otp_obj.save()
        #     send_otp_email(to_email=email, otp=otp)
        #     return Response(data = {'otp': otp, 'email':email})
        # else:
        #     print('in else')
        #     serializer = OTPSerializer(data=otp_data)
        #     serializer.is_valid(raise_exception=True)
        #     serializer.save()
        #     send_otp_email(to_email=email, otp=otp)
        #     return Response(data=serializer.data, status=status.HTTP_201_CREATED)
