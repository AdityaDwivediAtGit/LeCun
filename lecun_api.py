from flask import Flask, render_template, request, send_from_directory
app = Flask(__name__)

import sqlite3

"""Authenticator for Login and Signup"""
import authenticator

"""Discord send verification message"""
import random

## GLOBAL VARS
prediction = 0
nearest_customers = []
chance_of_buying = 0
authenticator_obj = authenticator.auth(app)
verification_code = 0
username = ""


"""Rough KNN Model"""
from model import knn


"""## Flask"""

# HOSTING IMAGES
@app.route('/images/<path:filename>')
def get_image(filename):
    return send_from_directory('static', filename)



@app.route('/signup', methods=["GET", "POST"])
def signup_page():
    global authenticator_obj
    if request.method == 'POST':
        username_received = request.form['username']
        password_received = request.form['password']
        if authenticator_obj.SignUp(username_received, password_received):
            return render_template('login.html')
        else:
            return render_template('signup.html', err = "User already exists !")
    return render_template('signup.html')

@app.route('/verify', methods=["GET", "POST"])
def verification_page():
    global authenticator_obj
    global verification_code
    global username

    if request.method == 'POST':
        verification_code_received = int(request.form['verification_code_name'])
        print("/verify post", verification_code_received, verification_code) #############
        if verification_code_received == verification_code:
            authenticator_obj.create_cookie(username = username)
            return render_template("input.html", username = username)
    return render_template('login.html', incorrect_pass="Incorrect Verification Code !")

@app.route('/login', methods=["GET", "POST"])
def login_page():
    global authenticator_obj
    global verification_code
    global username
    
    if authenticator_obj.Is_already_logged_in()["logged_in"]: 
        return render_template("input.html", username = username)

    if request.method == 'POST':
        username_received = request.form['username']
        username = username_received
        password_received = request.form['password']
        if authenticator_obj.Login(username_received,password_received):

            # generate verification code
            verification_code = random.randint(100000, 999999)

            #send code
            # temporary webhook, replace this from db later, every login has different webhook
            f = open("webhook_url.txt", 'r')
            webhook_url = f.read()
            f.close()
            if authenticator_obj.sent_discord_verification_message(discord_webhook_url = webhook_url, verification_code = verification_code):
                # return render_template("input.html", username = username_received)
                return render_template("verification.html")
        else:
            return render_template('login.html', incorrect_pass="Username or password is incorrect")
    return render_template('login.html')


@app.route('/', methods=["GET"])
def homepage():
    return render_template('homepage.html')

@app.route('/input', methods=['GET', 'POST'])
def input_page():
    global prediction
    global nearest_customers
    global chance_of_buying

    if request.method == 'POST':
        # if logout button is pressed
        print(request.form)
        if "logout_button_name" in request.form:
            authenticator_obj.Logout()
            return render_template('login.html', incorrect_pass="You're successfully logged out.")

        # if age or salary field is empty
        if (not request.form['age']) or (not request.form['salary']):
            return render_template('input.html', err="Enter Age and Salary.")
        
        age = int(request.form['age'])
        salary = int(request.form['salary'])
        prediction, nearest_customers, chance_of_buying = knn(age, salary)
        prediction = "YES" if prediction == 1 else "NO"
        return render_template('output.html', age=age, salary=salary, prediction=prediction+",\t"+str(chance_of_buying*100)+"% chances of buying", nearest_customers=nearest_customers, data_saved = "Has the new customer purchased the car ?")
    return "Please Login !"

@app.route('/output', methods=['GET', 'POST'])
def output_page():
    global prediction
    global nearest_customers
    global chance_of_buying

    if request.method == 'POST':
        age = int(request.form['age'])
        salary = int(request.form['salary'])
        
        ###### another thread for parallel operation (since flask performs parallel operations)
        conn = sqlite3.connect('car_prediction.db')
        cursor = conn.cursor()

        button_id = request.form['button_id']
        purchase = 1 if button_id == 'yes' else 0
        # Update the purchase status in the database
        cursor.execute('INSERT INTO customers (Age, EstimatedSalary, Purchased) VALUES (?, ?, ?)', (age, salary, purchase))
        conn.commit()
        conn.close()
        return render_template('output.html', age=age, salary=salary, prediction=prediction+",\t"+str(chance_of_buying*100)+"% chances of buying", nearest_customers=nearest_customers, data_saved = "Data Saved to DB")
    else:
        return "Please Login provide input first !"

if __name__ == '__main__':
    app.run(debug = True, port = 5001)