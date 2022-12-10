from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__, root_path="/api")
csrf = CSRFProtect()
csrf.init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
