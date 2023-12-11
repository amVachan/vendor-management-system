from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from vendor_app.models import Vendor, PurchaseOrder, HistoricalPerformance
from vendor_app.signals import calculate_metrics


class SignalsTest(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="test@example.com",
            address="Test Address",
            vendor_code="V001",
            on_time_delivery_rate=0.0,
            quality_rating_avg=0.0,
            average_response_time=0.0,
            fulfillment_rate=0.0
        )
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_calculate_metrics_on_status_change(self):
        po = PurchaseOrder.objects.create(
            po_number="PO001",
            vendor=self.vendor,
            order_date=timezone.now(),
            items={},
            status='pending',
            issue_date=timezone.now()
        )

        po.status = 'completed'
        po.quality_rating = 4.0
        po.save()

        self.vendor.refresh_from_db()

        self.assertEqual(self.vendor.on_time_delivery_rate, 0.0)
        self.assertEqual(self.vendor.quality_rating_avg, 4.0)
        self.assertEqual(self.vendor.fulfillment_rate, 1.0)
        self.assertEqual(self.vendor.average_response_time, 0.0)

    def test_calculate_metrics_on_acknowledgment_date_change(self):
        print(self.vendor.average_response_time)
        po = PurchaseOrder.objects.create(
            po_number="PO002",
            vendor=self.vendor,
            order_date=timezone.now(),
            items={},
            status='completed',
            issue_date=timezone.now(),
            acknowledgment_date=timezone.now()
        )
        print(po.issue_date)
        new_ack_date = timezone.now() + timezone.timedelta(hours=3)
        po.acknowledgment_date = new_ack_date
        po.save()

        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.average_response_time, 3.0)
