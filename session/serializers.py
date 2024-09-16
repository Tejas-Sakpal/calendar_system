from rest_framework import serializers
from .models import Session, MeetingRoom



class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = "__all__"


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = "__all__"


class GetSessionSerializer(serializers.ModelSerializer):
    meeting_room = MeetingRoomSerializer()
    class Meta:
        model = Session
        fields = "__all__"
