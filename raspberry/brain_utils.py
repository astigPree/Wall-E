
from g4f.client import Client
from g4f.Provider import RetryProvider, Free2GPT , Pizzagpt
import g4f.debug

g4f.debug.logging = True
g4f.debug.version_check = False

import time



class BrainUtils:
    
    client = Client()
    # client = Client(
    #     provider=RetryProvider([Pizzagpt , Free2GPT], shuffle=False)
    # )
    model = "gpt-4o-mini"
    model = ""

    debounce = 2



    async def generate_response(self, command : str):
        """
        Generates a response based on the provided text.
        """
        # while True:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": command}],
            )
            self.debounce = 2 # Reset the delay
            # print(f"The response is: {response.choices[0].message.content}")
            return str(response.choices[0].message.content)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(self.debounce)
            self.debounce  = self.debounce * self.debounce
            return await self.generate_response(command)
    







