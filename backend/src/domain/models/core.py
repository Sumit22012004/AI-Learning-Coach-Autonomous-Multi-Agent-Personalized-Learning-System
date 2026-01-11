from datetime import datetime
from typing import List, Dict, Optional, Any
from uuid import UUID, uuid4
from beanie import Document, Indexed
from pydantic import BaseModel, Field

class SkillProfile(BaseModel):
    skills: Dict[str, int] = Field(default_factory=dict) # e.g., {"python": 5, "sql": 2}
    last_updated: datetime = Field(default_factory=datetime.utcnow)

class User(Document):
    email: Indexed(str, unique=True)
    full_name: str
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    skill_profile: SkillProfile = Field(default_factory=SkillProfile)

    class Settings:
        name = "users"

class Module(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    description: str
    order_index: int
    status: str = "pending" # 'pending', 'in_progress', 'completed'
    topics: List[str] = Field(default_factory=list)

class Curriculum(Document):
    user_id: str  # Reference to User ID
    goal: str
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    modules: List[Module] = Field(default_factory=list)

    class Settings:
        name = "curriculums"

class Task(Document):
    module_id: str
    user_id: str
    type: str # 'quiz', 'code', 'reading'
    content: Dict[str, Any] # { "question": "...", "options": [...] }
    solution: Dict[str, Any]
    generated_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "tasks"

class Submission(Document):
    task_id: str
    user_id: str
    user_input: str
    agent_feedback: str
    score: int
    submitted_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "submissions"
