from flask import Flask, render_template, request, jsonify, session, url_for
import psycopg2
import bcrypt

connStr = "postgresql://vishokmanikantan:IRYuKPmoZk75@ep-fancy-mouse-a12n6vlg.ap-southeast-1.aws.neon.tech/procrm?sslmode=require"

conn = psycopg2.connect(connStr)
cursor = conn.cursor()
conn.autocommit = True

app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def index():
    return render_template('index.html')

#backend
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    #hash password
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    #check if fields are empty
    if not username or not name or not email or not password:
        return jsonify({'status': 'error', 'message': 'Missing parameters. Please try again.'})
    
    #check if email is valid
    if '@' not in email:
        return jsonify({'status': 'error', 'message': 'Invalid email. Please try again.'})

    #check if username exists
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        return jsonify({'status': 'error', 'message': 'Username already exists. Please try again.'})
    
    #check if email exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        return jsonify({'status': 'error', 'message': 'Email already exists. Please try again.'})
    
    #insert into db with error handling
    try:
        cursor.execute("INSERT INTO users (username, name, email, password) VALUES (%s, %s, %s, %s)", (username, name, email, password))
    except:
        return jsonify({'status': 'error', 'message': 'An error occured while creating your account. Please try again.'})
    
    #success
    return jsonify({'status': 'success', 'message': 'Account created successfully!'}) 

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    #check if fields are empty
    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Missing parameters. Please try again.'})
    
    #check if username exists
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if not user:
        return jsonify({'status': 'error', 'message': 'Username does not exist. Please try again.'})
    
    #check if password is correct
    if not bcrypt.checkpw(password.encode('utf-8'), user[4].encode('utf-8')):
        return jsonify({'status': 'error', 'message': 'Incorrect password. Please try again.'})
    
    #create session
    session['user'] = user[0]
    session['username'] = user[1]
    session['name'] = user[2]
    session['email'] = user[3]

    #success
    return jsonify({'status': 'success', 'message': 'Logged in successfully!'})

#login
@app.route('/auth', methods=["GET"])
def auth():
    return render_template('auth/index.html')

if __name__ == '__main__':
    #run on LAN
    app.run(host='0.0.0.0', port=5000, debug=True)
