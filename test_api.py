import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

try:
    # Test the API with a simple completion
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Write a haiku about artificial intelligence."}
        ],
        temperature=0.7,
        max_tokens=100
    )
    print("Response:", response.choices[0].message.content)
except Exception as e:
    print("Error:", str(e))
    print("\nAvailable models:")
    try:
        models = client.models.list()
        for model in models.data:
            print(f"- {model.id}")
    except Exception as model_error:
        print("Could not fetch available models:", str(model_error)) 