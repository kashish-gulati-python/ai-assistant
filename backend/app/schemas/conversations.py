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