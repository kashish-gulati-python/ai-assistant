from sqlalchemy.orm import Session
from app.schemas.conversations import NewConversationRequest, NewMessageRequest
from app.models.conversations import Conversations, Messages
from fastapi import HTTPException

def add_conversation(db: Session, request: NewConversationRequest, user_id):
    conversation = Conversations(user_id=user_id, title=request.title)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

def get_all_conversation(db: Session, user_id):
    return db.query(Conversations).filter(Conversations.user_id==user_id).all()

def add_message(db: Session, request: NewMessageRequest, conversation_id, user_id):
    conversation = db.query(Conversations).filter(Conversations.conversation_id==conversation_id, Conversations.user_id==user_id).first()
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    message = Messages(conversation_id=conversation_id, role="user", content=request.content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message
<<<<<<< HEAD

def get_messages(db: Session, convesation_id, user_id):
    print(db.query(Messages).join(Conversations, Messages.conversation_id==Conversations.conversation_id).\
                filter(Conversations.conversation_id==convesation_id, Conversations.user_id==user_id).all())
    return db.query(Messages).join(Conversations, Messages.conversation_id==Conversations.conversation_id).\
                filter(Conversations.conversation_id==convesation_id, Conversations.user_id==user_id).all()
=======
>>>>>>> 0f270ed18d981bc6d770cb07a8d903005cd46388
