from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from vendor_app.models import Vendor, PurchaseOrder
from datetime import datetime
import json
from django.core.serializers import serialize
from django.utils import timezone


class VendorViewSetTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
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

    def test_list_vendors(self):
        response = self.client.get('/api/Vendors/')
        self.assertEqual(response.status_code, 200)

    def test_retrieve_vendor(self):
        response = self.client.get(f'/api/Vendors/{self.vendor.id}/')
        self.assertEqual(response.status_code, 200)

    def test_create_vendor(self):
        data = {
            "name": "New Vendor",
            "contact_details": "new@example.com",
            "address": "New Address",
            "vendor_code": "V002",
            "on_time_delivery_rate": 90.0,
            "quality_rating_avg": 4.0,
            "average_response_time": 3.0,
            "fulfillment_rate": 95.0
        }
        response = self.client.post('/api/Vendors/', data)
        self.assertEqual(response.status_code, 201)

    def test_update_vendor(self):
        data = {
            "name": "Test Vendor",
            "contact_details": "test@example.com",
            "address": "Test Address",
            "vendor_code": "V001",
            "on_time_delivery_rate": 92.0,
            "quality_rating_avg": 4.2,
            "average_response_time": 2.5,
            "fulfillment_rate": 96.0
        }
        response = self.client.put(f'/api/Vendors/{self.vendor.id}/', data)
        self.assertEqual(response.status_code, 200)

    def test_delete_vendor(self):
        response = self.client.delete(f'/api/Vendors/{self.vendor.id}/')
        self.assertEqual(response.status_code, 204)

    def test_vendor_performance(self):
        response = self.client.get(
            f'/api/Vendors/{self.vendor.id}/performance/')
        self.assertEqual(response.status_code, 200)


class PurchaseOrderViewSetTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
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
        self.purchase_order = PurchaseOrder.objects.create(
            po_number="PO001",
            vendor=self.vendor,
            items={"name": "test_item"},
            order_date=datetime.now(),
            # status='pending',
            issue_date=datetime.now()
        )

    def test_list_purchase_orders(self):
        response = self.client.get('/api/PurchaseOrder/')
        self.assertEqual(response.status_code, 200)

    def test_retrieve_purchase_order(self):
        response = self.client.get(
            f'/api/PurchaseOrder/{self.purchase_order.id}/')
        self.assertEqual(response.status_code, 200)

    def test_create_purchase_order(self):
        data = {
            "po_number": "P005",
            "order_date": "2023-12-04",
            "delivery_date": None,
            "items": {},
            "quantity": 3,
            "status": "pending",
            "quality_rating": 5,
            "issue_date": "2023-12-07",
            "acknowledgment_date": None,
            "vendor": self.vendor.id
        }

        # data = serialize('json', data)
        response = self.client.post(
            '/api/PurchaseOrder/', json.dumps(data), content_type='application/json')
        print(response.content)
        self.assertEqual(response.status_code, 201)

    def test_update_purchase_order(self):
        data = {
            "po_number": "P005",
            "order_date": "2023-12-04",
            "delivery_date": None,
            "items": {},
            "quantity": 3,
            "status": "completed",
            "quality_rating": 5,
            "issue_date": "2023-12-07",
            "acknowledgment_date": None,
            "vendor": self.vendor.id
        }
        response = self.client.put(
            f'/api/PurchaseOrder/{self.purchase_order.id}/', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_delete_purchase_order(self):
        response = self.client.delete(
            f'/api/PurchaseOrder/{self.purchase_order.id}/')
        self.assertEqual(response.status_code, 204)

    def test_acknowledge_purchase_order(self):
        response = self.client.post(
            f'/api/PurchaseOrder/{self.purchase_order.id}/acknowledge/')
        self.assertEqual(response.status_code, 200)
