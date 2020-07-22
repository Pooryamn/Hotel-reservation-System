from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Reserve
from .serializers import ReserveSerializer, ReserveTrackingSerializer


class ReserveTrackingAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = ReserveTrackingSerializer(request.data)

        tracking_code = serializer.data.get("tracking_code", None)
        phone = serializer.data.get("phone", None)

        reserve = get_object_or_404(Reserve, trackingCode=tracking_code,
                                             user__profile__phone=phone)

        reserve_serializer = ReserveSerializer(reserve)

        response_dict = reserve_serializer.data
        response_dict["rooms"] = list(reserve.room.values_list('room_number', flat=True))
        response_dict["hotel"] = reserve.room.first().hotel.name
        response_dict["first_name"] = reserve.user.first_name
        response_dict["last_name"] = reserve.user.last_name

        return Response(response_dict)

