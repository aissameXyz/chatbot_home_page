
from distutils.log import error
from urllib import response
from colorama import Cursor
from flask_ngrok import run_with_ngrok
from flask import Flask, render_template, request, jsonify, make_response,flash
from flask_cors import CORS, cross_origin
import requests
import pymongo
import json
import os
from saveConversation import Conversations
from pymongo import MongoClient
from requests import Response
with open('config.json') as file:
    params=json.load(file)['params']

app=Flask(__name__)
run_with_ngrok(app)

@app.route('/home')
def home():
    return render_template('home.html') 
  
@app.route('/webhook',methods=['POST','GET'])
def webhook():
    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    return r

def processRequest(req):
    
    log = Conversations.Log()
    sessionID = req.get('responseId')
    result = req.get("queryResult")
    intent = result.get("intent").get('displayName')
    query_text = result.get("queryText")
    parameters = result.get("parameters")
    db = configureDataBase()
    fulfillmentText = result.get("fulfillmentText")
    log.saveConversations(sessionID, query_text, fulfillmentText, intent, db)   

@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('Myhome.html')
@app.route('/home', methods=('GET', 'POST'))
def home_page():
    return render_template('login.html')
@app.route('/index', methods=('GET', 'POST'))
def indexe():
    return render_template('index.html')

@app.route('/sign', methods=('GET', 'POST'))
def sign():
    return render_template('signin.html')
@app.route('/login',methods=('GET','POST'))
def login():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        db=database()
        users=db.users
        user=users.find_one({'username':username,'password':password})
        if not user:
            dict={
            
            'username':username,
            'email':email,
            'password':password
            }
            users.insert_one(dict)
            return render_template('index.html')
        else:
           return render_template('login.html',error="the user is already exists try to signin ")
            
     
@app.route('/signin',methods=('GET','POST')) 
def signin():
    errore="the user doesnt exists create one"
    if request.method=='POST':
        username=request.form['username']
        
        password=request.form['password']
        db=database()
        users=db.users
        if users.find_one({'username':username,'password':password}):
            return render_template('index.html')
        else:
            
            return render_template('signin.html',error=errore)



def database():
    client = MongoClient("mongo_url")
    db=client.get_database('db')
    return db



def configureDataBase():
    client = MongoClient("mongo_url")
    return client.get_database('yourDb')



if __name__ == "__main__":
    app.run()
