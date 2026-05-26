# AI Assistant — v0.1

v0.1 scope is: "user can sign up, log in, start a conversation, send messages, and see history"

## Features:
1. User registration
2. User login/logout
3. Create conversation
4. Send message
5. Assistant echoes message
6. View conversation history

## Non Goals:
1. No LLM
2. No file upload
3. No streaming
4. No vector DB
5. No OCR
6. No S3
7. No sharing
8. No realtime updates
9. No email verification

## Core Tables:
### users
id , name, email , password_hash , created_at , updated_at
### conversations
id , user_id , title , created_at , updated_at , deleted_at
### messages
id , conversation_id , role , content , created_at , updated_at , deleted_at

## Core Tables

| users  | conversations | messages |
| ------------- |:-------------:|:-------------:|
| id      | id    | id    |
| name      | user_id     | conversation_id    |
| email      | title     | role    |
| password_hash    | created_at    | content    |
| created_at      | updated_at     | created_at    |
| updated_at      | deleted_at     | updated_at    |
|       |      | deleted_at    |

## Indexes:
- INDEX conversations(user_id)
- INDEX messages(conversation_id)

## Testing Plan:
Backend APIs will be tested using pytest and FastAPI TestClient with integration tests against a PostgreSQL test database.

## API Endpoints:
### POST /auth/register

### Purpose:
Register a new user account.

#### Request Schema:
class RegisterUserRequest(BaseModel):
	name: str
	email: EmailStr
	password: str

#### Response Schema:
class RegisterUserResponse(BaseModel):
	id: UUID
	email: EmailStr
	created_at: datetime

#### Success Response:
200 OK

#### Possible Errors:
409 Conflict -> email already exists
422 Validation Error -> invalid request schema
500 Internal Server Error

------------------------------------------------------

### POST /auth/login

### Purpose:
Login existing user account.

### Request Schema:
class LoginUserRequest(BaseModel):
	email: EmailStr
	password: str

### Response Schema:
class LoginUserResponse(BaseModel):
	access_token: str
	token_type: str = "Bearer"

### Success Response:
200 OK

### Possible Errors:
401 Unauthorized -> invalid credentials
422 Validation Error

------------------------------------------------------

### POST /auth/logout

### Purpose:
Logout current user account.

### Response Schema:
class LogoutUserResponse(BaseModel):
	success: bool
	message: str

### Success Response:
200 OK

### Possible Errors:
401 Unauthorized -> token expired
403 Validation Error
404 Not Found -> user not found

------------------------------------------------------

### GET /auth/me

### Purpose:
Retrieves the currently authenticated user's profile.

### Headers:
Authorization: Bearer <access_token>
Accept: application/json

### Response Schema:
class MeResponse(BaseModel):
	id: UUID
	name: str
	email: EmailStr
	name: str
	created_at: datetime

### Success Response:
200 OK

### Possible Errors:
401 Unauthorized -> token expired
422 Validation Error
404 Not Found -> user not found

------------------------------------------------------

### POST /conversations

### Purpose:
Create a new conversation

### Request Schema:
class NewConversationRequest(BaseModel):
	title: str

### Response Schema:
class NewConversationResponse(BaseModel):
	id: UUID
	title: str
	created_at: datetime

### Success Response:
200 OK

### Possible Errors:
401 Unauthorized -> token expired, invalid creds
422 Validation Error

------------------------------------------------------

### Conversations API Contract:
GET /conversations

### Purpose:
Retrieves the list of chat

### Response Schema:
class ConversationResponse(BaseModel):
	id: UUID
	title: str
	created_at: datetime

### Success Response:
200 OK

### Possible Errors:
401 Unauthorized -> token expired, invalid creds
422 Validation Error

------------------------------------------------------

### POST /conversations/{id}/messages

### Purpose:
Add a message inside an existing conversation.

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

### Request Schema:
class NewMessageRequest(BaseModel):
	content: str

### Response Schema:
class NewMessageResponse(BaseModel):
	id: UUID
	role: MessageRole
	content: str
	created_at: datetime

### Success Response:
200 OK

### Possible Errors:
401 Unauthorized -> token expired, invalid creds
404 Not Found -> Conversation doesn't exist.
422 Validation Error -> Empty/invalid request body.

------------------------------------------------------

### GET /conversations/{id}/messages

### Purpose:
Gets the message from conversation

### Response Schema:
class MessageResponse(NewMessageResponse):
	pass

### Success Response:
200 OK

### Possible Errors:
401 Unauthorized -> token expired, invalid creds
404 Not Found -> Conversation doesn't exist.
422 Validation Error -> Empty/invalid request body.

------------------------------------------------------

### GET /conversations/{id}

### Purpose:
Retrieves the details and current state of a specified conversation.

### Headers:
Authorization: Bearer <access_token>
Accept: application/json

### Response Schema:
class ConversationDetailResponse(BaseModel):
	id: UUID
	role: MessageRole
	content: str
	created_at: datetime

### Success Response:
200 OK

### Possible Errors:
401 Unauthorized -> token expired, invalid creds
404 Not Found -> Conversation doesn't exist.
422 Validation Error -> Empty/invalid request body.

------------------------------------------------------

### DELETE /conversations/{id}

### Purpose:
Deletes the details and current state of a specified conversation.

### Response Schema:
class ConversationDeleteResponse(BaseModel):
	id: UUID
	deleted: bool

### Success Response:
204 No Content

Possible Errors:
401 Unauthorized -> token expired, invalid creds
404 Not Found -> Conversation doesn't exist.
