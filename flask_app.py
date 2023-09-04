# A very simple Flask Hello World app for you to get started with...

from flask import Flask

app = Flask(__name__)

@app.route('/')


def run_script():
    file = open(r'/home/pythdepl/AvacadoDashApplication/app.py', 'r').read()
    return exec(file)

if __name__ == "__main__":
    app.run(debug=True, port=8051)