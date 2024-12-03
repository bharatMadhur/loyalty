from fastapi import APIRouter, HTTPException, Depends
from services.campaign_service import CampaignService
from dependencies import get_current_shop_id

router = APIRouter()

@router.post("/")
def create_campaign(campaign_data: dict, store_id: int = Depends(get_current_shop_id)):
    try:
        campaign_data["store_id"] = store_id
        CampaignService.create_campaign(campaign_data)
        return {"message": "Campaign created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{campaign_id}")
def get_campaign(campaign_id: int, store_id: int = Depends(get_current_shop_id)):
    try:
        campaign = CampaignService.get_campaign(campaign_id, store_id)
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found or not authorized.")
        return {"campaign": campaign}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{campaign_id}")
def update_campaign(campaign_id: int, campaign_data: dict, store_id: int = Depends(get_current_shop_id)):
    try:
        campaign_data["store_id"] = store_id
        CampaignService.update_campaign(campaign_data, campaign_id, store_id)
        return {"message": "Campaign updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{campaign_id}")
def delete_campaign(campaign_id: int, store_id: int = Depends(get_current_shop_id)):
    try:
        CampaignService.delete_campaign(campaign_id, store_id)
        return {"message": "Campaign deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))