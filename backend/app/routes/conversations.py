from fastapi import APIRouter, Depends
<<<<<<< HEAD
from app.schemas.conversations import NewConversationResponse, NewConversationRequest, ConversationResponse, NewMessageResponse, NewMessageRequest, MessageResponse
=======
from app.schemas.conversations import NewConversationResponse, NewConversationRequest, ConversationResponse, NewMessageResponse, NewMessageRequest
>>>>>>> 0f270ed18d981bc6d770cb07a8d903005cd46388
from app.services.auth_service import get_current_user
from app.services.conversations_service import add_conversation, get_all_conversation, add_message, get_messages
from app.models.user import Users
from app.db.deps import get_db
from sqlalchemy.orm import Session
<<<<<<< HEAD
=======
from app.services.conversations_service import add_conversation, get_all_conversation, add_message
>>>>>>> 0f270ed18d981bc6d770cb07a8d903005cd46388
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
    conversations_list = get_all_conversation(db, current_user.user_id)
    all_conversations = []
    for record in conversations_list:
        conversation = ConversationResponse(conversation_id=record.conversation_id, title=record.title, created_at=record.created_at)
        all_conversations.append(conversation)
    return all_conversations

@router.post("/{conversation_id}/messages/", response_model=NewMessageResponse, status_code=201)
def user_message(conversation_id: UUID, request: NewMessageRequest, current_user: Users=Depends(get_current_user), db: Session=Depends(get_db)):
    message = add_message(db, request, conversation_id=conversation_id, user_id=current_user.user_id)
    return NewMessageResponse(
        message_id=message.message_id,
        role=message.role,
        content=message.content,
        created_at=message.created_at
<<<<<<< HEAD
    )

@router.get("/{conversation_id}/messages/", response_model=list[MessageResponse], status_code=200)
def get_message_from_conversation(conversation_id: UUID, current_user: Users=Depends(get_current_user), db: Session=Depends(get_db)):
    messages = get_messages(db, convesation_id=conversation_id, user_id=current_user.user_id)
    all_messages = []
    for message in messages:
        message = MessageResponse(message_id=message.message_id, role=message.role, content=message.content, created_at=message.created_at)
        all_messages.append(message)
    return all_messages
=======
    )
>>>>>>> 0f270ed18d981bc6d770cb07a8d903005cd46388
