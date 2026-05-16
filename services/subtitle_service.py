import os
import uuid
from faster_whisper import WhisperModel

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load the model once to save time on subsequent requests
print("Loading AI Whisper model...")
model = WhisperModel("base", device="cpu", compute_type="int8", download_root=OUTPUT_DIR)

def format_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds_rem = seconds % 60
    milliseconds = int((seconds_rem - int(seconds_rem)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{int(seconds_rem):02d},{milliseconds:03d}"

def generate_subtitles(audio_filename: str) -> str:
    """
    Generates subtitles for a given audio file.
    Returns the relative path to the generated .srt file.
    """
    audio_path = os.path.join(OUTPUT_DIR, audio_filename)
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    filename_without_ext = os.path.splitext(audio_filename)[0]
    srt_filename = f"{filename_without_ext}.srt"
    srt_path = os.path.join(OUTPUT_DIR, srt_filename)

    print(f"Transcribing {audio_path}...")
    segments, info = model.transcribe(audio_path, beam_size=5)
    
    with open(srt_path, "w", encoding="utf-8") as srt_file:
        for i, segment in enumerate(segments, start=1):
            start_time = format_timestamp(segment.start)
            end_time = format_timestamp(segment.end)
            text = segment.text.strip()
            
            srt_file.write(f"{i}\n")
            srt_file.write(f"{start_time} --> {end_time}\n")
            srt_file.write(f"{text}\n\n")
            
    print(f"Subtitles successfully saved to {srt_path}")
    return srt_filename
