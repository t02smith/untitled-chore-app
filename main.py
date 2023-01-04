from fastapi import FastAPI
from routes.root import router
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="Untitled Chore API",
    version="0.1.0",
    description="The official API for untitled-chore-app.",
)
app.include_router(router)

# app.add_middleware(HTTPSRedirectMiddleware)
# app.add_middleware(TrustedHostMiddleware, allowed_hosts=["our frontend server domain", "localhost"])
app.add_middleware(
  CORSMiddleware, 
  allow_origins=["http://localhost:5173"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8056, reload=True)
