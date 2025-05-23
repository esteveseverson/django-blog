from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response

from base.models import Room
from .serializers import RoomSerializer

@api_view(['GET'])
def get_route(request: HttpRequest):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]

    return Response(routes)


@api_view(['GET'])
def get_rooms(request: HttpRequest):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
def get_room(request: HttpRequest, pk: str):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    
    return Response(serializer.data)