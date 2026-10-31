from enum import Enum
from pydantic import BaseModel, ConfigDict, Field
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
	content: str = Field(
        ...,
        min_length=1,
        description="Message content cannot be empty",
    )
	
	model_config = ConfigDict(str_strip_whitespace=True)

class NewMessageResponse(BaseModel):
	message_id: UUID
	role: MessageRole
	content: str
	created_at: datetime

class MessageResponse(NewMessageResponse):
	model_config = ConfigDict(from_attributes=True)

class GenerationStatus(str, Enum):
	COMPLETED = "completed"
	FAILED = "failed"
	PENDING = "pending"

class ErrorDetail(BaseModel):
	code: str
	message: str

class MessageGenerationResponse(BaseModel):
	user_message: MessageResponse
	assistant_message: MessageResponse | None = None
	generation_status: GenerationStatus
	error: ErrorDetail | None = None

	model_config = ConfigDict(from_attributes=True)

