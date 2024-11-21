from fastapi import APIRouter, Depends

from src.dependencies import get_intent_classifier
from src.services.intent_classifier import IntentClassifierService

router = APIRouter()


@router.get("/score")
async def get_intent_score(
    text: str, intent_service: IntentClassifierService = Depends(get_intent_classifier)
):
    result, topics = intent_service.is_text_pertinent(text)
    return {"Is_pertinent": result, "topics": topics}
