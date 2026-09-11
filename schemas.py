import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


# Auth Schemas
class UserRegister(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=6, max_length=100)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    email: str
    full_name: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# Chat Schemas
class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1)


class MessageOut(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class ConversationCreate(BaseModel):
    title: Optional[str] = "New Financial Conversation"
    initial_message: Optional[str] = None


class ConversationRename(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)


class ConversationSummary(BaseModel):
    id: str
    title: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    message_count: Optional[int] = 0
    last_message_preview: Optional[str] = None

    class Config:
        from_attributes = True


class ConversationDetail(BaseModel):
    id: str
    title: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    messages: List[MessageOut] = []

    class Config:
        from_attributes = True


# Public Resources Schemas
class PublicResourceOut(BaseModel):
    id: str
    title: str
    category: str
    description: str
    eligibility: Optional[str] = None
    official_url: Optional[str] = None
    helpline: Optional[str] = None
    verified: bool

    class Config:
        from_attributes = True
