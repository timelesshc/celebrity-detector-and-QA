import os
import base64
import requests
from utils.logger import get_logger

class CelebrityDetector:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.api_key = os.getenv("GROQ_API_KEY")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "meta-llama/llama-4-maverick-17b-128e-instruct"
        
        if not self.api_key:
            self.logger.warning("GROQ_API_KEY not found in environment variables")
        else:
            self.logger.info(f"GROQ_API_KEY found: {self.api_key[:10]}..." if len(self.api_key) > 10 else "GROQ_API_KEY found (short)")

    def identify(self, image_bytes):
        encoded_image = base64.b64encode(image_bytes).decode()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        prompt = {
            "model": self.model,
            "messages": [
                {
                    "role": "user", 
                    "content": [
                        {
                            "type": "text",
                            "text": """You are a celebrity recognition expert AI. 
                            Identify the person in the image. If known, respond in this format:

                            - **Full Name**:
                            - **Profession**:
                            - **Nationality**:
                            - **Famous For**:
                            - **Top Achievements**:

                            If unknown, return "Unknown".
                                    """
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}"
                            }
                        }
                    ]
                }
            ],
            "temperature": 0.3,    
            "max_tokens": 1024     
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=prompt)
            self.logger.info(f"API Response status code: {response.status_code}")
            self.logger.debug(f"API Response content: {response.text[:200]}...")

            if response.status_code == 200:
                result = response.json()['choices'][0]['message']['content']
                name = self.extract_name(result)
                
                if result.strip().lower() == "unknown" or name == "Unknown":
                    return "No celebrity detected. Please try again.", None
                
                self.logger.info(f"Celebrity detected: {name}")
                return result, name
            else:
                error_msg = f"API Error {response.status_code}: {response.text}"
                self.logger.error(error_msg)
                return error_msg, None
        except Exception as e:
            error_msg = f"Error calling celebrity detection API: {str(e)}"
            self.logger.error(error_msg)
            return error_msg, None
    
    def extract_name(self, response_text):
        for line in response_text.split("\n"):
            if line.lower().startswith("- **full name**:"):
                return line.split(":")[1].strip()
        
        return "Unknown"