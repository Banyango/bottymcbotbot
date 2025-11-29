from pydantic import BaseModel, ConfigDict, Field
from pydantic._internal._generate_schema import GenerateSchema
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    """Base schema for all models."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        schema_generator=GenerateSchema,
    )


class PaginatedBaseSchema(BaseSchema):
    total: int = Field(description="Total number of items")
    limit: int = Field(description="Number of items per page")
    offset: int = Field(description="Offset of the current page")
