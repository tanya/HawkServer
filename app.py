from flask import Flask
from flask import request
import dcapi
import json
app = Flask(__name__)

@app.route('/')
def square_of_distrust():
    return 'Welcome to the Square of Distrust!'


@app.route('/register', methods=['POST'])
def register():
    userId = request.form['userId']
    email = request.form['email']
    password = request.form['password']
    success = dcapi.register(userId, email, password)
    if success == False:
        return json.dumps({'status' : 'error', 'message' : 'Something went wrong, please try again!'})
    else:
        return json.dumps({'status' : 'ok', 'message' : 'Registration successful!', 'userId' : userId})

@app.route('/login', methods=['POST'])
def login():
    userId = request.form['userId']
    password = request.form['password']
    success = dcapi.login(userId, password)
    if success == False:
        return json.dumps({'status' : 'error', 'message' : 'Login was not successful! Please make sure your user id or password is correct'})
    else:
        return json.dumps({'status' : 'ok', 'message' : 'Login successful!', 'userId' : userId})

@app.route('/updateCrimes')
def update_crimes():
    lat = request.args.get('lat','')
    lon = request.args.get('lon','')
    radius = request.args.get('radius','')
    if checkValidString(lat) and checkValidString(lon) and checkValidString(radius) and checkValidString(radius):
        return json.dumps({'status' : 'ok', 'message' : dcapi.updateCrimes(float(lat), float(lon), float(radius))})
    return json.dumps({'status' : 'error', 'message' : 'invalid arguments'})


@app.route('/getCrimes')
def getCrimes():
    lat = request.args.get('lat','')
    lon = request.args.get('lon','')
    radius = request.args.get('radius','')
    if checkValidString(lat) and checkValidString(lon) and checkValidString(radius):
        try:
            results = dcapi.getCrimes(float(lat), float(lon), float(radius))
            return json.dumps({'status' : 'ok', 'results' : results})
        except ValueError:
            return json.dumps({'status' : 'error', 'message' : 'arguments were not all numbers'})
    else:
        return json.dumps({'status' : 'error', 'message' : 'invalid arguments'})

@app.route('/createReview', methods=['POST'])
def createReview():
    rating = request.form['rating']
    lat = request.form['lat']
    lon = request.form['lon']
    comments = request.form['comments']
    userId = request.form['userId']
    message = dcapi.postReview(rating, lat, lon, comments, userId)
    return json.dumps(message)

@app.route('/voteForReview', methods=['POST'])
def voteForReview():
    rId = request.form['rId']
    userId = request.form['userId']
    upvote = request.form['upvote']
    result = dcapi.voteForReview(rId, userId, upvote)
    return json.dumps(result)

@app.route('/getVotedReviews')
def getVotedReviews():
    userId = request.args.get('userId','')
    result = dcapi.getVoted(userId)
    result = {'votes' : result}
    return json.dumps(result)

@app.route('/getReviews')
def getReviews():
    lat = request.args.get('lat','')
    lon = request.args.get('lon','')
    radius = request.args.get('radius','')
    if checkValidString(lat) and checkValidString(lon) and checkValidString(radius):
        try:
            results = dcapi.getReviews(float(lat), float(lon), float(radius))
            return json.dumps({'status' : 'ok', 'results' : results})
        except ValueError:
            return json.dumps({'status' : 'error', 'message' : 'invalid arguments'})
    else:
        return json.dumps({'status' : 'error', 'messgae' : 'invalid arguments'})


@app.route('/getReviewsByUserId')
def getReviewsByUserId():
    userId = request.args.get('userId','')
    if not checkValidString(userId):
        return json.dumps({'status' : 'error', 'message' : 'please enter a valid user id'})
    else:
        results = dcapi.getReviewsByUserId(userId)
        return json.dumps({'status' : 'ok' , 'results' : results})

@app.route('/getCityScore')
def getCityScore():
    lat = request.args.get('lat',0.0)
    lon = request.args.get('lon',0.0)
    res = dcapi.getCityScore(lat, lon)
    return json.dumps(res)

@app.route('/getCityCrimesCount')
def getCityCrimesCount():
    lat = request.args.get('lat',0.0)
    lon = request.args.get('lon',0.0)
    window = request.args.get('window','')
    res = dcapi.getCrimesInWindow(lat,lon,window)
    return json.dumps(res)


@app.route('/updateGunLaws')
def uploadGunLaws():
    dcapi.postGunLaws()
    return 'update'

def checkValidString(string):
    if string == None or len(string) < 1:
        return False
    return True
