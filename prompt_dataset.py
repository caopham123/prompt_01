import pandas as pd
from config import GOOGLE_API_KEY
from google import genai
from google.genai import types

def get_column_data():
    file_path = "comment_services.xlsx"

    df = pd.read_excel(
        file_path, 
        sheet_name='Sheet1', 
        usecols="C", 
        skiprows=2, # Bỏ qua 2 dòng đầu tiên để lấy từ C3
        # nrows=260
    )
    df = df.fillna('')  # Điền giá trị NaN bằng chuỗi rỗng
    
    # Chuyển thành danh sách (list)
    danh_sach_level_3 = df.iloc[:, 0].dropna().unique().tolist()
    
    for item in danh_sach_level_3:
      print(item)

def load_taxonomy_from_dataset(file_path:str):
  df = pd.read_excel(file_path,sheet_name='Sheet1')
  df = df.fillna('')  # Điền giá trị NaN bằng chuỗi rỗng
  taxonomy_text = "Danh mục dịch vụ:\n"

  for index, row in df.iterrows():
    number = index + 1
    lv_1 = row['Level 1']
    lv_2 = row['Level 2']
    lv_3 = row['Level 3']
    taxonomy_text += f"{number}. {lv_1} > {lv_2} > {lv_3}:\n"
    if row['MÔ TẢ']:
      taxonomy_text += f"  -- Mô tả: {row['MÔ TẢ']}\n"
    if row['Ví dụ']:
      taxonomy_text += f"  -- Ví dụ: {row['Ví dụ']}\n"

  return taxonomy_text

def classify_feedback(input_feedback:str, taxonomy_context:str):
  client = genai.Client(api_key=GOOGLE_API_KEY)
  model = "gemini-3-flash-preview"
  system_instruction = f"""
    Bạn là một chuyên gia phân loại dữ liệu. Dựa vào danh mục hệ thống dưới đây, 
    hãy phân loại feedback của khách hàng vào đúng 3 cấp độ.
    {taxonomy_context}
    Yêu cầu: 
    1. Gán nhãn của feedback theo 3 cấp độ.
    Ví dụ: Nhân viên giao dịch, nhân viên tư vấn thái độ không tốt, hay cáu gắt.
    => Level 1: Dịch vụ khách hàng, Level 2: Thái độ cán bộ chi nhánh, Level 3: Giao dịch viên

    2. Trả về kết quả dưới dạng JSON: {{"feedback": "Nhân viên giao dịch, nhân viên tư vấn thái độ không tốt, hay cáu gắt.", "level_1": "Dịch vụ khách hàng", "level_2": "Thái độ cán bộ chi nhánh", 
    "level_3": "Giao dịch viên", "sentiment/classifier": "tích cực/tiêu cực/không xác định", "keywords": ["từ khóa 1", "từ khóa 2"], "suggestion": "gợi ý cải thiện dịch vụ"}}
    """
  
  tools = [types.Tool(googleSearch=types.GoogleSearch()),]
  config = types.GenerateContentConfig(
    temperature=0.2,       # Controls randomness (0.0 to 2.0)
    top_p=0.9,            # Lấy sample có tổng xác suất cao
    # top_k=40,           #  Lấy Sample from the top K most likely tokens
    # max_output_tokens=1000, # Limit the length of the response
    response_mime_type="application/json",
    tools=tools,
    # If using a "Thinking" model, you would uncomment this:
    # thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_level="HIGH"),
    
  )

  response = client.models.generate_content(
    model=model,
    contents=input_feedback,
    config=config,
  )
  print(response.text)
  
if __name__ == "__main__":
  # get_column_data()
  # print(load_taxonomy_from_dataset("comment_services.xlsx"))
  # load_taxonomy_from_dataset("comment_services.xlsx")
  classify_feedback(
    input_feedback="Nhân viên giao dịch, nhân viên tư vấn thái độ không tốt, hay cáu gắt. Tôi cảm thấy không hài lòng về dịch vụ.",
    taxonomy_context=load_taxonomy_from_dataset("comment_services.xlsx"))