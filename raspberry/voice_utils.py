

# Import the required module for text 
# to speech conversion
from gtts import gTTS
import pyttsx3

# from playsound import playsound
import pygame
from pygame import mixer
from playsound import playsound

# This module is imported so that we can 
# play the converted audio
import os
import time


# Initialize the mixer module 
pygame.mixer.init()

class VoiceUtils:
    
    # The text that you want to convert to audio
    text = None
    
    # Language in which you want to convert
    language = 'en'

    save_path = "speech.mp3"
    
    is_playing = False # True if we are playing from the current position in the file
    
    def __init__(self):
        self.engine = pyttsx3.init()

        # Get the available voices and set a male voice
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if "male" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        self.engine.setProperty('volume', 0.6)  # Lower volume for gentler voice
        self.engine.setProperty('rate', 120)  # Slower speech rate for smoother delivery
    
    def update_text(self, text : str):
        self.text = text
    
    def update_language(self, language : str):
        self.language = language
    
    def stop_speak(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        time.sleep(1)
    
    def speak(self, text: str):
        print("Speaking ...")
        if text:
            # Wait if audio is already playing
            while self.is_playing:
                time.sleep(0.1)
            
            self.is_playing = True

            # Generate speech using pyttsx3 (Replaces gTTS)
            self.engine.say(text)
            self.engine.runAndWait()

            self.is_playing = False
            print("Done Speaking ...")
        
    # def speak(self, text: str):
    #     print("Speaking ...")
    #     if text:
    #         # Wait if audio is already playing
    #         while self.is_playing:
    #             time.sleep(0.1)
            
    #         self.is_playing = True

    #         # Generate speech using gTTS
    #         myobj = gTTS(text=text, lang=self.language, slow=False)

    #         # Ensure the file can be overwritten
    #         if os.path.exists(self.save_path):
    #             os.remove(self.save_path)

    #         # Save the generated audio to the file
    #         myobj.save(self.save_path)

    #         # Try to play the audio using playsound
    #         try:
    #             time.sleep(0.1)
    #             playsound(self.save_path)
    #         except Exception as e:
    #             print(f"Error playing audio with playsound: {e}")
    #             print("Falling back to pygame...")

    #             # Fallback to pygame
    #             try:
    #                 mixer.init()
    #                 mixer.music.load(self.save_path)
    #                 mixer.music.play()

    #                 # Wait while the audio is playing
    #                 while mixer.music.get_busy():
    #                     time.sleep(0.1)
    #             except Exception as pygame_error:
    #                 print(f"Error playing audio with pygame: {pygame_error}")
    #             finally:
    #                 # Clean up pygame
    #                 mixer.quit()

    #         self.is_playing = False
    #         print("Done Speaking ...")
            
    
    # def speak(self , text : str):
    #     # Passing the text and language to the engine, 
    #     # here we have marked slow=False. Which tells 
    #     # the module that the converted audio should 
    #     # have a high speed
    #     if self.text or text:
            
            
    #         self.stop_speak()
            
            
    #         myobj = gTTS(text=self.text if text is None else text, lang=self.language, slow=False)

    #         # Ensure the file can be overwritten 
    #         if os.path.exists(self.save_path): 
    #             os.remove(self.save_path)
            
    #         # Saving the converted audio in a mp3 file named
    #         # welcome 
    #         myobj.save(self.save_path)
            
    #         # Playing the converted file
    #         # os.system(f"start {self.save_path}")
            
    #         # Load the music file 
    #         pygame.mixer.music.load(self.save_path)
            
    #         # Play the music 
    #         pygame.mixer.music.play()
            



