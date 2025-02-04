# Household Services Application - Complete Backend Testing Guide

## Environment Setup
1. Create a new environment in Postman
2. Add the following variables:
   - `BASE_URL`: http://localhost:5000
   - `ADMIN_TOKEN`: (Will be set after admin login)
   - `CUSTOMER_TOKEN`: (Will be set after customer login)
   - `PROFESSIONAL_TOKEN`: (Will be set after professional login)

## Test Flow Sequence

### 1. Authentication Flow

#### 1.1 Admin Authentication
POST {{BASE_URL}}/auth/login
```json
{
    "email": "admin@example.com",
    "password": "Admin@123"
}
```

#### 1.2 Register Customer
POST {{BASE_URL}}/auth/register/customer
```json
{
    "email": "customer@test.com",
    "password": "password123",
    "name": "Test Customer",
    "pin_code": "123456"
}
```

#### 1.3 Register Professional
POST {{BASE_URL}}/auth/register/professional
```json
{
    "email": "professional@test.com",
    "password": "password123",
    "name": "Test Professional",
    "service_type": "Plumbing",
    "experience": 5,
    "description": "Experienced plumber"
}
```

### 2. Admin Operations

#### 2.1 View Pending Professionals
GET {{BASE_URL}}/admin/professionals/pending
Headers:
- Authorization: Bearer {{ADMIN_TOKEN}}

#### 2.2 Approve Professional
POST {{BASE_URL}}/admin/professionals/1/approve
Headers:
- Authorization: Bearer {{ADMIN_TOKEN}}

#### 2.3 Create Service
POST {{BASE_URL}}/admin/services
Headers:
- Authorization: Bearer {{ADMIN_TOKEN}}
```json
{
    "name": "Pipe Repair",
    "description": "Fix leaking pipes",
    "category": "Plumbing",
    "base_price": 50.00,
    "required_time": 60
}
```

### 3. Customer Operations

#### 3.1 Create Service Request
POST {{BASE_URL}}/customer/service-request
Headers:
- Authorization: Bearer {{CUSTOMER_TOKEN}}
```json
{
    "service_id": 1,
    "description": "Leaking kitchen sink",
    "preferred_date": "2024-01-20",
    "preferred_time": "10:00",
    "address": "123 Test Street",
    "pin_code": "123456"
}
```

#### 3.2 View Service Requests
GET {{BASE_URL}}/customer/service-requests
Headers:
- Authorization: Bearer {{CUSTOMER_TOKEN}}

### 4. Professional Operations

#### 4.1 View Available Requests
GET {{BASE_URL}}/professional/requests
Headers:
- Authorization: Bearer {{PROFESSIONAL_TOKEN}}

#### 4.2 Accept Request
POST {{BASE_URL}}/professional/requests/1/accept
Headers:
- Authorization: Bearer {{PROFESSIONAL_TOKEN}}

#### 4.3 Complete Request
POST {{BASE_URL}}/professional/requests/1/complete
Headers:
- Authorization: Bearer {{PROFESSIONAL_TOKEN}}
```json
{
    "notes": "Fixed leaking pipe",
    "duration": 45
}
```

### 5. Service Operations

#### 5.1 List Services
GET {{BASE_URL}}/services

#### 5.2 Search Services
GET {{BASE_URL}}/services/search?q=plumbing&pin_code=123456

#### 5.3 Get Service Details
GET {{BASE_URL}}/services/1

For each endpoint, verify:
1. Response status code
2. Response body structure
3. Error handling
4. Authorization requirements