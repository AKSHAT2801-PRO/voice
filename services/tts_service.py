import re
import asyncio
import edge_tts
import uuid
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def generate_voice_from_script(text: str, voice: str) -> str:
    """
    Cleans the script and generates a TTS audio file using edge_tts.
    Returns the relative path to the generated audio file.
    """
    # General cleanup
    text = re.sub(r'\[.*?\]', '', text)  # remove tone brackets
    text = text.replace('**', '').replace('*', '')  # remove bold/italics
    # Removing any custom script headers might be too specific, but we'll try to clean up Markdown titles
    text = re.sub(r'^#.*$', '', text, flags=re.MULTILINE) 
    
    text = re.sub(r'\n\s*\n', '\n\n', text).strip()

    if not text:
        raise ValueError("Script is empty after cleaning.")

    filename = f"{uuid.uuid4().hex}.mp3"
    output_file = os.path.join(OUTPUT_DIR, filename)

    print(f"Generating audio with voice: {voice}")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    print(f"Audio saved to {output_file}")
    
    return filename
