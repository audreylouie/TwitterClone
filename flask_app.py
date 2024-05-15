
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, redirect, render_template, session, make_response, url_for
from flask_session import Session
import datetime

import random
import json
import boto3
import uuid

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

AWSKEY = ''
AWSSECRET = ''
PUBLIC_BUCKET = 'sm87295n'
#STORAGE_URL = 'http://sm87295n.s3-website.us-east-2.amazonaws.com/'
STORAGE_URL = 'https://sm87295n.s3.amazonaws.com/'


def get_public_bucket():
    s3 = boto3.resource(service_name = 's3',
    region_name = 'us-east-2',
    aws_access_key_id= AWSKEY,
    aws_secret_access_key=AWSSECRET)

    bucket = s3.Bucket(PUBLIC_BUCKET)
    return bucket



#helper function to get a dynamodb table
def get_table(name):
    client = boto3.resource(service_name = 'dynamodb',
                        region_name = 'us-east-2',
                        aws_access_key_id = AWSKEY,
                        aws_secret_access_key=AWSSECRET)

    table = client.Table(name)
    return table


#project code

@app.route('/signup.html')
def signup_page():
    return render_template("signup.html")


@app.route('/signup', methods=['GET'])
def signup():
    table = get_table("AppUser")
    email = request.args.get('email')
    username = request.args.get('username')
    password = request.args.get('password')
    id = str(uuid.uuid4())

    if not email or '@' not in email or '.' not in email:
        return {'result': 'Invalid email'}

    if not username or not password:
        return {'result': 'Username and password can not be blank.'}

    # Check if the email already exists
    existing = get_user_by_email(email)
    if existing is not None:
        return {'result': 'Email in use '}

    # Save user information to the database
    userInfo = {'id': id, 'email': email, 'username': username, 'password': password, 'image': "", 'image_url':""}
    table.put_item(Item=userInfo)

    # Set user session
    session['user_id'] = id
    session['username'] = username

    return {'result': 'OK', 'username': username}

@app.route('/logout.html')
def logout_page():
    return render_template("login.html")

@app.route('/')
def home_page():
    return render_template("login.html")


@app.route('/login.html')
def login_page():
    return render_template("login.html")

@app.route('/login')
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    if not username or not password:
        return {'result': 'Missing username or password'}

    # Query the DynamoDB table to find the user with the provided username
    table = get_table("AppUser")
    response = table.scan(
        FilterExpression='username = :username',
        ExpressionAttributeValues={':username': username}
    )

    # Check if any items match the username
    items = response.get('Items', [])
    if not items:
        return {'result': 'Username not found'}

    # Assuming usernames are unique, there should be only one user with the provided username
    user = items[0]

    # Check if the password matches
    if user.get('password') != password:
        return {'result': 'Incorrect password'}

    # Authentication successful
    # Set user session
    session['user_id'] = user['id']
    session['username'] = user['username']

    return {'result': 'OK', 'username': user['username']}

def get_user_by_email(email):
    table = get_table("AppUser")
    response = table.scan(
        FilterExpression='email = :email',
        ExpressionAttributeValues={':email': email}
    )

    # Check if any items match the email
    items = response.get('Items', [])
    if not items:
        return None

    # Assuming email are unique, there should be only one user with the provided email
    user = items[0]
    return user

def get_user_by_username(username):
    table = get_table("AppUser")
    response = table.scan(
        FilterExpression='username = :username',
        ExpressionAttributeValues={':username': username}
    )

    # Check if any items match the username
    items = response.get('Items', [])
    if not items:
        return None

    # Assuming usernames are unique, there should be only one user with the provided username
    user = items[0]
    return user

def get_post_by_post_id(post_id):
    table = get_table("Post")
    response = table.scan(
        FilterExpression='post_id = :post_id',
        ExpressionAttributeValues={':post_id': post_id}
    )

    # Check if any items match the username
    items = response.get('Items', [])
    if not items:
        return None

    # Assuming usernames are unique, there should be only one user with the provided username
    post = items[0]
    return post

@app.route('/post/<post_id>')
def post_id(post_id):
    #make a template, get text, username and date or fields,in the post - need a js for list replies need to call //,that will call the parent_id
    #session['post_id']= post_id
    post = get_post_by_post_id(post_id)
    text = post["text"]
    username = post["username"]
    return render_template('post.html',post_id = post_id, username=username, text = text)

def get_photo_by_username(username):
    user = get_user_by_username(username)

    if user['image_url'] == "":
        user['image_url'] = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRpHyzR9FXgWHf12X8gdOnzbjjYBNgik7Tk9-Px4qEe9fa2jpxQLA64SXFAihZy4w1X3qM&usqp=CAU"

    return user['image_url']

def get_imageURL_by_username(image_url):
    table = get_table("AppUser")
    response = table.scan(
        FilterExpression='image_url= :img',
        ExpressionAttributeValues={':img': image_url}
    )

    # Check if any items match the username
    items = response.get('Items', [])
    if not items:
        return None

    # Assuming usernames are unique, there should be only one user with the provided username
    image = items[0]
    return image


@app.route('/profile/<username>')
def profile(username):
    # Fetch the profile image URL using the get_profile_image_url function

        if username:
        # Pass the profile image URL to the template
            user = get_user_by_username(username)
            if user is None:
                return redirect("/")
            else:
                image_url = user["image_url"]
            if image_url == "":
                image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRpHyzR9FXgWHf12X8gdOnzbjjYBNgik7Tk9-Px4qEe9fa2jpxQLA64SXFAihZy4w1X3qM&usqp=CAU"
            if session ["username"] == username:
                return render_template("profile.html", username=username, image_url=image_url)
            else:
                return render_template("profile_other.html", username=username, image_url=image_url)
        else:
            return render_template("signup.html")


@app.route('/list_post/<username>')
def list_post(username):
    table = get_table('Post')
    results = []

    # Query posts based on the provided username
    response = table.scan(
        FilterExpression='username = :username',
        ExpressionAttributeValues={':username': username}
    )

    for item in response['Items']:
        parent_id = item['parent_id']
        if parent_id != "":
            continue

        id = item['post_id']
        text = item['text']
        date = item['date']
        user = item['username']

        x = {'id': id, 'text': text, 'date': date, 'username': user}
        results.append(x)

        #if parent_id != "":
            #continue

    results.sort(key=get_post_entry_date, reverse=True)

    return {'result': results, 'username': username}

@app.route('/post_entry')
def post_entry():
    table = get_table("Post")
    text = request.args.get('text')
    date = datetime.datetime.now().strftime('%Y-%m-%d %X')
    entry_id = str(uuid.uuid4())
    parent_id = ""
    username = session.get('username')

    # Save post to DynamoDB
    content = {'post_id': entry_id, 'text': text, 'date': date, 'username': username, 'parent_id':parent_id}
    table.put_item(Item=content)

    return {'result': 'OK', 'username':username}

def get_post_entry_date(entry):
    return entry['date']

@app.route('/feed.html')
def feed():
    username = session.get('username')
    return render_template('feed.html', username=username)

@app.route('/post_reply')
def post_reply():
    table = get_table("Post")
    text = request.args.get('text')
    date = datetime.datetime.now().strftime('%Y-%m-%d %X')
    entry_id = str(uuid.uuid4())
    parent_id = request.args.get('pid')
    username = session.get('username')

    # Save post to DynamoDB
    content = {'post_id': entry_id, 'text': text, 'date': date, 'username': username, 'parent_id':parent_id}
    table.put_item(Item=content)

    return {'result': 'OK', 'username':username}

@app.route('/list_replies')
def list_replies():

    p = request.args.get('parent_id')
    table = get_table('Post')
    results = []

    # Scan all items in the 'Post' table
    response = table.scan()

    for item in response['Items']:
        id = item['post_id']
        text = item['text']
        date = item['date']

        # Check if the 'username' attribute exists
        if 'username' in item:
            username = item['username']
        else:
            username = None  # Set username to None if 'username' attribute is missing

        parent_id = item['parent_id']
        # if the parent_id is not the one we're looking for skip it
        if parent_id != p:
            continue

        image_url = get_photo_by_username(username)
        x = {'post_id': id, 'text': text, 'date': date, 'username': username, image_url:'image_url'}
        results.append(x)

    # Sort the results by date in descending order
    results.sort(key=lambda x: x['date'], reverse=True)


    return {'result': results}


@app.route('/list_recent_posts')
def list_recent_posts():
    table = get_table('Post')
    results = []

    # Scan all items in the 'Post' table
    response = table.scan()

    for item in response['Items']:
        id = item['post_id']
        text = item['text']
        date = item['date']

        # Check if the 'username' attribute exists
        if 'username' in item:
            username = item['username']
        else:
            username = None  # Set username to None if 'username' attribute is missing

        parent_id = item['parent_id']
        # if the parent_id = "" that means its the original msg, if not blank it is a reply to that post

        if parent_id != "": # it's a reply
            continue

        image_url = get_photo_by_username(username)
        x = {'post_id': id, 'text': text, 'date': date, 'username': username, 'image_url':image_url}
        results.append(x)

    # Sort the results by date in descending order
    results.sort(key=lambda x: x['date'], reverse=True)

    # Limit the results to the ten most recent posts
    results = results[:10]

    return {'result': results}


@app.route('/uploadfile', methods=['POST'])
def upload_file():
    bucket = get_public_bucket()
    file = request.files["file"]
    filename = file.filename
    #user_email = request.form.get("txtEmail")

    # Determine content type based on filename extension (optional)
    ct = 'image/jpeg'
    if filename.endswith('.png'):
        ct = "image/png"

    #uid=str(uuid.uuid4())
    #filename = uid + "-" + filename

    # Upload file to S3
    bucket.upload_fileobj(file, filename, ExtraArgs={'ContentType': ct})
    #bucket.upload_fileobj(file, PUBLIC_BUCKET, filename)

    table = get_table('AppUser')
    #file = request.files["file"]
    image_id = str(uuid.uuid4())

    user_id = session.get('user_id')


    # Get the URL of the uploaded image
    image_url = STORAGE_URL + filename
    #image_url= f"{STORAGE_URL}/{filename}"

    table.update_item(
        Key={'id': user_id},
        UpdateExpression='SET image_url =:img',
        ExpressionAttributeValues={':img': image_url}
    )

    # Return the URL as a JSON response
    return {'results': 'OK', 'image_url': image_url}



"""
@app.route('/uploadfile', methods=['POST'])
def upload_file():
    bucket = get_public_bucket()
    file = request.files["file"]
    filename = file.filename
    caption = request.form.get('caption', '')

    # Determine content type based on filename extension (optional)
    ct = 'image/jpeg'
    if filename.endswith('.png'):
        ct = "image/png"

    # Upload file to S3
    bucket.upload_fileobj(file, filename, ExtraArgs={'ContentType': ct})

    table = get_table('post')
    file = request.files["file"]
    caption = request.form["caption"]

    image_id = str(uuid.uuid4())

    filename = file.filename

    table.put_item(
        Item={
            'post_id': image_id,
            'caption': caption,
            'filename': filename
        }
    )
    return {'results': 'OK'}

def signup
 table = get_table("AppUser")
    email = request.args.get('email')
    username = request.args.get('username')
    password = request.args.get('password')
    id = str(uuid.uuid4())

    if not email or '@' not in email or '.' not in email:
        return {'result': 'Invalid email'}

    if not username or not password:
        return {'result': 'blank'}

    # Check if the email already exists
    resp = table.scan(AttributesToGet=['email'])
    if any(username['email'] == email for username in resp['Items']):
        return {'result': 'BAD'}

    # Save user information to the database
    userInfo = {'id': id, 'email': email, 'username': username, 'password': password, 'image': ""}
    table.put_item(Item=userInfo)

    # Set user session
    session['user_id'] = id
    session['username'] = username

    return {'result': 'OK', 'username': username}

"""






