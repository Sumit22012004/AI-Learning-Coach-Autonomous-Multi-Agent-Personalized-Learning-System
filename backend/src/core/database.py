from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from src.core.config import settings

# Import models here
# from src.domain.models.user import User

async def init_db():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    database = client[settings.DATABASE_NAME]
    
    # Initialize Beanie with document models
    await init_beanie(
        database=database,
        document_models=[
            # User,
            # Curriculum,
            # Task,
            # Submission
        ]
    )
