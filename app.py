from flask import Flask
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)



@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
