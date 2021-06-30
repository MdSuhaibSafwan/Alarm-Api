from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from . import serializers
from .models import Alarm, Node, Acknowledgement, People
from rest_framework.permissions import IsAuthenticated


class AlarmViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AlarmSerializer

    def get_queryset(self):
        return Alarm.objects.all()


class AlarmCurrentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AlarmSerializer

    def change_qs(self, current_qs):
        date = self.request.query_params.get("date", None)
        if date is not None:
            time_lst = date.split("-")
            for i in time_lst:
                try:
                    int(i)
                except ValueError:
                    raise PermissionDenied("Give an Integer...")

            year, month, day = time_lst[0], time_lst[1], time_lst[2]
            qs = current_qs.filter(opened__year=year)
            qs = qs.filter(opened__month=month)
            qs = qs.filter(opened__day__lte=day)
            
            if not qs.exists():
                raise NotFound("Qs with this Time do not exist...")

            return qs

        return current_qs

    def get_queryset(self):
        current = Alarm.objects.all() # (resolved__isnull=True) 
        prop = self.request.query_params.get("search", None)  # /api/history or /api/history/?search=MAJoasdr -> major
        device = self.request.query_params.get("device", None)
        current = self.change_qs(current)
        if prop is not None:
            prop = str(prop).upper()
            print(prop)
            if prop == "MAJOR":
                current = current.filter(severity__lte=2)

            elif prop == "MINOR":
                pass

            elif prop == "CRITICAL":   
                current = current.filter(severity=1)

            else:
                raise PermissionDenied("search property only takes...")

        if device is not None:
            try:
                device = int(device)
            except ValueError:
                raise PermissionDenied("Please Provide an Integer Value...")

            current = current.filter(node__id=device)
            if not current.exists():
                raise NotFound("Alarm with this Node donot exist...")

        return current


class AlarmHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AlarmSerializer

    def get_queryset(self):
        history = Alarm.objects.filter(resolved__isnull=False)
        return history


class NodeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.NodeSerializer

    def get_queryset(self):
        nodes = Node.objects.all()
        return nodes


class AckViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.NodeSerializer

    def get_queryset(self):
        ack = Acknowledgement.objects.all()
        return ack


class AlarmSeverityViewSet(ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = serializers.AckSerializer
    pk_url_kwarg = "alarm_id"

    def get_queryset(self):
        qs = Acknowledgement.objects.all()
        
        return qs

    # def get_serializer(self, *args, **kwargs):
    #     return self.serializer_class

    def list(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        pk = self.pk_url_kwarg  # alarm_id
        pk = self.kwargs.get(pk)  # Got The Id from Kwargs Dictionary
        print(pk)
        
        qs = Alarm.objects.filter(pk=pk)
        if not qs.exists():
            raise NotFound("Alarm With This Primary Key is not Found...")

        alarm_obj = qs.get()
        print("Alarm Object", alarm_obj)
        
        user = self.request.user
        print(user)

        people_obj = People.objects.first()  # ad_user => people
        print(people_obj)
        
        time_now = timezone.now()

        qs = Acknowledgement.objects.filter(alarm=alarm_obj)
        if qs.exists():
            raise PermissionDenied("A User Has already Acknowledged it...")

        serializer.save(
            acknowledger=people_obj, 
            created=time_now, 
            alarm=alarm_obj
        ) # Ack.objects.create(**kwargs)


    # def post(self, request, *args, **kwargs):
    #     # Serializer- > Data -> perform_create(serializer)


class AcknowledgementRetrieveAPIView(RetrieveAPIView):
    serializer_class = serializers.AckSerializer

    def get_queryset(self):
        pass

    def get_object(self):
        pk = self.kwargs.get("id")
        qs = Acknowledgement.objects.filter(pk=pk)
        if not qs.exists():
            raise NotFound("Object WIth this pk is not Found")
        obj = qs.get()
        return obj
        