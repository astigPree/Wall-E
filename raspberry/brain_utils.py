
# from g4f.client import Client
# from g4f.Provider import RetryProvider, Free2GPT , Pizzagpt
# import g4f.debug

import cohere

# g4f.debug.logging = True
# g4f.debug.version_check = False

import time 
import asyncio 

class BrainUtils:
    
    # client = Client()
    # client = Client(
    #     provider=RetryProvider([Pizzagpt , Free2GPT], shuffle=False)
    # )
    # model = "gpt-4o-mini"
    model = ""
    
    
    cohere_client = cohere.ClientV2("VH6wyVMc8xw3qFCV9JJDA2YJnvc21mXRtNPMGYG3")

    debounce = 2

    
    def generate_cohere_response(self, command :  str , system : str):
        try:
            if system:
                response = self.cohere_client.chat(
                    model="command-r", 
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": command}
                    ]
                )
            else:
                response = self.cohere_client.chat(
                    model="command-r", 
                    messages=[
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


    # def generate_response(self, command: str):
    #     """
    #     Generates a response based on the provided text.
    #     """
    #     async def main_generator():
    #         try:
    #             response = self.client.chat.completions.create(
    #                 model=self.model,
    #                 messages=[
    #                     {"role": "user", "content": command}
    #                 ],
    #             )
    #             self.debounce = 2  # Reset the delay
    #             return response.choices[0].message.content
    #         except Exception as e:
    #             print(f"Error: {e}")
    #             return None

    #     loop = asyncio.get_event_loop()
    #     if loop.is_running():
    #         # Schedule the coroutine and wait for the result
    #         return loop.run_until_complete(main_generator())
    #     else:
    #         return asyncio.run(main_generator())








