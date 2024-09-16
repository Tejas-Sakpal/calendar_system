from typing import Any
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User


SESSION_TYPES = [
    ("Prelim", "Prelim"),
    ("Advance", "Advance")
]

class MeetingRoom(models.Model):
    room_name = models.CharField(_("Room Name"), max_length=50)
    is_occupied = models.BooleanField(_("Is Occupied"), default=False)

class Session(models.Model):
    name = models.CharField(_("Session Name"), max_length=50)
    session_type = models.CharField(_("Session Type"), max_length=50, choices=SESSION_TYPES)
    start_time = models.DateTimeField(_("Start Time"), auto_now=False, auto_now_add=False)
    end_time = models.DateTimeField(_("End Time"), null=True, blank=True)
    duration = models.DurationField(_("Duration"), null=True, blank=True)
    host_user = models.ForeignKey(User, related_name="session_user", on_delete=models.CASCADE)
    attendee = models.ManyToManyField(User)
    session_data = models.JSONField(_("Session Data"), null=True, blank=True)
    meeting_room = models.ForeignKey(MeetingRoom, related_name=_("session_room"), on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Session"
        verbose_name_plural = "Sessions"

    def save(self, *args, **kwargs):
        if not self.end_time and self.duration:
            self.end_time = self.start_time + self.duration
        self.meeting_room.is_occupied = True
        self.meeting_room.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.meeting_room.is_occupied = False
        self.meeting_room.save()        
        super().delete(*args, **kwargs)
