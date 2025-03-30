"""
Crypto Toolkit - A comprehensive educational platform for cryptocurrencies
Copyright (c) 2025 xPOURY4
MIT License
"""

from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, users, categories, items, bookmarks, notifications, statistics

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(bookmarks.router, prefix="/bookmarks", tags=["bookmarks"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(statistics.router, prefix="/statistics", tags=["statistics"]) 