from enum import Enum
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class NewConversationRequest(BaseModel):
	title: str

class NewConversationResponse(BaseModel):
	conversation_id: UUID
	title: str
	created_at: datetime

class ConversationResponse(BaseModel):
	conversation_id: UUID
	title: str
	created_at: datetime

	model_config = ConfigDict(from_attributes=True)

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class NewMessageRequest(BaseModel):
	content: str
<<<<<<< HEAD
=======
	role: str
>>>>>>> 0f270ed18d981bc6d770cb07a8d903005cd46388

class NewMessageResponse(BaseModel):
	message_id: UUID
	role: MessageRole
	content: str
<<<<<<< HEAD
	created_at: datetime

class MessageResponse(NewMessageResponse):
	pass
=======
	created_at: datetime
>>>>>>> 0f270ed18d981bc6d770cb07a8d903005cd46388
