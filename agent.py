from fastapi import FastAPI
from dotenv import load_dotenv
from branding_os.agents.imagyn import router as imagyn_router

load_dotenv()

app = FastAPI()
app.include_router(imagyn_router)
