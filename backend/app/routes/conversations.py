from fastapi import APIRouter, Depends
from app.schemas.conversations import NewConversationResponse, NewConversationRequest
from app.services.auth_service import get_current_user
from app.models.user import Users
from app.db.deps import get_db
from sqlalchemy.orm import Session
from app.services.conversations_service import add_conversation

router = APIRouter(prefix="/conversations", tags=["conversations"])

@router.post("/", response_model=NewConversationResponse, status_code=201)
def user_conversation(request: NewConversationRequest, current_user: Users=Depends(get_current_user), db: Session=Depends(get_db)):
    conversation = add_conversation(db, request, current_user.user_id)
    return NewConversationResponse(
        conversation_id=conversation.conversation_id,
        title=conversation.title,
        created_at=conversation.created_at,
    )