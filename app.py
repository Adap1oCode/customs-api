from flask import Flask, render_template
from customs_declarations import get_data
from notifications import get_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
