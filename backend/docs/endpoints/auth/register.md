# Authentication API Documentation

## Register User

**Function:** `register_user`

**DTO** `RegisterDTO`

### Description

Registers a new user in the system. Creates a new user account with the provided email, password, and personal information.

### URL

`POST /auth/register`

### Requirements

- [x] Valid email address format
- [x] Password meeting security requirements
- [x] First name and last name must be provided

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

Register request body containing user registration information.

#### Example Body Content
```json
{
    "email": "testuser3@gmail.com",
    "password": "deneme123.",
    "first_name": "su",
    "last_name": "koç"
}
```

**Example cURL**

```bash
curl --location 'http://127.0.0.1:8000/auth/register' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "testuser3@gmail.com",
    "password": "deneme123.",
    "first_name": "su",
    "last_name": "koç"
}'
```

### Response

**Body**

```json
{
    "message": "User registered successfully",
    "data": {
        "custom_token": "eyJhbGciOiAiUlMyNTYiLCAidHlwIjogIkpXVCIsICJraWQiOiAiMDg4M2EyZDM2NWY0N2UwOTViMjE5NjU3ODE4ZTg0OTgyNTkzMmIyYyJ9.eyJpc3MiOiAiYmFja2VuZC1hcGlAeXp0YS1ib290Y2FtcC5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsICJzdWIiOiAiYmFja2VuZC1hcGlAeXp0YS1ib290Y2FtcC5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsICJhdWQiOiAiaHR0cHM6Ly9pZGVudGl0eXRvb2xraXQuZ29vZ2xlYXBpcy5jb20vZ29vZ2xlLmlkZW50aXR5LmlkZW50aXR5dG9vbGtpdC52MS5JZGVudGl0eVRvb2xraXQiLCAidWlkIjogIkJ0bWFEQkFyOW5kcXpnbWRhTmc2SWxjdW9yRzIiLCAiaWF0IjogMTc1MjM5NjMyOSwgImV4cCI6IDE3NTIzOTk5MjksICJjbGFpbXMiOiB7InBlcnNvbklkIjogIkJ0bWFEQkFyOW5kcXpnbWRhTmc2SWxjdW9yRzIiLCAiZmlyc3ROYW1lIjogInN1IiwgImxhc3ROYW1lIjogImtvXHUwMGU3IiwgImVtYWlsIjogInRlc3R1c2VyODBAZ21haWwuY29tIn19.drawnca0zITuyMg_0ng_6rlJfg23zslsbqtte-_vwccwYqynegyopXQOkn_9asM14Bg2lWXmbZSy94r8hD_UlGy1pbF7MwxiA4Gz-VhfsMszZMA-pGb6kdt5mTGph3L1qgL2jgZrf_6Y_uZGbupkxjMkb87xzFKaVKmb7z9aqzYWOVIq9NMfQ82HgT8BOi0mYPHuUDPqwKC0J3eMdiPgE5hHufZFcVYDupGTIxReV6XFJOSNklBPVOopTd0ljnDBNgLgxikKpAd_seIAbplpSIPsu7esxHGSHHBlvYdj97TtnDfucyBxUCQIKoig2q6dX_HJasJMwLpKSL2wtOYitA",
        "user_id": "BtmaDBAr9ndqzgmdaNg6IlcuorG2"
    }
}
```

**HTTP Status:** `201 Created`

**Error Response:**

- `500 Internal Server Error` - Email address already exists

---

