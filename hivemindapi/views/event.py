from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from hivemindapi.models import Event
from rest_framework.decorators import action
from django.contrib.auth.models import User
from hivemindapi.models.cities import City

from hivemindapi.views import city


class EventView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        events = Event.objects.get(pk=pk)
        serializer = EventSerializer(events)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        events = Event.objects.all()

        # request.auth holds token object
        # auth.user gets the user object associated with token
        # Set the `joined` property on every event

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):

        creator = request.auth.user

        serializer = CreateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(creator=creator)
        event = Event.objects.get(pk=serializer.data["id"])
        event.city.add(request.data["city"])
        return Response(serializer.data)

    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True)
    def events_by_city(self, request, pk):
        param = self.request.query_params.get('name', None)
        if param is None:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)
        events = Event.objects.filter(city_name=param)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def events_by_date(self, request, pk):
        param = self.request.query_params.get('date', None)
        if param is None:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)
        events = Event.objects.filter(event_date=param)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    @action(methods=["get"], detail=False)
    def my_events(self, request):

        events = Event.objects.filter(creator=request.auth.user)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def update(self, request, pk):

        event = Event.objects.get(pk=pk)
        event.name = request.data["name"]
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]
        event.imgAddress = request.data["imgAddress"]

        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'name', 'description', 'date',
                  'time', 'creator', 'imgAddress', 'extraLink', 'city')
        depth = 2


class CreateEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'name', 'description', 'date',
                  'time', 'creator', 'imgAddress', 'extraLink')
        depth = 1
