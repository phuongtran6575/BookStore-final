from fastapi import FastAPI
from controller.auth_controller import router as auth_router
from controller.book_controller import router as book_router
from controller.category_controller import router as category_router
from controller.publisher_controller import router as publisher_router
from controller.author_controller import router as author_router
from controller.role_controller import router as role_router
from controller.userrole_controller import router as userrole_router
from controller.user_controller import router as user_router
from controller.bookcategory_controller import router as bookcategory_router
from controller.bookauthor_controller import router as bookauthor_router
from controller.bookpublisher_controller import router as bookpublisher_router
from controller.booktag_controller import router as booktag_router
from controller.useraddress_controller import router as useraddress_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello API"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(book_router)
app.include_router(category_router)
app.include_router(publisher_router)
app.include_router(author_router)
app.include_router(role_router)
app.include_router(userrole_router)
app.include_router(user_router)
app.include_router(bookcategory_router)
app.include_router(bookauthor_router)
app.include_router(bookpublisher_router)
app.include_router(booktag_router)
app.include_router(useraddress_router)