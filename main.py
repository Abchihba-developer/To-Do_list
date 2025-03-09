import uvicorn
from fastapi import FastAPI
from config import settings

app = FastAPI()



if __name__ == "__main__":
    uvicorn.run(app="main:app", host=settings.host, port=settings.port)
