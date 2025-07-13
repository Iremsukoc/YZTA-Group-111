# Get History API Documentation

## Get Chat History

**Function:** `get_history`

**Response DTO** `GeneralTestChatHistoryResponseDTO`

### Description

Retrieves the complete chat history for a specific user session. Returns all messages exchanged between the user and AI assistant, including timestamps and roles (user/assistant/system).

### URL

`GET /chat/history/{user_id}/{session_id}`

### Requirements

- [x] Valid user ID must be provided in URL path
- [x] Valid session ID must be provided in URL path

### Request

**Headers**

```
Content-Type: application/json
```

**URL Params**

- `user_id` (string, required): The unique identifier of the user
- `session_id` (string, required): The unique identifier of the chat session

**Query Params**

Not provided.

**Body**

Not provided.

**Example cURL**

```bash
curl --location 'http://localhost:8000/chat/history/FPVMAn0lroW6kv4UU1L36p3WWcY2/98b756fa-580e-4786-8558-82f549c9005e' \
--header 'Content-Type: application/json'
```

### Response

**Body**

```json
{
    "user_id": "FPVMAn0lroW6kv4UU1L36p3WWcY2",
    "session_id": "98b756fa-580e-4786-8558-82f549c9005e",
    "history": [
        {
            "content": "\nYou are an expert medical assistant and you automatically detect the language the user is speaking and respond in that language. If the language is not supported, you will respond in English.\nYour objectives are:\n1️- Collect the user's general health information.\n2️- Learn about the user's symptoms in detail (duration, severity, triggering factors, accompanying symptoms).\n3️- Analyze the risk level and indicate urgency if necessary.\n4️- Clearly inform the user whether they should see a doctor.\n### Rules for Collecting General Health Information:\n- Do not ask for all information at once; ask step by step.\n- After each answer, thank the user and proceed to the next question.\n- If the user does not wish to share certain information, accept this respectfully and continue to the next step.\n### Order of Questions:\n1️- Age and gender.  H\n2️- Height and weight.\n3️- Use of tobacco, alcohol, and drugs.  \n4️- Allergies and medications used regularly.  \n5️- Existing medical conditions (hypertension, diabetes, asthma, etc.) and family history of chronic diseases.  \n6️- Occupation and recent travel history.\n### Rules for Asking About Symptoms:\n- Ask questions to understand the symptoms in detail, including triggers, duration, severity, and any accompanying symptoms.\n- Avoid unnecessary repetition; do not ask the same question in different wording.\n- Use a short, clear, simple, and understandable language throughout the conversation.\n- Use a friendly and supportive tone to reduce the user's anxiety\n- Do not attempt to make a medical diagnosis during the conversation; only provide an initial assessment.\n- Do not end the conversation until the user types “exit” or “quit”.\n- At the end of the conversation, remind the user that this is not a medical diagnosis and that consulting a doctor is necessary.\nYour purpose is to provide the user with a valuable preliminary assessment and encourage them to consult a doctor if needed.\n",
            "timestamp": "2025-07-13T11:54:38.615061Z",
            "role": "system"
        },
        {
            "content": "Hello! I have a skin problem.",
            "timestamp": "2025-07-13T11:58:01.172709Z",
            "role": "user"
        },
        {
            "content": "I'm sorry to hear you're having a skin problem.  I can't offer medical advice, so I can't diagnose or treat your issue.  However, I can offer some general information and suggest steps you can take:\n\n* **Describe your symptoms:**  The more detail you can provide (location, appearance, texture, duration, any related symptoms), the better a doctor will be able to understand your situation.  Examples:  \"I have a red, itchy rash on my arm that started three days ago,\" or \"I have a dry, flaky patch on my scalp that's been there for months.\"\n* **See a dermatologist or your primary care doctor:**  They can properly diagnose your skin condition and recommend appropriate treatment.  This is the most important step.\n* **Keep a journal:**  Tracking your skin problem, including when it started, any triggers, and any treatments you try, can be helpful for your doctor.\n* **Avoid self-treating with strong medications or home remedies without consulting a doctor:**  Some treatments can worsen skin problems or interact with other medications.\n* **Over-the-counter options (with caution):** For mild issues like dry skin, you might consider gentle, fragrance-free moisturizers.  For itching, hydrocortisone cream can sometimes provide temporary relief.  However, if symptoms persist or worsen, see a doctor.\n\nRemember, I am not a medical professional.  The information I provide should not be considered medical advice.  Please consult a doctor for diagnosis and treatment.\n",
            "timestamp": "2025-07-13T11:58:07.490241Z",
            "role": "assistant"
        }
    ]
}
```

**HTTP Status:** `200 OK`