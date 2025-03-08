
from g4f.client import Client
from g4f.Provider import RetryProvider, Free2GPT , Pizzagpt
import g4f.debug

import cohere

g4f.debug.logging = True
g4f.debug.version_check = False

import time 
import asyncio


class BrainUtils:
    
    # client = Client()
    client = Client(
        provider=RetryProvider([Pizzagpt , Free2GPT], shuffle=False)
    )
    # model = "gpt-4o-mini"
    model = ""
    
    
    cohere_client = cohere.ClientV2("6KXJUorIR8sWsMs5x6GTjmMDTar57vWvFUKYrakT")

    debounce = 2

    
    def generate_cohere_response(self, command :  str , system : str):
        try:
            
            response = self.cohere_client.chat(
                model="command-r", 
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": command}
                ]
            )
            data = response.dict()
            
            for k in data:
                if k == "message":
                    message: list = data[k]["content"]
                    for mes in message:
                        if isinstance(mes, dict):
                            main_content = mes.get("text") 
                            if main_content:
                                return main_content
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None


    def generate_response(self, command: str):
        """
        Generates a response based on the provided text.
        """
        async def main_generator():
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": command}
                    ],
                )
                self.debounce = 2  # Reset the delay
                return response.choices[0].message.content
            except Exception as e:
                print(f"Error: {e}")
                return None

        # Run the asynchronous generator and capture its result
        generated = asyncio.run(main_generator())
        return generated







