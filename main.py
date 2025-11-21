from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai import types

app = Flask(__name__)

# 設定 Gemini API
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

@app.route('/')
def hello():
    return 'Hello from Zeabur! (Python)'

@app.route('/api/info', methods=['GET'])
def info():
    """簡單的資訊 API"""
    return jsonify({
        'service': 'Zeabur Demo API',
        'version': '1.0.0',
        'endpoints': [
            {'path': '/', 'method': 'GET', 'description': 'Hello message'},
            {'path': '/api/info', 'method': 'GET', 'description': 'API information'},
            {'path': '/api/gemini', 'method': 'POST', 'description': 'Call Gemini API'}
        ]
    })

@app.route('/api/gemini', methods=['POST'])
def gemini_api():
    """呼叫 Gemini API 的 endpoint"""
    try:
        # 從 request body 取得 prompt
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({
                'error': 'Missing prompt in request body',
                'example': {'prompt': 'Tell me a joke'}
            }), 400
        
        prompt = data['prompt']
        
        # 已在 client.generate_content 呼叫中設定安全過濾，這裡的舊 safety_settings 已移除

        
        # 使用 genai.GenerativeModel 呼叫 Gemini API（限制輸出長度在 50 tokens 內）
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(
            prompt,
            generation_config=types.GenerationConfig(
                max_output_tokens=50,
            ),
            safety_settings=[
                {
                    "category": types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                    "threshold": types.HarmBlockThreshold.BLOCK_NONE,
                },
                {
                    "category": types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                    "threshold": types.HarmBlockThreshold.BLOCK_NONE,
                },
                {
                    "category": types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                    "threshold": types.HarmBlockThreshold.BLOCK_NONE,
                },
                {
                    "category": types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    "threshold": types.HarmBlockThreshold.BLOCK_NONE,
                },
            ],
        )
        
        # 若被安全過濾器阻擋
        if not response.candidates or not response.candidates[0].content.parts:
            finish_reason = response.candidates[0].finish_reason if response.candidates else "UNKNOWN"
            return jsonify({
                'success': False,
                'error': f'Response blocked by safety filter. Finish reason: {finish_reason}',
                'prompt': prompt
            }), 400
        
        return jsonify({
            'success': True,
            'prompt': prompt,
            'response': response.text
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Zeabur 會自動注入 PORT 環境變數，預設為 8080
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
