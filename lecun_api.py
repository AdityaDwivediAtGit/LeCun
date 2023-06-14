from flask import Flask, render_template, request
app = Flask(__name__)

import sqlite3

## GLOBAL VARS
prediction = 0
nearest_customers = []
chance_of_buying = 0


"""Rough KNN Model"""
from model import knn


"""## Flask"""

@app.route('/', methods=['GET', 'POST'])
def input_page():
    global prediction
    global nearest_customers
    global chance_of_buying

    if request.method == 'POST':
        age = int(request.form['age'])
        salary = int(request.form['salary'])
        prediction, nearest_customers, chance_of_buying = knn(age, salary)
        prediction = "YES" if prediction == 1 else "NO"
        return render_template('output.html', age=age, salary=salary, prediction=prediction+",\t"+str(chance_of_buying*100)+"% chances of buying", nearest_customers=nearest_customers, data_saved = "Has the new customer purchased the car ?")
    return render_template('input.html')

@app.route('/output', methods=['GET', 'POST'])
def output_page():
    global prediction
    global nearest_customers
    global chance_of_buying

    age = int(request.form['age'])
    salary = int(request.form['salary'])
    
    ###### another thread for parallel operation (since flask performs parallel operations)
    conn = sqlite3.connect('car_prediction.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        button_id = request.form['button_id']
        purchase = 1 if button_id == 'yes' else 0
        # Update the purchase status in the database
        cursor.execute('INSERT INTO customers (Age, EstimatedSalary, Purchased) VALUES (?, ?, ?)', (age, salary, purchase))
        conn.commit()   


    return render_template('output.html', age=age, salary=salary, prediction=prediction+",\t"+str(chance_of_buying*100)+"% chances of buying", nearest_customers=nearest_customers, data_saved = "Data Saved to DB")

if __name__ == '__main__':
    app.run(debug = True, port = 5001)