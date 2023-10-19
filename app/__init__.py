from flask import Flask,request, jsonify
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from resources.subscriptions import routes
from firebase_admin import initialize_app, auth


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://baacmudo:vqBxenJTLvyvBhsX0ZPsmN_VSPC9-pS2@chunee.db.elephantsql.com/baacmudo'
db = SQLAlchemy(app)


firebase_config = {
    "apiKey": "AIzaSyAZMhQtdhLlnjA95iujv6mArE0cK02za5s",
    "authDomain": "fir-demo-matrix-130.firebaseapp.com",
    "projectId": "fir-demo-matrix-130",
    "storageBucket": "fir-demo-matrix-130.appspot.com",
    "messagingSenderId": "575173277598",
    "appId": "1:575173277598:web:c0c2d6670fd8008babc88f"
}
firebase = initialize_app(firebase_config)





