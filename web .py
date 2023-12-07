from flask import Flask, render_template
from main import flag


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('fine.html')



if __name__ == '__main__':
    if flag == 1:
        app.run(host='127.0.0.1', debug=True)
        raise SystemExit(1)

