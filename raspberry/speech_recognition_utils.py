import speech_recognition as sr

class SpeechRecognitionUtils:
    
    def __init__(self):
        self.r = sr.Recognizer()
        self.r.energy_threshold = 500
        self.mic_index = self.get_usable_mic_index()  # Auto-select usable mic
        self.mic_ready = self.test_microphone()  # Test mic once & store result

    def get_usable_mic_index(self):
        """Finds the first available microphone index and returns it."""
        mic_list = sr.Microphone.list_microphone_names()

        if mic_list:
            print(f"Available Microphones: {mic_list}")

            # Automatically select the first valid microphone (skip bcm2835 Headphones)
            for i, mic in enumerate(mic_list):
                if "Headphones" not in mic:  # Avoid speaker output devices
                    print(f"Using Microphone: {mic} (Index {i})")
                    return i  # Return first usable mic index

            print("No valid microphone found.")
            return None


    def test_microphone(self):
        """Tests if the microphone is working once on startup."""
        if self.mic_index is None:
            print("Error: No microphone available.")
            return False

        try:
            with sr.Microphone(device_index=self.mic_index) as source:
                print(f"Testing Microphone: {self.mic_index} ({sr.Microphone.list_microphone_names()[self.mic_index]})")
                self.r.adjust_for_ambient_noise(source)
                print("Say something to test...")
                audio_text = self.r.listen(source, timeout=5)  # Set timeout to avoid indefinite waiting
                print("Microphone is working!")
                return True
        except Exception as e:
            print(f"Microphone test failed: {e}")
            return False

    def recognize_speech(self):
        """Recognizes speech only if the microphone has been successfully tested."""
        if not self.mic_ready:
            print("Skipping recognition due to microphone issue.")
            return None

        try:
            with sr.Microphone(device_index=self.mic_index) as source:
                print(f"Using Microphone: {self.mic_index}")
                self.r.adjust_for_ambient_noise(source)
                print("You can start speaking...")
                audio_text = self.r.listen(source)

                try:
                    result = self.r.recognize_google(audio_text, language="fil-PH") 
                    return result if result else "Unrecognized speech"
                except sr.RequestError:
                    print("Error: Could not reach the recognition API.")
                except sr.UnknownValueError:
                    print("Error: Unable to recognize speech.")
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
