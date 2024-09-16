from django.utils.translation import gettext_lazy as _
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from session.models import Session, MeetingRoom
from session.serializers import SessionSerializer, GetSessionSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.shortcuts import get_object_or_404

class SessionAPIView(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == "list":
            return GetSessionSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        request_data = request.data
        attendee = request_data.get("attendee", [])
        if not attendee:
            return Response({"error": "Please add attendee"}, status=status.HTTP_400_BAD_REQUEST)

        if request_data.get("session_type") == "Prelim":
            if len(attendee) > 1:
                return Response({"error": "You can't add more than one attendee for prelim sessions"}, status=status.HTTP_400_BAD_REQUEST)
        meeting_room = get_object_or_404(MeetingRoom, id=request_data.get("meeting_room"))
        if meeting_room.is_occupied:
            return Response({"error": "Meeting room not available"}, status=status.HTTP_400_BAD_REQUEST)
        
        conflicts = self.queryset.filter(attendee__id__in=attendee).filter(
            Q(start_time__lte=request_data.get("start_time"), end_time__gte=request_data.get("start_time"))
            | Q(start_time__lte=request_data.get("end_time"), end_time__gte=request_data.get("end_time"))
        )
        if conflicts.exists():
            return Response({"error": "Conflicts in scheduled meeting with as attendees have scheduled meetings"}, status=status.HTTP_400_BAD_REQUEST)
        request_data["host_user"] = request.user.id
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
