from sqlalchemy.orm import Session
from app.schemas.conversations import NewConversationRequest
from app.models.conversations import Conversations


def add_conversation(db: Session, request: NewConversationRequest, user_id):
    conversation = Conversations(user_id=user_id, title=request.title)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

def get_all_conversation(db: Session, user_id):
    return db.query(Conversations).filter(Conversations.user_id==user_id).all()