from pydantic import BaseModel, Field
from typing import List

class Theme(BaseModel):
    """Theme model"""
    title: str = Field(..., description="Title of the theme")
    description: str = Field(..., description="Description of the theme")

class theme_schema(BaseModel):
    """Theme schema"""
    response: List[Theme] = Field(
        ..., 
        description="List of themes, each with a title and description."
    )
class Character(BaseModel):
    """Character model"""
    title: str = Field(..., description="Name of the character")
    description: str = Field(..., description="Role of the character")

class character_schema(BaseModel):
    """Character schema"""
    response: List[Character] = Field(
        ..., 
        description="List of characters, each with a name and role."
    )

class Options(BaseModel):
    """Options model"""
    title: str = Field(..., description="Title of the decision to make")
    description: str = Field(..., description="Description of the decision to make")

class AdventureSchema(BaseModel):
    """Adventure schema"""
    text: str = Field(..., description="The engaging opening scene text")
    options: List[Options] = Field(..., description="List of decisions to make")

class ResponseSchema(BaseModel):
    """Response schema"""
    response: AdventureSchema = Field(..., description="The adventure response containing opening text and decisions")
