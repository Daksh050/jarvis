# voice_client.py
import speech_recognition as sr
import requests

def listen_to_jarvis():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("\n[🎙️] Adjusting for background noise. Please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("[🟢] J.A.R.V.I.S. is listening. Speak now...")
        
        try:
            # Capture the audio
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
            print("[⚙️] Processing speech...")
            
            # Convert speech to text (Using Google's free STT for speed)
            # To use another language, change 'en-US' to 'hi-IN' for Hindi, etc.
            command_text = recognizer.recognize_google(audio, language="en-US")
            print(f"> You said: '{command_text}'")
            
            # Send the text to your FastAPI backend
            print("[🚀] Executing command...")
            response = requests.post(
                "http://localhost:8000/api/v1/execute",
                json={"command": command_text}
            )
            
            # Print J.A.R.V.I.S.'s reply
            if response.status_code == 200:
                print(f"\n[JARVIS]: {response.json().get('reply')}")
            else:
                print("\n[ERROR]: Failed to connect to backend.")
                
        except sr.WaitTimeoutError:
            print("[!] No speech detected.")
        except sr.UnknownValueError:
            print("[!] Could not understand the audio.")
        except requests.exceptions.ConnectionError:
            print("[!] Backend is offline. Is Uvicorn running on port 8000?")

if __name__ == "__main__":
    # Run in a continuous loop
    while True:
        listen_to_jarvis()
        input("\nPress Enter to speak again or Ctrl+C to quit...") 