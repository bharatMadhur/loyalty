from fastapi import APIRouter, HTTPException, Depends
from services.offer_service import OfferService
from dependencies import get_current_shop_id

router = APIRouter()

@router.post("/")
def create_offer(offer_data: dict, store_id: int = Depends(get_current_shop_id)):
    try:
        offer_data["store_id"] = store_id
        OfferService.create_offer(offer_data)
        return {"message": "Offer created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{offer_id}")
def get_offer(offer_id: int, store_id: int = Depends(get_current_shop_id)):
    try:
        offer = OfferService.get_offer(offer_id, store_id)
        if not offer:
            raise HTTPException(status_code=404, detail="Offer not found or not authorized.")
        return {"offer": offer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{offer_id}")
def update_offer(offer_id: int, offer_data: dict, store_id: int = Depends(get_current_shop_id)):
    try:
        offer_data["store_id"] = store_id
        OfferService.update_offer(offer_data, offer_id, store_id)
        return {"message": "Offer updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{offer_id}")
def delete_offer(offer_id: int, store_id: int = Depends(get_current_shop_id)):
    try:
        OfferService.delete_offer(offer_id, store_id)
        return {"message": "Offer deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))