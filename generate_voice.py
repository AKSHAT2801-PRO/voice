import re
import subprocess
import asyncio
import edge_tts

async def main():
    # Read the script
    with open('cleaned_script.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    # Clean the text:
    # 1. Remove the [Tone: ...] tags and bracketed narrator text
    text = re.sub(r'\[.*?\]', '', text)
    # 2. Remove markdown bold/italics
    text = text.replace('**', '').replace('*', '')
    # 3. Remove the initial title lines
    text = re.sub(r'# Voice Direction: Donald Trump Biographical Script.*?(Everything about)', r'\1', text, flags=re.DOTALL)
    
    # Clean up excess whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text).strip()

    # Voice to use (American Male)
    voice = 'en-US-GuyNeural'
    output_file = 'voice_output.mp3'

    print(f"Generating audio with voice: {voice}")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    print(f"Audio saved to {output_file}")

if __name__ == "__main__":
    asyncio.run(main())
