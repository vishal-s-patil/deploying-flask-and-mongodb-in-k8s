from flask import Flask, render_template, request, redirect
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)

user = 'username'           
password = 'password'       
host = 'mongodb-service'    
port = 27017              
conn_string = f'mongodb://{user}:{password}@{host}:{port}'
db_name = 'blog'

db = ""

@app.route('/')
def home():
    global db
    try:
        client = MongoClient(conn_string)
        db = client[db_name]
        posts = list(db.posts.find({}))
        return render_template("home.html", homeIsActive=True, createPostIsActive=False, posts=posts)
        
    except pymongo.errors.ConnectionFailure:
        print("Connection Failed")
        return "failed"

@app.route('/create-post', methods=["GET", "POST"])
def createPost():
    if(request.method=="GET"):
        return render_template("create-post.html", homeIsActive=False, createPostIsActive=True)

    elif(request.method == "POST"):
        title = request.form['title']
        author = request.form['author']
        createdAt = datetime.now()

        db.posts.insert_one({"title": title, "author": author, "createdAt": createdAt})

        return redirect("/")

@app.route('/edit-post', methods=['GET', 'POST'])
def editPost():
    if request.method == "GET":
        postId = request.args.get('form')

        post = dict(db.posts.find_one({"_id":ObjectId(postId)}))

        return render_template('edit-post.html', post=post)

    elif request.method == "POST":
        postId = request.form['_id']
        title = request.form['title']
        author = request.form['author']

        db.posts.update_one({"_id":ObjectId(postId)},{"$set":{"title":title,"author":author}})

        return redirect("/")

@app.route('/delete-post', methods=['POST'])
def deletePost():
    postId = request.form['_id']

    db.posts.delete_one({ "_id": ObjectId(postId)})

    return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)