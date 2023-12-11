from django.test import TestCase
from vendor_app.models import Vendor, PurchaseOrder, HistoricalPerformance
from vendor_app.serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer


class VendorSerializerTest(TestCase):
    def test_vendor_serializer(self):
        vendor_data = {
            "name": "Test Vendor",
            "contact_details": "test@example.com",
            "address": "Test Address",
            "vendor_code": "V001",
            "on_time_delivery_rate": 95.5,
            "quality_rating_avg": 4.5,
            "average_response_time": 2.0,
            "fulfillment_rate": 98.0
        }

        serializer = VendorSerializer(data=vendor_data)
        self.assertTrue(serializer.is_valid())

        vendor_instance = serializer.save()
        self.assertEqual(vendor_instance.name, "Test Vendor")


class PurchaseOrderSerializerTest(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="test@example.com",
            address="Test Address",
            vendor_code="V001",
            on_time_delivery_rate=95.5,
            quality_rating_avg=4.5,
            average_response_time=2.0,
            fulfillment_rate=98.0
        )

    def test_purchase_order_serializer(self):
        po_data = {
            "po_number": "PO001",
            "vendor": self.vendor.id,
            "order_date": "2022-01-01T12:00:00Z",
            "delivery_date": "2022-01-08T12:00:00Z",
            "items": {"item1": 10, "item2": 20},
            "quantity": 30,
            # "status": "pending",
            "quality_rating": 4.0,
            "issue_date": "2022-01-01T12:00:00Z",
            "acknowledgment_date": "2022-01-01T13:00:00Z"
        }

        serializer = PurchaseOrderSerializer(data=po_data)
        self.assertTrue(serializer.is_valid())

        po_instance = serializer.save()
        self.assertEqual(po_instance.po_number, "PO001")


class HistoricalPerformanceSerializerTest(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="test@example.com",
            address="Test Address",
            vendor_code="V001",
            on_time_delivery_rate=95.5,
            quality_rating_avg=4.5,
            average_response_time=2.0,
            fulfillment_rate=98.0
        )

    def test_historical_performance_serializer(self):
        performance_data = {
            "vendor": self.vendor.id,
            "date": "2022-01-01T12:00:00Z",
            "on_time_delivery_rate": 95.0,
            "quality_rating_avg": 4.2,
            "average_response_time": 2.5,
            "fulfillment_rate": 97.0
        }

        serializer = HistoricalPerformanceSerializer(data=performance_data)
        self.assertTrue(serializer.is_valid())

        performance_instance = serializer.save()
        self.assertEqual(str(performance_instance), "Test Vendor - {}".format(
            performance_instance.date.strftime('%Y-%m-%d')))
