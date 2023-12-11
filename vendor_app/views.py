from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from datetime import datetime


class VendorViewSet(viewsets.ModelViewSet):
    serializer_class = VendorSerializer
    queryset = Vendor.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def performance(self, request, pk=None):
        vendor = self.get_object()
        performance_data = {
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'average_response_time': vendor.average_response_time,
            'fulfillment_rate': vendor.fulfillment_rate,
        }

        return Response(performance_data)


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseOrderSerializer
    queryset = PurchaseOrder.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['POST'])
    def acknowledge(self, request, pk=None):
        purchase_order = self.get_object()
        purchase_order.acknowledgment_date = datetime.now()
        purchase_order.save()
        return Response({"message": "Acknowledged"})
