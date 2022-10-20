from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import permissions, exceptions

from goals.models import BoardParticipant


class BoardPermissions(permissions.BasePermission):
    """
    Разрещения на доступ к доске.

    """

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()


class PermissionsCU(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            user = get_object_or_404(BoardParticipant, user_id=request.user.id)
        except Http404:
            raise exceptions.PermissionDenied(detail="you are not a member of this board")

        if user.role in [BoardParticipant.Role.owner, BoardParticipant.Role.writer]:
            return True

        return False
