from dotenv import load_dotenv
load_dotenv(override=True)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bin.routers import user_router,admin_router


import uvicorn

app = FastAPI(
    title="Holy Land",
    contact={
        "name": "chamindika Kodithuwakku",
        "email": "chamindika1996@gmail.com",
    },
    root_path="/api/",
    root_path_in_servers=True
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)
app.include_router(user_router.router)
app.include_router(admin_router.router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, workers=1, reload=False)







