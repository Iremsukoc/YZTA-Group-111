# Start Chat API Documentation

## Start Chat Session

**Function:** `start_chat`

**DTO** `StartGeneralTestChatRequestDTO`

**Response DTO** `StartGeneralTestChatResponseDTO`

### Description

Starts a new chat session for a user. Creates a unique session ID and initializes the chat history with system prompt in database. This endpoint is used to begin a new conversation with the AI assistant.

### URL

`POST /chat/start`

### Requirements

- [x] Valid user ID must be provided

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

Start chat request body containing user identification.

#### Example Body Content
```json
{
    "user_id": "user123"
}
```

**Example cURL**

```bash
curl --location 'http://127.0.0.1:8000/chat/start' \
--header 'Content-Type: application/json' \
--data-raw '{
    "user_id": "user123"
}'
```

### Response

**Body**

```json
{
    "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "message": "Chat session started."
}
```

**HTTP Status:** `200 OK`

**Error Responses:**

- `500 Internal Server Error` - Database connection error or system failure

### Technical Details

- Generates a unique UUID for session ID
- Creates a new document in Firestore under `GeneralTestChatHistory/{user_id}/sessions/{session_id}`
- Initializes chat history with system prompt