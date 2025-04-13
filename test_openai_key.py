import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def test_openai_key():
    """Test if the OpenAI API key is valid by making a simple API call."""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ Failed: OPENAI_API_KEY environment variable is not set")
        return
    
    # Create OpenAI client with the API key
    client = OpenAI(api_key=api_key)
    
    try:
        # Make a simple API call to test the key
        response = client.models.list()
        print("✅ Success: OpenAI API key is valid")
        print(f"Available models: {', '.join([model.id for model in response.data[:3]])}...")
    except Exception as e:
        error_message = str(e)
        print(f"❌ Failed: {error_message}")

if __name__ == "__main__":
    test_openai_key()
