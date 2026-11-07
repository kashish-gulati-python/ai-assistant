from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.dependencies.auth import get_current_user
from app.models.user import Users
from app.schemas.conversations import (
    ConversationDeleteResponse,
    ConversationDetailResponse,
    ConversationResponse,
    MessageGenerationResponse,
    MessageResponse,
    NewConversationRequest,
    NewConversationResponse,
    NewMessageRequest,
)
from app.services.conversations_service import (
    add_conversation,
    add_message,
    get_all_conversation,
    get_conversation_details,
    get_messages,
    soft_delete_conversation,
)

router = APIRouter(prefix="/conversations", tags=["conversations"])

@router.post("/", response_model=NewConversationResponse, status_code=201)
def user_conversation(request: NewConversationRequest, current_user: Users=Depends(get_current_user), db: Session=Depends(get_db)):
    conversation = add_conversation(db, request, current_user.user_id)
    return NewConversationResponse(
        conversation_id=conversation.conversation_id,
        title=conversation.title,
        created_at=conversation.created_at
    )

@router.get("/", response_model=list[ConversationResponse], status_code=200)
def user_get_all_conversations(current_user: Users=Depends(get_current_user), db: Session=Depends(get_db)):
    return get_all_conversation(db, current_user.user_id)

@router.post("/{conversation_id}/messages/", response_model=MessageGenerationResponse, status_code=201)
def user_message(conversation_id: UUID, request: NewMessageRequest, current_user: Users=Depends(get_current_user), db: Session=Depends(get_db)):
    return add_message(db, request, conversation_id=conversation_id, user_id=current_user.user_id)

@router.get("/{conversation_id}/", response_model=ConversationDetailResponse, status_code=200)
def retrieve_conversation(conversation_id: UUID, current_user: Users=Depends(get_current_user), db: Session=Depends(get_db)):
    return get_conversation_details(conversation_id=conversation_id, db=db, user_id=current_user.user_id)

@router.delete("/{conversation_id}/", response_model=ConversationDeleteResponse, status_code=200)
def delete_user_conversation(conversation_id: UUID, current_user: Users=Depends(get_current_user), db: Session=Depends(get_db)):
    success = soft_delete_conversation(conversation_id=conversation_id, db=db, user_id=current_user.user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return ConversationDeleteResponse(id=conversation_id, deleted=success)

@router.get("/{conversation_id}/messages/", response_model=list[MessageResponse], status_code=200)
def get_message_from_conversation(conversation_id: UUID, current_user: Users=Depends(get_current_user), db: Session=Depends(get_db)):
    return get_messages(db, convesation_id=conversation_id, user_id=current_user.user_id)
