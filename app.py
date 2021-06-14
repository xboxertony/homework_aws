import re
import boto3
from flask import Flask,render_template,jsonify
from flask.globals import request
from config import aws_access_key_id,aws_secret_access_key,DATABASE_URI,dict_for_database
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

s3 = boto3.client(
    "s3",
    aws_access_key_id = aws_access_key_id,
    aws_secret_access_key = aws_secret_access_key
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_BINDS"] = dict_for_database
db = SQLAlchemy(app)

allow_path = set(["jpg","png","JPG","PNG"])

@app.route("/upload",methods=["POST"])
def upload():
    if request.method=="POST":
        # print(request.files)
        # print(request.form.get("text"))
        photo = request.files["files"]
        text = request.form.get("text")
        if photo.filename.split(".")[-1] not in allow_path:
            return jsonify({"error":True})
        file_path = "static/photo/"+photo.filename
        real_path = "http://d3nczlg85bnjib.cloudfront.net/"+photo.filename
        sql = f"insert into img_test (url,text) values ('{real_path}','{text}')"
        db.engine.execute(sql)
        photo.save(file_path)
        s3.upload_file(file_path,"tonytony58",photo.filename,ExtraArgs={'ACL': 'public-read'})
        return jsonify({"ok":True})

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_img")
def get_img():
    sql = f"select url,text from img_test order by id desc"
    r = db.engine.execute(sql)
    arr = []
    for i in r:
        item = {"url":i[0],"text":i[1]}
        arr.append(item)
    return jsonify({"data":arr})

# @app.route("/get_another")
# def get_another():
#     engine = create_engine(app.config['SQLALCHEMY_BINDS']['db2'])
#     sql = f"select url,text from img_test order by id desc"
#     r = db.session.execute(sql,bind=engine)
#     arr = []
#     for i in r:
#         item = {"url":i[0],"text":i[1]}
#         arr.append(item)
#     return jsonify({"data":arr})

# @app.route("/word",methods=["POST"])
# def word():
#     text = request.get_json()["data"]
#     sql = f"insert into img_test (text) values ('{text}')"
#     return jsonify({"ok":True})


if __name__=="__main__":
    app.run(host="0.0.0.0",port=3000,debug=True)