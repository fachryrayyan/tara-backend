from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.models.user import User
from app.core.security import verify_google_token, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

class GoogleLoginRequest(BaseModel):
    id_token: str  # id_token yang didapat dari Google SDK di Frontend

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/google", response_model=TokenResponse)
async def google_login(payload: GoogleLoginRequest):
    # 1. Verifikasi ID Token ke Google
    google_data = verify_google_token(payload.id_token)
    if not google_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Google tidak valid atau kadaluarsa"
        )

    google_id = google_data.get("sub")
    email = google_data.get("email")
    full_name = google_data.get("name")
    avatar = google_data.get("picture")

    # 2. Cek user di DB, jika belum ada otomatis buat baru (Upsert)
    user = await User.find_one(User.google_id == google_id)
    if not user:
        user = User(
            google_id=google_id,
            email=email,
            full_name=full_name,
            avatar=avatar
        )
        await user.insert()

    # 3. Terbitkan JWT Access Token backend
    access_token = create_access_token(data={"sub": user.email, "google_id": user.google_id})
    return {"access_token": access_token, "token_type": "bearer"}