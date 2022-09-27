from django.shortcuts import get_object_or_404
from rest_framework import permissions

from goals.models import BoardParticipant, GoalComment


class BoardPermissions(permissions.BasePermission):

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

        if get_object_or_404(BoardParticipant, pk=request.user.id).role not in [BoardParticipant.Role.owner,
                                                                                BoardParticipant.Role.writer]:
            return False
        return True

