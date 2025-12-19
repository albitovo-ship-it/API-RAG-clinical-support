from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.router.router import router

#DEFINIMOS APP
app = FastAPI()

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(router)

@app.get("/")
async def serve_frontend():
    return FileResponse("app/static/index.html")