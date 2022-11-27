from fastapi import FastAPI
from routes import router
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn
import logging

app = FastAPI(title="untitled-chore-api", version="0.1.0")
app.include_router(router)

# app.add_middleware(HTTPSRedirectMiddleware)
# app.add_middleware(TrustedHostMiddleware, allowed_hosts=["our frontend server domain", "localhost"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=80, reload=True)
