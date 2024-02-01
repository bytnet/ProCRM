from flask import Flask, render_template, request, jsonify, session, url_for, redirect
import psycopg2
import hashlib

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
    password = password.encode("utf-8")
    password = hashlib.sha256(password).hexdigest()

    #check if fields are empty
    if not username or not name or not email or not password:
        return jsonify({'status': 'error', 'message': 'Missing parameters. Please try again.'}), 400  # Bad Request
    
    # check if email is valid
    if '@' not in email:
        return jsonify({'status': 'error', 'message': 'Invalid email. Please try again.'}), 400  # Bad Request

    # check if username exists
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        return jsonify({'status': 'error', 'message': 'Username already exists. Please try again.'}), 409  # Conflict
    
    # check if email exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        return jsonify({'status': 'error', 'message': 'Email already exists. Please try again.'}), 409  # Conflict
    
    # insert into db with error handling
    try:
        cursor.execute("INSERT INTO users (username, name, email, password) VALUES (%s, %s, %s, %s)", (username, name, email, password))
    except:
        return jsonify({'status': 'error', 'message': 'An error occurred while creating your account. Please try again.'}), 500  # Internal Server Error
    
    # success
    return jsonify({'status': 'success', 'message': 'Account created successfully!'}), 201  # Created


@app.route('/login', methods=['POST'])
def login():
    
    username = request.form['username']
    password = request.form['password']
    
    #check if fields are empty
    if not username or not password:
        print("Missing parameters. Please try again.")
        return jsonify({'status': 'error', 'message': 'Missing parameters. Please try again.'}),400 
    
    #check if username exists or email exists
    cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username,username,))
    details = cursor.fetchone()
    if not details:
        print("Username does not exist. Please try again.")
        return jsonify({'status': 'error', 'message': 'Username does not exist. Please try again.'}),400 

    user = details[0]
    password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    
    #check if password is correct
    if details[1] != password:
        return jsonify({'status': 'error', 'message': 'Incorrect password. Please try again.'}) ,400 
    else:
        session['user'] = user  # user[0] is the user's ID or a unique identifier
        session['username'] = details[1]
        session['name'] = details[2]
        session['email'] = details[3]
        #success
        print("Logged in successfully!") 
        return jsonify({'status': 'success', 'message': 'Logged in successfully!'}), 201

"""
CREATE TABLE contacts (
    contact_id SERIAL PRIMARY KEY,
    username INT REFERENCES users(username),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    phone_number VARCHAR(20),
    job_title VARCHAR(100),
    company VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

"""

@app.route('/contacts', methods=['POST'])
def contacts():
    #get username from session
    username = session['username']
    operation = request.form['operation']

    #check if fields are empty
    if not operation:
        return jsonify({'status': 'error', 'message': 'Missing parameters. Please try again.'})
    
    #get all contacts if operation is get
    if operation == 'view':
        cursor.execute("SELECT * FROM contacts WHERE username = %s", (username,))
        contacts = cursor.fetchall()
        return jsonify({'status': 'success', 'message': 'Contacts retrieved successfully!', 'contacts': contacts})
    
    #if operation is add
    if operation == 'add':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        job_title = request.form['job_title']
        company = request.form['company']

        #check if fields are empty
        if not first_name or not last_name:
            return jsonify({'status': 'error', 'message': 'Missing parameters. Please try again.'})
        
        #insert into db with error handling
        try:
            cursor.execute("INSERT INTO contacts (username, first_name, last_name, email, phone_number, job_title, company) VALUES (%s, %s, %s, %s, %s, %s, %s)", (username, first_name, last_name, email, phone_number, job_title, company))
        except:
            return jsonify({'status': 'error', 'message': 'An error occured while adding your contact. Please try again.'})
        
        #success
        return jsonify({'status': 'success', 'message': 'Contact added successfully!'})
    
    #if operation is update
    if operation == 'update':
        contact_id = request.form['contact_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        job_title = request.form['job_title']
        company = request.form['company']

        #check if fields are empty
        if not contact_id or not first_name or not last_name:
            return jsonify({'status': 'error', 'message': 'Missing parameters. Please try again.'})
        
        #update db with error handling
        try:
            cursor.execute("UPDATE contacts SET first_name = %s, last_name = %s, email = %s, phone_number = %s, job_title = %s, company = %s WHERE contact_id = %s", (first_name, last_name, email, phone_number, job_title, company, contact_id))
        except:
            return jsonify({'status': 'error', 'message': 'An error occured while updating your contact. Please try again.'})
        
        #success
        return jsonify({'status': 'success', 'message': 'Contact updated successfully!'})
    
    #if operation is delete
    if operation == 'delete':
        contact_id = request.form['contact_id']

        #check if fields are empty
        if not contact_id:
            return jsonify({'status': 'error', 'message': 'Missing parameters. Please try again.'})
        
        #delete from db with error handling
        try:
            cursor.execute("DELETE FROM contacts WHERE contact_id = %s", (contact_id,))
        except:
            return jsonify({'status': 'error', 'message': 'An error occured while deleting your contact. Please try again.'})
        
        #success
        return jsonify({'status': 'success', 'message': 'Contact deleted successfully!'})

"""
CREATE TABLE company (
    id SERIAL PRIMARY KEY,-- Assuming 'id' is an auto-incrementing integer
    username VARCHAR(20) REFERENCES users(username),
name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    phone VARCHAR(50),
    email VARCHAR(255),
    industry VARCHAR(100),
    website VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);"""

@app.route('/company', methods=['POST'])
def company():
    #get username from session
    username = session['username']
    operation = request.form['operation']

    #check if fields are empty
    if not operation:
        return jsonify({'status': 'error', 'message': 'Missing parameters. Please try again.'})
    
    #get all companies if operation is get
    if operation == 'view':
        cursor.execute("SELECT * FROM company WHERE username = %s", (username,))
        companies = cursor.fetchall()
        return jsonify({'status': 'success', 'message': 'Companies retrieved successfully!', 'companies': companies})
    
    #if operation is add
    if operation == 'add':
        name = request.form['name']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        postal_code = request.form['postal_code']
        phone = request.form['phone']
        email = request.form['email']
        industry = request.form['industry']
        website = request.form['website']

        #check if fields are empty
        if not name:
            return jsonify({'status': 'error', 'message': 'Missing parameters. Please try again.'})
        
        #insert into db with error handling
        try:
            cursor.execute("INSERT INTO company (username, name, address, city, state, country, postal_code, phone, email, industry, website) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (username, name, address, city, state, country, postal_code, phone, email, industry, website))
        except:
            return jsonify({'status': 'error', 'message': 'An error occured while adding your company. Please try again.'})
        
        #success
        return jsonify({'status': 'success', 'message': 'Company added successfully!'})
    
    #if operation is update
    if operation == 'update':
        company_id = request.form['company_id']
        name = request.form['name']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        postal_code = request.form['postal_code']
        phone = request.form['phone']
        email = request.form['email']
        industry = request.form['industry']
        website = request.form['website']

        #check if fields are empty
        if not company_id or not name:
            return jsonify({'status': 'error', 'message': 'Missing parameters. Please try again.'})
        
        #update db with error handling
        try:
            cursor.execute("UPDATE company SET name = %s, address = %s, city = %s, state = %s, country = %s, postal_code = %s, phone = %s, email = %s, industry = %s, website = %s WHERE id = %s AND username = %s", (name, address, city, state, country, postal_code, phone, email, industry, website, company_id, username))
        except:
            return jsonify({'status': 'error', 'message': 'An error occured while updating your company. Please try again.'})
        
        #success
        return jsonify({'status': 'success', 'message': 'Company updated successfully!'})
    
    #if operation is delete
    if operation == "delete":
        company_id = request.form['company_id']

        #check if fields are empty
        if not company_id:
            return jsonify({'status': 'error', 'message': 'Missing parameters. Please try again.'})
        
        #delete from db with error handling, if company belongs to user
        try:
            cursor.execute("DELETE FROM company WHERE id = %s AND username = %s", (company_id, username))
        except:
            return jsonify({'status': 'error', 'message': 'An error occured while deleting your company. Please try again.'})
        
        #success
        return jsonify({'status': 'success', 'message': 'Company deleted successfully!'})

"""
 CREATE TABLE leads (
      lead_id SERIAL PRIMARY KEY,
      username INT REFERENCES users(username),
      lead_name VARCHAR(100) NOT NULL,
      company_name VARCHAR(100),
      industry VARCHAR(50),
      contact_person VARCHAR(100),
      email VARCHAR(100),
      phone_number VARCHAR(20),
      status VARCHAR(20) DEFAULT 'Open',
      source VARCHAR(50),
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
"""

@app.route('/leads', methods=['POST'])
def leads():
    #get username from session
    username = session['username']
    operation = request.form['operation']

    #check if fields are empty
    if not operation:
        return jsonify({'status': 'error', 'message': 'Missing parameters. Please try again.'})
    
    #get all leads if operation is get
    if operation == 'view':
        cursor.execute("SELECT * FROM leads WHERE username = %s", (username,))
        leads = cursor.fetchall()
        return jsonify({'status': 'success', 'message': 'Leads retrieved successfully!', 'leads': leads})
    
    #if operation is add
    if operation == 'add':
        lead_name = request.form['lead_name']
        company_name = request.form['company_name']
        industry = request.form['industry']
        contact_person = request.form['contact_person']
        email = request.form['email']
        phone_number = request.form['phone_number']
        status = request.form['status']
        source = request.form['source']

        #check if fields are empty
        if not lead_name:
            return jsonify({'status': 'error', 'message': 'Missing parameters. Please try again.'})
        
        #insert into db with error handling
        try:
            cursor.execute("INSERT INTO leads (username, lead_name, company_name, industry, contact_person, email, phone_number, status, source) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (username, lead_name, company_name, industry, contact_person, email, phone_number, status, source))
        except:
            return jsonify({'status': 'error', 'message': 'An error occured while adding your lead. Please try again.'})
        
        #success
        return jsonify({'status': 'success', 'message': 'Lead added successfully!'})
    
    #if operation is update
    if operation == 'update':
        lead_id = request.form['lead_id']
        lead_name = request.form['lead_name']
        company_name = request.form['company_name']
        industry = request.form['industry']
        contact_person = request.form['contact_person']
        email = request.form['email']
        phone_number = request.form['phone_number']
        status = request.form['status']
        source = request.form['source']

        #check if fields are empty
        if not lead_id or not lead_name:
            return jsonify({'status': 'error', 'message': 'Missing parameters. Please try again.'})
        
        #update db with error handling
        try:
            cursor.execute("UPDATE leads SET lead_name = %s, company_name = %s, industry = %s, contact_person = %s, email = %s, phone_number = %s, status = %s, source = %s WHERE lead_id = %s", (lead_name, company_name, industry, contact_person, email, phone_number, status, source, lead_id))
        except:
            return jsonify({'status': 'error', 'message': 'An error occured while updating your lead. Please try again.'})
        
        #success
        return jsonify({'status': 'success', 'message': 'Lead updated successfully!'})
    

#frontend
#login
@app.route('/auth', methods=["GET"])
def auth():
    return render_template('auth/index.html')

#dashboard
@app.route('/dashboard')
def dashboard():
    # Check if user is in session
    if 'user' not in session:
        return redirect(url_for('auth'))
    
    name = session['name']

    return render_template('dashboard/index.html', name=name)

#contacts
@app.route('/dashboard/contacts', methods=["GET"])
def contacts_page():
    #set variables
    username = "mvishok"
    name = "Vishok Manikantan"
    email = "mvishok2005@gmail.com"

    return render_template('dashboard/contacts.html', username=username, name=name, email=email)


# Set a secret key for session management
app.secret_key = '69nExkjwgX'  # Replace with a strong, random key

# Configure session type
app.config['SESSION_TYPE'] = 'filesystem'


if __name__ == '__main__':
    # Run the application
    app.run(host='0.0.0.0', port=5000, debug=True)
