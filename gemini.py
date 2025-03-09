import google.generativeai as genai
genai.configure(api_key="YOUR_KEY")
response = genai.generate_content("What is a 401k?")
print(response.text)