from fastapi import APIRouter, HTTPException, Depends
from services.transaction_service import TransactionService
from dependencies import get_current_shop_id

router = APIRouter()

@router.post("/")
def create_transaction(transaction_data: dict, store_id: int = Depends(get_current_shop_id)):
    try:
        transaction_data["store_id"] = store_id
        TransactionService.create_transaction(transaction_data)
        return {"message": "Transaction created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{transaction_id}")
def get_transaction(transaction_id: int, store_id: int = Depends(get_current_shop_id)):
    try:
        transaction = TransactionService.get_transaction(transaction_id, store_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found or not authorized.")
        return {"transaction": transaction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{transaction_id}")
def update_transaction(transaction_id: int, transaction_data: dict, store_id: int = Depends(get_current_shop_id)):
    try:
        transaction_data["store_id"] = store_id
        TransactionService.update_transaction(transaction_data, transaction_id, store_id)
        return {"message": "Transaction updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, store_id: int = Depends(get_current_shop_id)):
    try:
        TransactionService.delete_transaction(transaction_id, store_id)
        return {"message": "Transaction deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))