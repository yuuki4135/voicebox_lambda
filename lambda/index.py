from fastapi import FastAPI, HTTPException
from mangum import Mangum
from fastapi.responses import Response
from pydantic import BaseModel
import voicevox_core
from voicevox_core import AccelerationMode, AudioQuery, VoicevoxCore, METAS

app = FastAPI()
# 話者は1:ずんだもん（あまあま）に設定。METAS から話者のリストが確認可能。
SPEAKER_ID = 1
print(METAS)
                
open_jtalk_dict_dir = './open_jtalk_dic_utf_8-1.11'
acceleration_mode = AccelerationMode.AUTO
core = VoicevoxCore(
        acceleration_mode=acceleration_mode, open_jtalk_dict_dir=open_jtalk_dict_dir
    )
core.load_model(SPEAKER_ID)

class TextToSpeechRequest(BaseModel):
    text: str
    speaker: int = 1
    speed_scale: float = 1.5

@app.post("/synthesize")
async def synthesize_speech(request: TextToSpeechRequest):
    voice_data = core.speech_synthesis(
        AudioQuery(text=request.text, speaker=request.speaker, speed_scale=request.speed_scale)
    )
    
    return Response(
        content=voice_data,
        media_type="audio/wav"
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

handler = Mangum(app)
