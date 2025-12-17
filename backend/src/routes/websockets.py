import asyncio
from fastapi import APIRouter, WebSocket
from ..database import SessionLocal
from ..services import book_service, review_service

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Endpoint do połączenia z WebSocket który wysyła statystyki z systemu
    """
    await websocket.accept()
    try:
        while True:
            db = SessionLocal()
            try:
                book_count = book_service.count_books(db)
                review_count = review_service.count_reviews(db)

                payload = {
                    "total_books": book_count,
                    "total_reviews": review_count
                }
            finally:
                db.close()

            await websocket.send_json(payload)

            await asyncio.sleep(1)

    except Exception as e:
        print(f"WebSocket disconnected: {e}")