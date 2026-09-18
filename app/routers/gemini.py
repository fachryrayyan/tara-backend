import os
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from google import genai
from app.core.deps import get_current_user
from app.models.user import User
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    prefix="/ai",
    tags=["Gemini AI"]
)

# Inisialisasi Gemini Client menggunakan API Key dari .env
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Skema Request Body
class PromptRequest(BaseModel):
    prompt: str

@router.post("/chat")
async def chat_with_gemini(
    request: PromptRequest,
    current_user: User = Depends(get_current_user) # Terproteksi dengan JWT Login Google
):
    """
    Endpoint untuk berinteraksi dengan Gemini AI (Membutuhkan Login)
    """
    try:
        # Memanggil model Gemini terbaru (gemini-2.5-flash cocok untuk teks & cepat)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=request.prompt,
        )
        return {
            "status": "success",
            "prompt": request.prompt,
            "response": response.text
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gagal memproses prompt ke Gemini API: {str(e)}"
        )