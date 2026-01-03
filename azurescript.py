from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables (OPENAI_API_KEY)
load_dotenv()

endpoint = os.getenv("OPENAI_API_ENDPOINT")
deployment_name = "o3-mini"

apiKey = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    base_url=endpoint,
    api_key=apiKey
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