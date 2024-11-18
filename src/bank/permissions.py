from rest_framework import permissions
from rest_framework.schemas.inspectors import re


class IsCustomer(permissions.BasePermission):
    """
    Custom permission to only allow registered customer to view information or edit it.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class UserIsAcHolder(permissions.BasePermission):
    """
    Custom permission to only allow customer holding given account view information or edit it.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.ac_holder.user == request.user


class UserIsCardHolder(permissions.BasePermission):
    """
    Custom permission class to only allow account holder holding given card to view information or edit objects.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.ac_no == view.kwargs.get("ac_no")


class UserHoldsAccount(permissions.BasePermission):
    """
    Custom permission class to only allow account holder to view information or edit objects.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.ac_no in view.get_customer_accounts()
