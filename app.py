from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# Where the database is located
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Return a string everytime make a new element
    def __repr__(self):
        return '<Task %r>' % self.id

# Index route so when I browse to the url it doesn't 404
@app.route('/', methods=['Post', 'GET'])
def index():
    # Whenever someone wants to add some input 
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        # Error Handling
        except: 
            return 'Issue adding input'
    else:
        # Looks at database contents in order they were created and show all of them
        tasks = Todo.query.order_by(Todo.date_created).all()
        # Base Page
        return render_template('index.html', tasks=tasks)

if __name__ == "__main__":
    # If theres any errors they'll pop up on the page
    app.run(debug=True)