from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello from Zeabur! (Python)'

if __name__ == '__main__':
    # Zeabur 會自動注入 PORT 環境變數，預設為 8080
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
