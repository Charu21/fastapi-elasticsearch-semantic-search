from fastapi import FastAPI, Depends
import uvicorn
import logging
from dotenv import load_dotenv
from config.logger_config import LoggerConfig
from api.crud_endpoints import router as crud_router
import threading
from dependencies import get_elastic_service, get_embedding_service
import os

load_dotenv()
LoggerConfig.configure_logging()

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logging.basicConfig(level=logging.INFO)
    embedding_service = get_embedding_service()
    threading.Thread(target=embedding_service.load_model).start()
    # if indexing is needed as well then uncomment
    # elastic_service = get_elastic_service()
    # threading.Thread(target=elastic_service.index_all_products).start()
    

@app.on_event("shutdown")
async def shutdown_event():
    logging.info("Shutting down FastAPI application...")

app.include_router(crud_router, prefix="/api")

@app.get("/")
async def home():
    return {"message": "Product Management"}

if __name__ == '__main__':
    app_port = int(os.getenv('APP_PORT', 9090))
    uvicorn.run("app:app", host="127.0.0.1", port=app_port, reload=True)

