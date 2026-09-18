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

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class PromptRequest(BaseModel):
    prompt: str

@router.post("/chat")
async def chat_with_gemini(
    request: PromptRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint untuk berinteraksi dengan Gemini AI (Membutuhkan Login)
    """
    try:
        # Gunakan gemini-2.5-flash untuk SDK google-genai
        response = client.models.generate_content(
            model="gemini-3.6-flash",
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