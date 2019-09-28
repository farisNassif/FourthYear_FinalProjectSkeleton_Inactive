import pymongo
from pymongo import MongoClient
from flask import Flask, render_template, url_for, request, redirect, Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from bson.objectid import ObjectId

# MongoString generated on my https://cloud.mongodb.com account
cluster = MongoClient("mongodb+srv://faris:loughrea@skeletonforproject-a2j6y.mongodb.net/test?retryWrites=true&w=majority")

app = Flask(__name__)

db2 = cluster["testdb"]
collection = db2["testcollection"]

# Index route so when I browse to the url it doesn't 404
@app.route('/', methods=['Post', 'GET'])
def index():
    # Whenever someone wants to submit
    if request.method == 'POST':
        # Preparing data to be inserted into mongo
        postForCollection = {"content":request.form['content'],"date_created":datetime.now()}
        try:        
            # Posting data stored above to mongo
            collection.insert_one(postForCollection)
            # Once above commits are made return back to index page
            return redirect('/')
        # Error Handling
        except: 
            # If for some reason data couldn't be commit throw an error message
            return 'Issue adding input'
    else:
        # Retrieving Mongo data and putting it in a list
        mongoData = list(collection.find())
        # Base Page
        return render_template('index.html', tasks=mongoData)

# Delete route, delete by id
@app.route('/delete/<string:_id>')
def delete(_id):
    # Attempt to get task by id or 404 if it doesn't exist
    try: 
        print(_id)
        # collection.delete_one(entryToDelete)
        collection.remove( {'_id': ObjectId(_id) } ) 
        return redirect('/')
    except:
        return 'Deleting didnt work :( '

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    # Attempt to get task by id or 404 if it doesn't exist
    # task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        # Setting above tasks content to the content in the update input field
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Updating didnt work :('
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    # If theres any errors they'll pop up on the page
    app.run(debug=True)