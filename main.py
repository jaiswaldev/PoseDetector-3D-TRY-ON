from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
from controllers.video_controller import generate_frames
import state  # shared state

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.post("/upload-frame/")
# async def upload_frame(file: UploadFile = File(...)):
#     contents = await file.read()
#     return {"filename": file.filename, "size": len(contents)}

@app.get('/video_feed')
async def video_feed():
    return StreamingResponse(generate_frames(), media_type='multipart/x-mixed-replace; boundary=frame')

@app.get('/stop_feed')
async def stop_feed():
    if state.is_camera_active:
        state.is_camera_active = False
        await asyncio.sleep(0.5)
        if state.camera and state.camera.isOpened():
            state.camera.release()
            print("Camera explicitly released via stop_feed.")
        state.camera = None
    return {"message": "Video feed stop signal sent."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


