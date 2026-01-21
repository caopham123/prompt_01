# gemini-3-flash-preview
# To run this code you need to install the following dependencies:
# pip install google-genai
# pip install google-generativeai

import base64
import os
from google import genai
from google.generativeai import types # Nếu dùng SDK cũ
from google.genai import types
from config import GOOGLE_API_KEY

def generate():
  client = genai.Client(
      api_key=GOOGLE_API_KEY,
  )

  model = "gemini-3-flash-preview"
  prompt_text = """Write a short lecture about the ML use cases in healthcare."""
  contents = [
    types.Content(
      role="user",
      parts=[
        types.Part.from_text(text=prompt_text),
      ],
    ),
  ]
  tools = [
    types.Tool(googleSearch=types.GoogleSearch(
    )),
  ]
# Defining the configuration with your requested parameters
  generate_content_config = types.GenerateContentConfig(
    temperature=0.7,       # Controls randomness (0.0 to 2.0)
    top_p=0.95,            # Nucleus sampling
    top_k=40,              # Sample from the top K most likely tokens
    max_output_tokens=4024, # Limit the length of the response
    tools=[types.Tool(google_search=types.GoogleSearch())],
    # If using a "Thinking" model, you would uncomment this:
    # thinking_config=types.ThinkingConfig(include_thoughts=True),
  )

  response = client.models.generate_content(
    model=model,
    contents=contents,
    config=generate_content_config,
  )
  print(response.text)

if __name__ == "__main__":
    generate()
