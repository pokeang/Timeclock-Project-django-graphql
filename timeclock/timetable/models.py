from django.db import models
from django.contrib.auth.models import User

class Clock(models.Model):
    user = models.ForeignKey(User, related_name='user_id', on_delete=models.CASCADE)
    clock_in = models.DateTimeField()
    clock_out = models.DateTimeField(null=True)

    class Meta:
        db_table = 'timetable'

