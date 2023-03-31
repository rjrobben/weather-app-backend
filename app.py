from flask import Flask, request, jsonify, session 
from flask_cors import CORS
from api.weather import Weather
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "dffdc06b68ba4bd57c55650929fbe3510ebc5a54d1ec9cebeb5bd91bfb72541c"
CORS(app)

api_key = 'dd32cd76830f2f6c410e45ac4570f532'
weather = Weather(api_key)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/weather')
def get_weather():
    # get the location from the query parameter
    location = request.args.get('location')
    if not location:
        return jsonify({'error': 'location parameter is missing'}), 400
    
    return weather.get_current_weather(location)


@app.route('/forecast')
def get_forecast():
    # get the location from the query parameter
    location = request.args.get('location')
    if not location:
        return jsonify({'error': 'location parameter is missing'}), 400

    return weather.get_forecast(location)

# not enough time to implement the database, for now, I will just use a dictionary to store the users
# if later have time can install and build the database
# and use the database like this

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/mydatabase'
# db = SQLAlchemy(app)

# class User(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   email = db.Column(db.String(120), unique=True, nullable=False)
#   password = db.Column(db.String(120), nullable=False)

# add add to db like this:
# db.session.add(user)
# db.session.commit()

users = {}


# Register a new user
@app.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    password = request.json.get('password')

    if email not in users:
        # Hash the password before storing it in the database
        hashed_password = generate_password_hash(password, method='sha256')
        # Store the user information in the database
        users[email] = hashed_password

        # return a message saying successful registration and a success status code
        return jsonify({'message': 'Registered successfully'}), 201
    else:
        return jsonify({'message': 'User already exists'}), 409

# Log in a user
@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    # Retrieve the user information from the database

    if email not in users:
        return jsonify({'message': 'User does not exist'}), 404

    if check_password_hash(users[email], password):
        # Log the user in and create a session
        session['user_id'] = users[email] 
        return jsonify({'message': 'Logged in successfully'}), 201
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# Log out the current user
@app.route('/logout', methods=['POST'])
def logout():
    if len(session) == 0:
        return jsonify({'message': 'User is not logged in'}), 401
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 201

# Check the current user's authentication status
@app.route('/auth_status', methods=['GET'])
def auth_status():
    if 'user_id' in session:
        return jsonify({'authenticated': True})
    else:
        return jsonify({'authenticated': False})



if __name__ == '__main__':
    app.run(debug=True)
