from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from hivemindapi.models import City
from rest_framework.decorators import action


class CityView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        cities = City.objects.get(pk=pk)
        serializer = CitySerializer(cities)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        cities = City.objects.all()

        # request.auth holds token object
        # auth.user gets the user object associated with token
        # Set the `joined` property on every event

        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)

    def create(self, request):

        city = City.objects.get(pk=request.data["city"])

        serializer = CreateCitySerializer(city)
        return Response(serializer.data)


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('id', 'name')


class CreateCitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('name')
