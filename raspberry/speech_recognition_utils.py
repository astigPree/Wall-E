import speech_recognition as sr



class SpeechRecognitionUtils:
    
        
    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    def recognize_speech(self): 
        # Reading Microphone as source
        # listening the speech and store in audio_text variable
        with sr.Microphone() as source:
            print("You can start speaking.")
            audio_text = self.r.listen(source) 
            # recoginze_() method will throw a request
            # error if the API is unreachable,
            # hence using exception handling
            
            try:
                # using google speech recognition
                # print("Text: "+r.recognize_google(audio_text))
                result = self.r.recognize_google(audio_text) 
                if result is not None:
                    return result
            except:
                # print("Sorry, I did not get that")
                pass

