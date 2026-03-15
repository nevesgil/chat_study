from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CommentBase(BaseModel):
    comment_text: str


class CommentCreate(CommentBase):
    psr_id: int
    created_by: str | None = None


class CommentUpdate(BaseModel):
    comment_text: str | None = None
    created_by: str | None = None


class CommentResponse(CommentBase):
    id: int
    psr_id: int
    created_by: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
