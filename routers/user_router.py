from fastapi import APIRouter, HTTPException, Depends
from services.user_service import UserService
from dependencies import get_current_shop_id

router = APIRouter()


@router.post("/")
def create_user(user_data: dict, store_id: int = Depends(get_current_shop_id)):
    try:
        user_data["store_id"] = store_id
        UserService.create_user(user_data)
        return {"message": "User created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}")
def get_user(user_id: int, store_id: int = Depends(get_current_shop_id)):
    try:
        user = UserService.get_user(user_id, store_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found or not authorized.")
        return {"user": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{user_id}")
def update_user(user_id: int, user_data: dict, store_id: int = Depends(get_current_shop_id)):
    try:
        user_data["store_id"] = store_id
        UserService.update_user(user_data, user_id, store_id)
        return {"message": "User updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{user_id}")
def delete_user(user_id: int, store_id: int = Depends(get_current_shop_id)):
    try:
        UserService.soft_delete_user(user_id, store_id)
        return {"message": "User deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))