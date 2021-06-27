from django.contrib import admin
from .models import Alarm, Node, Acknowledgement

admin.site.register(Alarm)
admin.site.register(Node)
admin.site.register(Acknowledgement)
