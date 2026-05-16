from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import uvicorn

from services.tts_service import generate_voice_from_script
from services.subtitle_service import generate_subtitles

app = FastAPI(title="Voice & Subtitle Generator")

# Models
class GenerateRequest(BaseModel):
    script: str
    voice: str

# Create required directories
os.makedirs("static/outputs", exist_ok=True)

@app.get("/outputs/{filename}")
async def get_output_file(filename: str):
    file_path = os.path.join("static/outputs", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")

@app.post("/api/generate")
async def generate_content(request: GenerateRequest):
    try:
        # Generate audio
        audio_filename = await generate_voice_from_script(request.script, request.voice)
        
        # Generate subtitles
        subtitle_filename = generate_subtitles(audio_filename)
        
        return {
            "success": True,
            "audio_url": f"/outputs/{audio_filename}",
            "subtitle_url": f"/outputs/{subtitle_filename}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Ensure index.html is served from root
@app.get("/")
def read_root():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"message": "index.html not found"}

# Mount static files for frontend
app.mount("/", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import sys
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
