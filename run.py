import uvicorn
from app.core.config import APP_HOST, APP_PORT, APP_DEBUG

if __name__ == "__main__":
    uvicorn.run("app.main:api", host=APP_HOST, port=APP_PORT, reload=APP_DEBUG)
