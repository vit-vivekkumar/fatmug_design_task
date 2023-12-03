from rest_framework import generics

from .utils import update_vendor_metrics
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Vendor
from .serializers import VendorSerializer
from django.utils import timezone


class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class VendorPerformanceView(APIView):
    def get(self, request, pk):
        vendor = Vendor.objects.get(pk=pk)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)
    
class AcknowledgePurchaseOrderView(APIView):
    def post(self, request, pk):
        purchase_order = PurchaseOrder.objects.get(pk=pk)
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()

        # Update vendor metrics after acknowledgment
        update_vendor_metrics(purchase_order.vendor)

        return Response({"message": "Purchase order acknowledged successfully."})