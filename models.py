import datetime
import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from backend.database import Base


def _utc_now():
    return datetime.datetime.now(datetime.timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=_utc_now)
    updated_at = Column(DateTime, default=_utc_now, onupdate=_utc_now)

    # Relationship to conversations
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan", order_by="desc(Conversation.updated_at)")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), default="New Financial Conversation", nullable=False)
    created_at = Column(DateTime, default=_utc_now)
    updated_at = Column(DateTime, default=_utc_now, onupdate=_utc_now)

    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at")


class Message(Base):
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String(36), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # "user" or "assistant" or "system"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=_utc_now)

    conversation = relationship("Conversation", back_populates="messages")


class PublicResource(Base):
    __tablename__ = "public_resources"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False, index=True)  # Banking, Insurance, Pension, Micro-loans, Safety & Helplines
    description = Column(Text, nullable=False)
    eligibility = Column(Text, nullable=True)
    official_url = Column(String(500), nullable=True)
    helpline = Column(String(100), nullable=True)
    verified = Column(Boolean, default=True)
    created_at = Column(DateTime, default=_utc_now)
