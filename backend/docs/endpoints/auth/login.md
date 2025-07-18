# Authentication API Documentation

## Login User

**Function:** `login_user`

**DTO** `LoginDTO`

### Description

Authenticates a user and returns authentication tokens.

### URL

`POST /auth/login`

### Requirements

- [x] Valid email address
- [x] Correct password

### Request

**Headers**

```
Content-Type: application/json
```

**URL Params**

Not provided.

**Query Params**

Not provided.

**Body**

Login request body containing user credentials.

#### Example Body Content
```json
{
    "email": "testuser3@gmail.com",
    "password": "deneme123."
}
```

**Example cURL**

```bash
curl --location 'http://127.0.0.1:8000/auth/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "testuser3@gmail.com",
    "password": "deneme123."
}'
```

### Response

**Body**

```json
{
    "message": "Login successful",
    "data": {
        "access_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjQ3YWU0OWM0YzlkM2ViODVhNTI1NDA3MmMzMGQyZThlNzY2MWVmZTEiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoic3Uga2_DpyIsInBlcnNvbklkIjoiRlBWTUFuMGxyb1c2a3Y0VVUxTDM2cDNXV2NZMiIsImZpcnN0TmFtZSI6InN1IiwibGFzdE5hbWUiOiJrb8OnIiwiZW1haWwiOiJ0ZXN0dXNlcjNAZ21haWwuY29tIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL3l6dGEtYm9vdGNhbXAiLCJhdWQiOiJ5enRhLWJvb3RjYW1wIiwiYXV0aF90aW1lIjoxNzUyMzk2NTA3LCJ1c2VyX2lkIjoiRlBWTUFuMGxyb1c2a3Y0VVUxTDM2cDNXV2NZMiIsInN1YiI6IkZQVk1BbjBscm9XNmt2NFVVMUwzNnAzV1djWTIiLCJpYXQiOjE3NTIzOTY1MDcsImV4cCI6MTc1MjQwMDEwNywiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInRlc3R1c2VyM0BnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.jsq7YKcl2vC8yLhJV9fA_aCUhx6njunTO6xw6XO-wkekWH8nKi9QuOA7f6v5_XXZwjUwMvTrLWzXGcGK5BFyzYrJRAV13CdRz1SX3i0nih9IweOvp2_D3j_AKMqPUEpt-Zk6P4o00nY-Td9eyJ4IR5OH4edoDlW5gsnsMJI5d37n6RgcfymalwX_51KD7FowmVYjvKHHA0UV3nCvcytY-FFl7oBvjCnRFW4u_jKq6tmcdFtIwf99gbe4xa7_3rI11UOauH5m_XzEkKkq_c0o7SyHtMLlTyzevAnRvsxXszKNUyRx7mDMhbwajnOmgU_ZBh8jZOlmy-06ioytwen1eg",
        "refresh_token": "AMf-vByx3UjPUNy28FWEcOMnOlYi3cEQk5YR-WFGnRlP06aUHUJwr8fk6hsfZMwH1GT8AL1RKFlyKlzD7ZHiD1h5TlBuVo-BqyjQMH0nelVsuZ6vtw5cQLaEmr5CPgPR1oPItOc7JKGHCRp83RpHG_9znejZD1_OukHTqqSjEpF19-6xi7KmjLeMhEnxkzyvPH8DA2yKMuq-4En3vWzCzXhLsLfReWwfjA",
        "custom_token": "eyJhbGciOiAiUlMyNTYiLCAidHlwIjogIkpXVCIsICJraWQiOiAiMDg4M2EyZDM2NWY0N2UwOTViMjE5NjU3ODE4ZTg0OTgyNTkzMmIyYyJ9.eyJpc3MiOiAiYmFja2VuZC1hcGlAeXp0YS1ib290Y2FtcC5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsICJzdWIiOiAiYmFja2VuZC1hcGlAeXp0YS1ib290Y2FtcC5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsICJhdWQiOiAiaHR0cHM6Ly9pZGVudGl0eXRvb2xraXQuZ29vZ2xlYXBpcy5jb20vZ29vZ2xlLmlkZW50aXR5LmlkZW50aXR5dG9vbGtpdC52MS5JZGVudGl0eVRvb2xraXQiLCAidWlkIjogIkZQVk1BbjBscm9XNmt2NFVVMUwzNnAzV1djWTIiLCAiaWF0IjogMTc1MjM5NjUwOCwgImV4cCI6IDE3NTI0MDAxMDgsICJjbGFpbXMiOiB7InBlcnNvbklkIjogIkZQVk1BbjBscm9XNmt2NFVVMUwzNnAzV1djWTIiLCAiZmlyc3ROYW1lIjogInN1IiwgImxhc3ROYW1lIjogImtvXHUwMGU3IiwgImVtYWlsIjogInRlc3R1c2VyM0BnbWFpbC5jb20ifX0.QpTPmjQBBVerWgTc18lp93rWajRvyaRuvxvRXCvpLh6_TTL2sP4iAdRYu3FLGoa7rcwoQgLwpm58d6i25I6fuxq42fAxqBXUPV2D6gVpfMH0vVqhcp7PFuv7sM03cKq2vr5kCw19Kk3WaMw7c3qvqEr0UqA5Q93Bo6phhIbYZ9pT-f-1_TZIpXxdObMjt5g5hFq7e2t_OdoAaOxEOjtVnb8eHwsIp7mXfeMwh9Xcuqmcqh3PsmHm4DgZS3K35uZTWZb42w6gogCPMlhKI6rhKlZe-38T1oVOjT8n2vsfyF7FwAgNJg8EJE-74LISxzG2-iSM1Wskl2apNWG8t-dNZw",
        "user_id": "FPVMAn0lroW6kv4UU1L36p3WWcY2",
        "user_data": {
            "first_name": "su",
            "last_name": "koç",
            "email": "testuser3@gmail.com"
        }
    }
}
```

**HTTP Status:** `200 OK`

**Error Response:**

- `401 Unauthorized` - INVALID_LOGIN_CREDENTIALS

---
