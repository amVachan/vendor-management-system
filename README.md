# Vendor Management System

## Overview

The Vendor Management System is a Django project developed to manage vendor profiles, track purchase orders, and calculate vendor performance metrics.

## Setup Instructions

### Prerequisites

- Python 3.x installed
- Virtual environment (optional but recommended)

### Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/your-username/vendor-management-system.git
    ```

2.  Navigate to the project directory:
    ```bash
    cd vendor-management-system
    ```
3.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    # On Windows, use `venv\Scripts\activate`
    ```
4.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5.  Apply database migrations:
    ```bash
    python manage.py createsuperuser
    ```

### Running the Project

```bash
python manage.py runserver
```

## Authenticating Requests

To make authenticated requests to the API, you need to include an authorization token in the header of your HTTP requests. Follow these steps:

1. **Generate an Authorization Token:**

   - Use the `/api/token/` endpoint to generate an authorization token.
   - Send a `POST` request with your username and password in the request body.
   - Example using cURL:
     ```bash
     curl -X POST http://127.0.0.1:8000/api/token/ -d "username=your_username&password=your_password"
     ```

2. **Include the Token in Header:**

   - For each subsequent API request, include the authorization token in the header with the key `Authorization`.
   - The value should be in the format `Token <your_token>`. Replace `<your_token>` with the actual token you obtained.

   Example using cURL:

   ```bash
   curl -X GET http://127.0.0.1:8000/api/vendors/ -H "Authorization: Token <your_token>"
   ```

## API Endpoints

### Vendor Profile Management

- Create a new vendor:

  - Endpoint: POST `/api/vendors/`
  - Example Request Body:

  ```JSON
  {
  "name": "Vendor5",
  "contact_details": "vendor5@gmail.com",
  "address": "some address in mumbai, maharashtra",
  "vendor_code": "V005",
  "on_time_delivery_rate": 0.0,
  "quality_rating_avg": 0.0,
  "average_response_time": 0.0,
  "fulfillment_rate": 0.0
  }
  ```

- List all vendors:
  - Endpoint: `GET /api/vendors/`
- Retrieve a specific vendor's details:

  - Endpoint: GET `/api/vendors/{vendor_id}/`

- Update a vendor's details:

  - Endpoint: PUT `/api/vendors/{vendor_id}/`
  - Example Request Body:

  ```JSON
  {
  "name": "Vendor5",
  "contact_details": "vendor5@gmail.com",
  "address": "some address in mumbai, maharashtra",
  "vendor_code": "V005",
  "on_time_delivery_rate": 5.0,
  "quality_rating_avg": 6.0,
  "average_response_time": 0.0,
  "fulfillment_rate": 0.0
  }
  ```

- Delete a vendor:

  - Endpoint: DELETE `/api/vendors/{vendor_id}/`

- Retrieve a specific vendor's performance metrics:
  - Endpoint: GET `/api/vendors/{vendor_id}/performance`

### Purchase Order Tracking

- Create a purchase order:

  - Endpoint: POST `/api/purchase_orders/`
  - Example Request Body:

  ```JSON
  {
  "po_number": "P007",
  "order_date": "2023-12-04",
  "delivery_date": "",
  "items": {},
  "quantity": 3,
  "status": "pending",
  "quality_rating": 5,
  "issue_date": "2023-12-07",
  "acknowledgment_date": "",
  "vendor": 1
  }
  ```

- List all purchase orders:

  - Endpoint: GET `/api/purchase_orders/`

- Retrieve details of a specific purchase order:

  - Endpoint: GET `/api/purchase_orders/{po_id}/`

- Update a purchase order:

  - Endpoint: PUT `/api/purchase_orders/{po_id}/`
  - Example Request Body:

  ```JSON
  {
  "po_number": "P007",
  "order_date": "2023-12-04",
  "delivery_date": "",
  "items": {},
  "quantity": 3,
  "status": "completed",
  "quality_rating": 5,
  "issue_date": "2023-12-07",
  "acknowledgment_date": "",
  "vendor": 1
  }
  ```

* Delete a purchase order:

  - Endpoint: DELETE `/api/purchase_orders/{po_id}/`

* Acknowledge a purchase order:
  - Endpoint: POST `/api/purchase_orders/{po_id}/acknowledge`

## Testing

- Run the test suite:

```bash
    python manage.py test
```
