import time
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from .database import engine, Base
from .routes import books, reviews, websockets

def wait_for_db():
    """
    Nawiązuje połaczenie z bazą danych do momentu jej poprawnego utworzenia.
    Przydatne przy uruchamianiu aplikacji w kontenerze Docker.
    """
    retries = 20
    while retries > 0:
        try:
            Base.metadata.create_all(bind=engine)
            print("Database connected.")
            return
        except Exception as e:
            print(f"Waiting for DB... {e}")
            retries -= 1
            time.sleep(10)

wait_for_db()

app = FastAPI(title="Book Grading App")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Globalny filtr wyjątków do modyfikacji domyślnego formatu błedu zwracanego w przypadku błedów walidacji pydantic
    """
    first_error = exc.errors()[0]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": first_error["type"],
            "field": first_error["loc"][-1],
            "message": first_error["msg"]
        }
    )

origins = [
    "http://localhost:5173",
    "http://localhost:80",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router)
app.include_router(reviews.router)
app.include_router(websockets.router)