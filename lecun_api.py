from flask import Flask, render_template, request
app = Flask(__name__)

import sqlite3

"""Authenticator for Login and Signup"""
import authenticator

## GLOBAL VARS
prediction = 0
nearest_customers = []
chance_of_buying = 0
authenticator_obj = authenticator.auth(app)


"""Rough KNN Model"""
from model import knn


"""## Flask"""
@app.route('/signup', methods=["GET", "POST"])
def signup_page():
    global authenticator_obj
    if request.method == 'POST':
        username_received = request.form['username']
        password_received = request.form['password']
        if authenticator_obj.SignUp(username_received, password_received):
            return render_template('login.html')
    return render_template('signup.html')

@app.route('/login', methods=["GET", "POST"])
def login_page():
    global authenticator_obj
    
    if authenticator_obj.Is_already_logged_in()[0]: 
        return render_template("input.html", username = authenticator_obj.Is_already_logged_in()[1])

    if request.method == 'POST':
        username_received = request.form['username']
        password_received = request.form['password']
        if authenticator_obj.Login(username_received,password_received):
            return render_template("input.html", username = username_received)
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