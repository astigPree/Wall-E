
from g4f.client import Client
from g4f.Provider import RetryProvider, Phind, Liaobots, Free2GPT
import g4f.debug

g4f.debug.logging = True
g4f.debug.version_check = False

import time

rule = """
When generating a text, you should English language but it depends on the user command below if the language is not specified.
Also make the generated text words shorter as necessary but it depends on the user command
when the text is not specified how long it will be.

Command :"""


class BrainUtils:
    
    # client = Client()
    client = Client(
        provider=RetryProvider([Free2GPT, Phind,  Liaobots], shuffle=False)
    )
    # model = "gpt-4o-mini"
    model = ""

    debounce = 2



    async def generate_response(self, text : str):
        """
        Generates a response based on the provided text.
        """
        # while True:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": rule +text}],
            )
            self.debounce = 2 # Reset the delay
            print(f"The response is: {response.choices[0].message.content}")
            return str(response.choices[0].message.content)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(self.debounce)
            self.debounce  = self.debounce * self.debounce
            return await self.generate_response(text)
    
