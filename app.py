import boto3
from flask import Flask,render_template,jsonify
from flask.globals import request
from config import aws_access_key_id,aws_secret_access_key

s3 = boto3.client(
    "s3",
    aws_access_key_id = aws_access_key_id,
    aws_secret_access_key = aws_secret_access_key
)

app = Flask(__name__)

allow_path = set(["jpg","png","JPG","PNG"])

@app.route("/upload",methods=["POST"])
def upload():
    if request.method=="POST":
        photo = request.files["files"]
        if photo.filename.split(".")[-1] not in allow_path:
            return jsonify({"error":True})
        file_path = "static/photo/"+photo.filename
        photo.save(file_path)
        s3.upload_file(file_path,"tonytony58",photo.filename,ExtraArgs={'ACL': 'public-read'})
        return jsonify({"ok":True})

@app.route("/")
def home():
    return render_template("index.html")

# result = s3.get_bucket_acl(Bucket="tonytony58")

# response = s3.upload_file("static/test.png","tonytony58","test.png")

# print(response)

app.run(debug=True)