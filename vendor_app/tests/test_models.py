from django.test import TestCase
from django.utils import timezone
from vendor_app.models import Vendor, PurchaseOrder, HistoricalPerformance


class VendorModelTest(TestCase):
    def test_vendor_creation(self):
        vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="test@example.com",
            address="Test Address",
            vendor_code="V001",
            on_time_delivery_rate=95.5,
            quality_rating_avg=4.5,
            average_response_time=2.0,
            fulfillment_rate=98.0
        )
        self.assertEqual(str(vendor), "Test Vendor")


class PurchaseOrderModelTest(TestCase):
    def test_purchase_order_creation(self):
        vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="test@example.com",
            address="Test Address",
            vendor_code="V001",
            on_time_delivery_rate=95.5,
            quality_rating_avg=4.5,
            average_response_time=2.0,
            fulfillment_rate=98.0
        )

        # Use one of the choices defined in the status field
        purchase_order = PurchaseOrder.objects.create(
            po_number="PO001",
            vendor=vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now() + timezone.timedelta(days=7),
            items={"item1": 10, "item2": 20},
            quantity=30,
            # status=PurchaseOrder.status.pending,
            quality_rating=4.0,
            issue_date=timezone.now(),
            acknowledgment_date=timezone.now() + timezone.timedelta(days=1)
        )

        self.assertEqual(str(purchase_order), "PO PO001 - Test Vendor")


class HistoricalPerformanceModelTest(TestCase):
    def test_historical_performance_creation(self):
        vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="test@example.com",
            address="Test Address",
            vendor_code="V001",
            on_time_delivery_rate=95.5,
            quality_rating_avg=4.5,
            average_response_time=2.0,
            fulfillment_rate=98.0
        )
        historical_performance = HistoricalPerformance.objects.create(
            vendor=vendor,
            date=timezone.now(),
            on_time_delivery_rate=94.0,
            quality_rating_avg=4.2,
            average_response_time=2.2,
            fulfillment_rate=97.0
        )
        self.assertEqual(str(historical_performance), "Test Vendor - {}".format(
            historical_performance.date.strftime('%Y-%m-%d')))
