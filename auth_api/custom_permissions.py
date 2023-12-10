from rest_framework.permissions import BasePermission


class isBranchAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.isBranchAdmin


class isParent(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.isParent


class isTutor(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.isTutor


class isParentOrBranchAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.isBranchAdmin or user.isParent


class notStudent(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.isBranchAdmin or user.isParent or user.isTutor
