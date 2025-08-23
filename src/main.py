from fastapi import FastAPI
from src.logger_panel.routes import router as logger_router

app = FastAPI()
 
# Routers
app.include_router(logger_router, prefix="", tags=["Logger Panel"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
