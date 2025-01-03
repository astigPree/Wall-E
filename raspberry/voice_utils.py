

# Import the required module for text 
# to speech conversion
from gtts import gTTS

# from playsound import playsound
import pygame

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
    
    
    def update_text(self, text : str):
        self.text = text
    
    def update_language(self, language : str):
        self.language = language
    
    def stop_speak(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        time.sleep(1)
    
    def speak(self , text : str):
        # Passing the text and language to the engine, 
        # here we have marked slow=False. Which tells 
        # the module that the converted audio should 
        # have a high speed
        if self.text or text:
            
            
            self.stop_speak()
            
            
            myobj = gTTS(text=self.text if text is None else text, lang=self.language, slow=False)

            # Ensure the file can be overwritten 
            if os.path.exists(self.save_path): 
                os.remove(self.save_path)
            
            # Saving the converted audio in a mp3 file named
            # welcome 
            myobj.save(self.save_path)
            
            # Playing the converted file
            # os.system(f"start {self.save_path}")
            
            # Load the music file 
            pygame.mixer.music.load(self.save_path)
            
            # Play the music 
            pygame.mixer.music.play()
            



