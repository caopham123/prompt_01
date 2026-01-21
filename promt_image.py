# gemini-3-flash-preview
# To run this code you need to install the following dependencies:
# pip install google-genai
# pip install google-generativeai

import base64
from io import BytesIO
from PIL import Image 
import os
from google import genai
from google.genai import types
from config import GOOGLE_API_KEY

def img_2_base64(image_path):
  """
  Chuyển đổi hình ảnh từ đường dẫn thành chuỗi base64 sử dụng Pillow.
  """
  try:
    # Mở hình ảnh bằng Pillow
    with Image.open(image_path) as img:
      # Tạo một bộ nhớ đệm (buffer) để lưu dữ liệu nhị phân
      buffered = BytesIO()

      # Lưu ảnh vào buffer.
      # img.format giúp giữ nguyên định dạng gốc (PNG, JPEG, v.v.)
      img.save(buffered, format=img.format)

      # Lấy dữ liệu bytes từ buffer và mã hóa base64
      img_byte = buffered.getvalue()
      img_base64 = base64.b64encode(img_byte).decode("utf-8")

      return img_base64
  except Exception as e:
    return f"Lỗi khi xử lý ảnh: {e}"

def generate():
  client = genai.Client(api_key=GOOGLE_API_KEY)

  model = "gemini-3-flash-preview"
  img = img_2_base64("img1.jpg")
  prompt_text = """Write a short description about the image with maximum 120 words."""

  contents = [prompt_text, img
    # types.Content(
    #   role="user",
    #   parts=[ 
    #     types.Part.from_text(text=prompt_text),
    #     types.Part.from_image_base64(
    #       image_base64=img,
    #       mime_type="image/jpeg",
    #     ),
    #   ],
    # ),
  ]
  tools = [types.Tool(googleSearch=types.GoogleSearch()),]
  
  # Defining the configuration with your requested parameters
  config = types.GenerateContentConfig(
    temperature=0.7,       # Controls randomness (0.0 to 2.0)
    top_p=0.95,            # Nucleus sampling
    top_k=40,              # Sample from the top K most likely tokens
    # max_output_tokens=4024, # Limit the length of the response
    # #If using a "Thinking" model, you would uncomment this:
    # thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_level="HIGH"),
    
    tools=tools,
  )

  response = client.models.generate_content(
    model=model,
    contents=contents,
    config=config,
  )
  print(response.text)

if __name__ == "__main__":
    generate()
