from fastapi import APIRouter, status, WebSocket, WebSocketDisconnect, Depends
from typing import List
from app.models.sensor import SensorData
from app.models.user import User
from app.core.deps import get_current_user

router = APIRouter(
    prefix="/sensor",
    tags=["Sensor IoT"]
)

# 1. GET ALL SENSOR DATA (Terproteksi dengan JWT Google Auth)
@router.get("/", response_model=List[SensorData])
async def get_all_sensor_data(current_user: User = Depends(get_current_user)):
    """Mengambil 50 data sensor terbaru (Membutuhkan Login)"""
    return await SensorData.find_all().sort("-created_at").limit(50).to_list()


# 2. POST SENSOR DATA (Untuk testing manual / HTTP client)
@router.post("/", response_model=SensorData, status_code=status.HTTP_201_CREATED)
async def create_sensor_data(data: SensorData):
    """Menyimpan data sensor manual ke MongoDB Atlas"""
    await data.insert()
    return data


# 3. WEBSOCKET CONNECTION MANAGER
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()


# 4. WEBSOCKET ENDPOINT (Real-time telemetry)
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Menjaga koneksi tetap live
    except WebSocketDisconnect:
        manager.disconnect(websocket)