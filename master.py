# import sys
# import os

# # Add the `data_end` directory to the system path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data_end')))

from fastapi import FastAPI
from routers import user_router, store_router, offer_router, campaign_router, transaction_router, feedback_router

app = FastAPI()

# Register all the routes
app.include_router(user_router.router, prefix="/api/users", tags=["Users"])
app.include_router(store_router.router, prefix="/api/stores", tags=["Stores"])
app.include_router(offer_router.router, prefix="/api/offers", tags=["Offers"])
app.include_router(campaign_router.router, prefix="/api/campaigns", tags=["Campaigns"])
app.include_router(transaction_router.router, prefix="/api/transactions", tags=["Transactions"])
app.include_router(feedback_router.router, prefix="/api/feedback", tags=["Feedback"])


