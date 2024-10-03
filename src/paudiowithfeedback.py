import asyncio
import os
from datetime import datetime
from src.paudio import create_podcast_audio
from src.utils.utils import get_last_timestamp, add_feedback_to_state
from src.utils.textGDwithWeightClipping import optimize_prompt

async def create_podcast_with_feedback(pdf_path, timestamp=None):
    # Get the last timestamp if not provided
    if timestamp is None:
        timestamp = get_last_timestamp()
    
    print(f"Creating podcast using timestamp: {timestamp}")
    
    # Create the podcast audio
    audio_bytes, dialogue_text, new_timestamp = await create_podcast_audio(
        pdf_path,
        timestamp=timestamp,
        summarizer_model="gpt-4o-mini",
        scriptwriter_model="gpt-4o-mini",
        enhancer_model="gpt-4o-mini",
        provider="OpenAI"
    )
    
    print("\nPodcast created successfully!")
    print(f"New timestamp: {new_timestamp}")
    
    # Save the audio file
    os.makedirs(os.path.join(PROJECT_ROOT, "audios"), exist_ok=True)
    audio_filename = os.path.join(PROJECT_ROOT, "audios", f"podcast_{new_timestamp}.mp3")
    with open(audio_filename, "wb") as audio_file:
        audio_file.write(audio_bytes)
    print(f"Audio saved as: {audio_filename}")
    
    # Save the dialogue text
    dialogue_filename = os.path.join(PROJECT_ROOT, "audios", f"dialogue_{new_timestamp}.txt")
    with open(dialogue_filename, "w", encoding="utf-8") as dialogue_file:
        dialogue_file.write(dialogue_text)
    print(f"Dialogue saved as: {dialogue_filename}")
    
    # Print the dialogue
    print("\nGenerated Dialogue:")
    print(dialogue_text)
    
    # Ask for feedback
    want_feedback = input("\nDo you want to provide feedback? (yes/no): ").lower()
    
    if want_feedback == "yes":
        feedback = input("Please provide your feedback: ")
        add_feedback_to_state(new_timestamp, feedback)
        print("Feedback added to the podcast state.")
        
        # Optimize prompts
        print("\nOptimizing prompts based on feedback...")
        optimize_prompt("summarizer", timestamp, new_timestamp, "gpt-4o-mini", "gpt-4o-mini")
        optimize_prompt("scriptwriter", timestamp, new_timestamp, "gpt-4o-mini", "gpt-4o-mini")
        optimize_prompt("enhancer", timestamp, new_timestamp, "gpt-4o-mini", "gpt-4o-mini")
        print("Prompts optimized successfully.")
    else:
        print("No feedback provided. Prompts will not be optimized.")

if __name__ == "__main__":
    pdf_path = input("Enter the path to your PDF file: ")
    asyncio.run(create_podcast_with_feedback(pdf_path))