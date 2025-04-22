import speech_recognition as sr



class SpeechRecognitionUtils:
    
    
    def __init__(self):
        # Initialize recognizer class (for recognizing the speech)
        self.r = sr.Recognizer()
        self.r.energy_threshold = 500
        self.r.pause_threshold = 1

    def recognize_speech(self, device_index=0): 
        # Reading Microphone as source
        # listening the speech and store in audio_text variable
        try:
            with sr.Microphone(device_index=1) as source:
                print("You can start speaking.")
                self.r.adjust_for_ambient_noise(source)
                audio_text = self.r.listen(source) 
                # recoginze_() method will throw a request
                # error if the API is unreachable,
                # hence using exception handling
                
                try:
                    # using google speech recognition
                    # print("Text: "+r.recognize_google(audio_text))
                    result = self.r.recognize_google(audio_text, language="fil-PH") 
                    if result is not None:
                        return result
                except:
                    # print("Sorry, I did not get that")
                    pass
        except AttributeError:
            print("Error: Microphone stream failed to initialize.")
            return None
        except sr.RequestError:
            print("Error: Could not reach the recognition API.")
            return None
        except sr.UnknownValueError:
            print("Error: Unable to recognize speech.")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None