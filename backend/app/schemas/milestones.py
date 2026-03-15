from pydantic import BaseModel, ConfigDict


class MilestoneResponse(BaseModel):
    id: int
    name: str
    milestone_order: int

    model_config = ConfigDict(from_attributes=True)
