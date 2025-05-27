from flask import Flask
import os

app = Flask(__name__, template_folder='app/templates')  # 指定模板路径
app.secret_key = os.urandom(24)

from app.routes import bp
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)
