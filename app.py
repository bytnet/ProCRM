from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def index():
    return render_template('index.html')

#login
@app.route('/login')
def login():
    return render_template('auth/index.html')

if __name__ == '__main__':
    #run on     LAN
    app.run(host='0.0.0.0', port=5000, debug=True)
