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
	deleted_at: datetime | None

	model_config = ConfigDict(from_attributes=True)

class ConversationDetailResponse(BaseModel):
    conversation_id: UUID
    title: str
    created_at: datetime
    updated_at: datetime

class ConversationDeleteResponse(BaseModel):
	id: UUID
	deleted: bool

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class NewMessageRequest(BaseModel):
	content: str

class NewMessageResponse(BaseModel):
	message_id: UUID
	role: MessageRole
	content: str
	created_at: datetime

class MessageResponse(NewMessageResponse):
	model_config = ConfigDict(from_attributes=True)
