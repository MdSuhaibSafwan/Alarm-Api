from rest_framework import serializers
from .models import Device, Alarm, Acknowledgement, Node, AlarmSeverity
from django.urls import reverse


class NodeRefSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Node
        fields = ['id', 'url']


class NodeForAcknowledgementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Node
        fields = "__all__"


class NodeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Node
        fields = '__all__'


class AlarmHyperlinkSerializer(serializers.HyperlinkedModelSerializer):


    class Meta:
        model = Alarm
        fields = "__all__"


class AckSerializer(serializers.ModelSerializer):
    alarm = AlarmHyperlinkSerializer(read_only=True)
    acknowledger = serializers.StringRelatedField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    node = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Acknowledgement
        fields = '__all__'

    def get_node(self, serializer):  # get_methodname
        alarm = serializer.alarm
        node = alarm.node

        return NodeForAcknowledgementSerializer(node).data

    def get_url(self, serializer):
        pk = serializer.pk
        url = reverse("Ack-Retrieve", kwargs={"id": pk})
        return "http://127.0.0.1:8000" + str(url)


class AlarmSerializer(serializers.ModelSerializer):
    node = NodeSerializer(read_only=True)
    ack = AckSerializer(read_only=True)
    severity = serializers.SerializerMethodField()

    class Meta:
        model = Alarm
        fields = '__all__'

    def get_severity(self, serializer):
        severity = serializer.severity
        value = AlarmSeverity(severity).label
        return value
        