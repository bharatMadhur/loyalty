from fastapi import APIRouter, HTTPException, Depends
from services.store_service import StoreService
from auth import master_login_required

router = APIRouter()

@router.post("/", dependencies=[Depends(master_login_required)])
def create_store(store_data: dict):
    try:
        StoreService.create_store(store_data)
        return {"message": "Store created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{store_id}")
def get_store(store_id: int):
    try:
        store = StoreService.get_store(store_id)
        if not store:
            raise HTTPException(status_code=404, detail="Store not found.")
        return {"store": store}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{store_id}", dependencies=[Depends(master_login_required)])
def update_store(store_id: int, store_data: dict):
    try:
        StoreService.update_store(store_data, store_id)
        return {"message": "Store updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{store_id}", dependencies=[Depends(master_login_required)])
def delete_store(store_id: int):
    try:
        StoreService.delete_store(store_id)
        return {"message": "Store deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))