from openai import OpenAI
from dotenv import load_dotenv
import  os
class DeppSeekIntegration():
    load_dotenv()
    client = OpenAI(base_url = "https://openrouter.ai/api/v1/",api_key= os.getenv("KEY_DEEP_SEEK"))
    def StartChat(self, content):

        chat = self.client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ]
        )
        print(chat.choices[0].message.content)
        return chat.choices[0].message.content