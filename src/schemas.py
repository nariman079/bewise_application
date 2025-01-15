from pydantic import BaseModel


class ApplicationCreateSchema(BaseModel):
    user_name: str
    description: str


class ApplicationFilterSchema(BaseModel):
    user_name: str | None = None
    description: str | None = None


class ApplicationDisplaySchema(ApplicationCreateSchema):
    id: int
