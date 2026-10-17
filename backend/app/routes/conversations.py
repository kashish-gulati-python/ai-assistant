from fastapi import APIRouter, Depends
from app.schemas.conversations import NewConversationResponse, NewConversationRequest, ConversationResponse, ConversationDetailResponse, NewMessageResponse, NewMessageRequest, MessageResponse
from app.services.auth_service import get_current_user
from app.services.conversations_service import add_conversation, get_all_conversation, get_conversation_details, add_message, get_messages
from app.models.user import Users
from app.db.deps import get_db
from sqlalchemy.orm import Session
from uuid import UUID

router = APIRouter(prefix="/conversations", tags=["conversations"])

@router.post("/", response_model=NewConversationResponse, status_code=201)
def user_conversation(request: NewConversationRequest, current_user: Users=Depends(get_current_user), db: Session=Depends(get_db)):
    conversation = add_conversation(db, request, current_user.user_id)
    return NewConversationResponse(
        conversation_id=conversation.conversation_id,
        title=conversation.title,
        created_at=conversation.created_at,
    )

@router.get("/", response_model=list[ConversationResponse], status_code=200)
def user_get_all_conversations(current_user: Users=Depends(get_current_user), db: Session=Depends(get_db)):
    return get_all_conversation(db, current_user.user_id)

@router.post("/{conversation_id}/messages/", response_model=NewMessageResponse, status_code=201)
def user_message(conversation_id: UUID, request: NewMessageRequest, current_user: Users=Depends(get_current_user), db: Session=Depends(get_db)):
    message = add_message(db, request, conversation_id=conversation_id, user_id=current_user.user_id)
    return NewMessageResponse(
        message_id=message.message_id,
        role=message.role,
        content=message.content,
        created_at=message.created_at
    )

@router.get("/{conversation_id}/", response_model=ConversationDetailResponse, status_code=200)
def retrieve_conversation(conversation_id: UUID, current_user: Users=Depends(get_current_user), db: Session=Depends(get_db)):
    return get_conversation_details(conversation_id=conversation_id, db=db, user_id=current_user.user_id)

@router.get("/{conversation_id}/messages/", response_model=list[MessageResponse], status_code=200)
def get_message_from_conversation(conversation_id: UUID, current_user: Users=Depends(get_current_user), db: Session=Depends(get_db)):
    return get_messages(db, convesation_id=conversation_id, user_id=current_user.user_id)
