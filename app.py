from flask import Flask

app = Flask(__name__)

# Index route so when I browse to the url it doesn't 404

@app.route('/')
def index():
    return "Hello World"

if __name__ == "__main__":
    # If theres any errors they'll pop up on the page
    app.run(debug=True)