from sqlalchemy.orm import Session
from app.db import models
from app.schemas.comments import CommentCreate


def create_comment(db: Session, comment: CommentCreate) -> models.Comment:

    new_comment = models.Comment(
        psr_id=comment.psr_id,
        comment_text=comment.comment_text,
        created_by=comment.created_by,
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


def get_psr_comments(db: Session, psr_id: int) -> list[models.Comment]:
    return db.query(models.Comment).filter(models.Comment.psr_id == psr_id).all()
