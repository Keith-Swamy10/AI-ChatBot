from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables (OPENAI_API_KEY)
load_dotenv()

endpoint = "https://keithopenaitokens.openai.azure.com/openai/v1"
deployment_name = "o3-mini"

client = OpenAI(
    base_url=endpoint,
    api_key=os.getenv("OPENAI_API_KEY")
)

completion = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {
            "role": "user",
            "content": "What is the cpital of Sri lanka?",
        }
    ],
)

print(completion.choices[0].message)