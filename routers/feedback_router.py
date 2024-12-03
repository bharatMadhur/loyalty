from fastapi import APIRouter, HTTPException, Depends
from services.feedback_service import FeedbackService
from dependencies import get_current_shop_id

router = APIRouter()

@router.post("/")
def submit_feedback(feedback_data: dict, store_id: int = Depends(get_current_shop_id)):
    try:
        feedback_data["store_id"] = store_id
        FeedbackService.submit_feedback(feedback_data)
        return {"message": "Feedback submitted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{feedback_id}")
def get_feedback(feedback_id: int, store_id: int = Depends(get_current_shop_id)):
    try:
        feedback = FeedbackService.get_feedback(feedback_id, store_id)
        if not feedback:
            raise HTTPException(status_code=404, detail="Feedback not found or not authorized.")
        return {"feedback": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{feedback_id}")
def update_feedback(feedback_id: int, feedback_data: dict, store_id: int = Depends(get_current_shop_id)):
    try:
        feedback_data["store_id"] = store_id
        FeedbackService.update_feedback(feedback_data, feedback_id, store_id)
        return {"message": "Feedback updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{feedback_id}")
def delete_feedback(feedback_id: int, store_id: int = Depends(get_current_shop_id)):
    try:
        FeedbackService.delete_feedback(feedback_id, store_id)
        return {"message": "Feedback deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))