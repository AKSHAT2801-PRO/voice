from faster_whisper import WhisperModel
import os

def format_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds_rem = seconds % 60
    milliseconds = int((seconds_rem - int(seconds_rem)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{int(seconds_rem):02d},{milliseconds:03d}"

def transcribe_audio_to_srt(audio_path, srt_path):
    print("Loading AI Whisper model...")
    # 'base' model is quick and usually accurate for clear speech. 
    model = WhisperModel("base", device="cpu", compute_type="int8")
    
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
            print(f"[{start_time} -> {end_time}] {text}")

if __name__ == "__main__":
    audio_file = "01_SCRIPT_Audio.mp3"
    srt_file = "01_SCRIPT_Audio.srt"
    
    if os.path.exists(audio_file):
        transcribe_audio_to_srt(audio_file, srt_file)
        print(f"Subtitles successfully saved to {srt_file}")
    else:
        print(f"Error: {audio_file} not found.")
