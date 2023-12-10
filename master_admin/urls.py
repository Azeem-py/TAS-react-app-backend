from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register(r'branch-admin', BranchAdminView, basename='branch-admin')
router.register(r'branch', BranchView, basename='branch')
# router.register(r'get-branch-info', BranchDetails, basename='get-branch-info')

urlpatterns = [
    path('', include(router.urls)),
    path('branch-admin/<str:email>/isVerified/', BranchAdminView.as_view({'patch': 'partial_update'})),
    path('branch/<int:pk>/', BranchView.as_view({'get': 'getInfo'})),
    path('validate-branch/<str:email>', BranchAdminView.as_view({'get':'validate_if_branch'})),
]