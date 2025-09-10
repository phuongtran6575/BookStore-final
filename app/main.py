from fastapi import FastAPI
from controller.auth_controller import router as auth_router
from controller.book_controller import router as book_router
from controller.category_controller import router as category_router
from controller.publisher_controller import router as publisher_router
from controller.author_controller import router as author_router
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello API"}

app.include_router(auth_router)
app.include_router(book_router)
app.include_router(category_router)
app.include_router(publisher_router)
app.include_router(author_router)