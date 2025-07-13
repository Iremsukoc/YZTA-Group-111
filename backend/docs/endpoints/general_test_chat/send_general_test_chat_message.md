# Send Message API Documentation

## Send Chat Message

**Function:** `send_chat_message`

**DTO** `GeneralTestChatMessageRequestDTO`

### Description

Sends a message to the AI assistant within an existing chat session. The message is processed by Google's Gemini AI model and the response is returned. Both user message and AI response are stored in the chat history.

### URL

`POST /chat/send`

### Requirements

- [x] Valid user ID must be provided
- [x] Valid session ID from an existing chat session
- [x] Message content must be provided
- [x] Gemini API key must be configured
- [x] Chat session must exist in database

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

Send message request body containing user ID, session ID, and message content.

#### Example Body Content
```json
{
    "user_id": "user123",
    "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "message": "Hello! I have a skin problem."
}
```

**Example cURL**

```bash
curl --location 'http://127.0.0.1:8000/chat/send' \
--header 'Content-Type: application/json' \
--data-raw '{
    "user_id": "user123",
    "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "message": "Hello! I have a skin problem."
}'
```

### Response

**Body**

```json
{
    "response": "I'm sorry to hear you're having a skin problem.  I can't offer medical advice, so I can't diagnose or treat your issue.  However, I can offer some general information and suggest steps you can take:\n\n* **Describe your symptoms:**  The more detail you can provide (location, appearance, texture, duration, any related symptoms), the better a doctor will be able to understand your situation.  Examples:  \"I have a red, itchy rash on my arm that started three days ago,\" or \"I have a dry, flaky patch on my scalp that's been there for months.\"\n* **See a dermatologist or your primary care doctor:**  They can properly diagnose your skin condition and recommend appropriate treatment.  This is the most important step.\n* **Keep a journal:**  Tracking your skin problem, including when it started, any triggers, and any treatments you try, can be helpful for your doctor.\n* **Avoid self-treating with strong medications or home remedies without consulting a doctor:**  Some treatments can worsen skin problems or interact with other medications.\n* **Over-the-counter options (with caution):** For mild issues like dry skin, you might consider gentle, fragrance-free moisturizers.  For itching, hydrocortisone cream can sometimes provide temporary relief.  However, if symptoms persist or worsen, see a doctor.\n\nRemember, I am not a medical professional.  The information I provide should not be considered medical advice.  Please consult a doctor for diagnosis and treatment.\n"
}
```

**HTTP Status:** `200 OK`