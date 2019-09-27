from flask import Flask, render_template

app = Flask(__name__)

# Index route so when I browse to the url it doesn't 404

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    # If theres any errors they'll pop up on the page
    app.run(debug=True)