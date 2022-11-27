from fastapi import FastAPI
from routes import router
import uvicorn
import logging

app = FastAPI(title="untitled-chore-api", version="0.1.0")
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8888, reload=True)
