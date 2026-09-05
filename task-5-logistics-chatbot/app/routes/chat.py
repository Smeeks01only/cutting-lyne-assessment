from fastapi import APIRouter, HTTPException, status
import logging
from .. import schemas
from ..services.intent_classifier import classify_intent
from ..services.retriever import retriever
from ..services.response_generator import generate_response

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["chat"]
)

@router.get("/health")
def health_check():
    """
    Simple health check endpoint to verify the service is running.
    """
    return {"status": "ok"}

@router.post("/chat", response_model=schemas.ChatResponse)
def process_chat(request: schemas.ChatRequest):
    """
    Accepts a user chat message, classifies intent, retrieves relevant context,
    and returns a structured response.
    """
    try:
        user_message = request.message
        
        # 1. Detect Intent deterministically
        intent_data = classify_intent(user_message)
        intent = intent_data["intent"]
        
        # 2. Retrieve Knowledge (Only for knowledge-based queries)
        retrieval_results = []
        if intent not in ["SHIPMENT_TRACKING", "UNKNOWN"]:
            # Uses the TF-IDF singleton
            retrieval_results = retriever.retrieve(user_message, top_k=1)
            
        # 3. Generate Final Response
        # The generator will seamlessly route tracking queries to the shipment_client internally
        final_response = generate_response(intent_data, retrieval_results, user_message)
        
        return final_response
        
    except Exception as e:
        logger.error(f"Failed to process chat message: {str(e)}")
        # Safe error boundary: never expose internal stack traces to the user
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing the chat message."
        )
