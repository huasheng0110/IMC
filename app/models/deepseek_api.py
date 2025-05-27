import os
import requests

# 你的 DeepSeek API Key
api_key = "************************************"  # ←←← 填入你的 API Key

def ask_deepseek(user_question):
    # 确保不使用代理
    os.environ.pop('HTTP_PROXY', None)
    os.environ.pop('HTTPS_PROXY', None)

    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "MedicalChatbot/1.0 (compatible; HealthcareSystem)"
    }
    
    data = {
        "messages": [{
            "role": "user",
            "content": f"[医疗系统上下文] {user_question}",
        }],
        "model": "deepseek-chat",
        "temperature": 0.3,
        "max_tokens": 1000
    }
    
    try:
        with requests.Session() as session:
            session.mount('https://', requests.adapters.HTTPAdapter(max_retries=3))
            
            response = session.post(
                url, 
                headers=headers,
                json=data,
                timeout=(10, 60),
                proxies={}  # 禁用代理
            )

        if response.status_code != 200:
            error_msg = f"API Error: {response.status_code} - {response.reason}"
            print(f"{error_msg}\nResponse Body: {response.text[:300]}")
            return error_msg

        json_response = response.json()
        
        if not all(key in json_response for key in ["choices", "usage"]):
            raise ValueError("Invalid API response structure")
            
        return json_response["choices"][0]["message"]["content"]

    except (requests.exceptions.RequestException, KeyError, ValueError) as e:
        print(f"API Request Failed: {str(e)}")
        return "医疗服务引擎暂时不可用，请联系管理员"

# 示例调用
if __name__ == "__main__":
    user_question = "如何预防高血压？"
    result = ask_deepseek(user_question)
    print(f"DeepSeek 医疗助手回答：\n{result}")
