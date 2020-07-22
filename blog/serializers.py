from rest_framework import serializers
from .models import Reserve


class ReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        fields = (
            'id',
            'beginDate',
            'endDate',
            'totalPrice',
            'trackingCode',
            'created',
            )


class ReserveTrackingSerializer(serializers.Serializer):
    tracking_code = serializers.CharField(max_length=10)
    phone = serializers.CharField(max_length=11)