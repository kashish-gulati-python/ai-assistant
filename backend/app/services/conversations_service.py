from datetime import UTC, datetime

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.conversations import Conversations, Messages
from app.schemas.conversations import (
    ErrorDetail,
    GenerationStatus,
    MessageGenerationResponse,
    NewConversationRequest,
    NewMessageRequest,
)


def add_conversation(db: Session, request: NewConversationRequest, user_id):
    conversation = Conversations(user_id=user_id, title=request.title)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

def get_all_conversation(db: Session, user_id):
    return db.query(Conversations).filter(Conversations.user_id==user_id).all()

def get_conversation_details(db: Session, conversation_id, user_id):
    return db.query(Conversations).filter(Conversations.conversation_id==conversation_id, Conversations.user_id==user_id, Conversations.deleted_at.is_(None)).first()

def soft_delete_conversation(db: Session, conversation_id, user_id) -> bool:
    now = datetime.now(UTC)
    conversation = db.query(Conversations).filter(Conversations.conversation_id==conversation_id, Conversations.user_id==user_id, Conversations.deleted_at.is_(None)).first()
    if conversation is None:
            raise HTTPException(status_code=404, detail="Conversation not found")
    conversation.deleted_at = now

    db.query(Messages).filter(Messages.conversation_id == conversation_id, Messages.deleted_at.is_(None)).\
            update({Messages.deleted_at: now}, synchronize_session=False)
    db.commit()
    return True

def echo_message(user_message: str) -> str:
    return f"Echo: {user_message}"

def add_message(db: Session, request: NewMessageRequest, conversation_id, user_id):
    conversation = db.query(Conversations).filter(Conversations.conversation_id==conversation_id, Conversations.user_id==user_id,
                                                  Conversations.deleted_at.is_(None)).first()
    # Validate conversation exists and is not soft-deleted
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    user_message = Messages(conversation_id=conversation_id, role="user", content=request.content)
    # Insert User Message (Situation: If this fails, entire request fails)
    try:
        db.add(user_message)
        db.commit()
        db.refresh(user_message)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to save user message") from e
    
    # Generate Echo Message (Situation: Echo fails)
    reply_content = echo_message(request.content)

    # Insert Assistant Message (Situation: DB insert fails)
    assistant_message = Messages(conversation_id=conversation_id, role="assistant", content=reply_content)
    try:
        db.add(assistant_message)
        db.commit()
        db.refresh(assistant_message)
    except SQLAlchemyError:
        db.rollback()
        return MessageGenerationResponse(user_message=user_message, assistant_message=None, generation_status=GenerationStatus.FAILED,
            error=ErrorDetail(code="ASSISTANT_PERSISTENCE_FAILED", message="Failed to persist assistant response."))

    # Success (Situation: Echo succeeds)
    return MessageGenerationResponse(user_message=user_message, assistant_message=assistant_message, generation_status=GenerationStatus.COMPLETED,
            error=None,
    )

def get_messages(db: Session, convesation_id, user_id):
    return db.query(Messages).join(Conversations, Messages.conversation_id==Conversations.conversation_id).\
                filter(Conversations.conversation_id==convesation_id, Conversations.user_id==user_id, Messages.deleted_at.is_(None)).all()
