from flask import Flask, render_template, request
app = Flask(__name__)

import sqlite3
# from sklearn.neighbors import KNeighborsClassifier

# conn = sqlite3.connect('car_prediction.db')
# cursor = conn.cursor()

## GLOBAL VARS
prediction = 0
nearest_customers = []
chance_of_buying = 0

# """## Train KNN Model"""

# # dataset = inputs, label = output column
# def load_dataset():
#     dataset = []
#     labels = []
#     ###### another thread for parallel operation (since flask performs parallel operations)
#     conn = sqlite3.connect('car_prediction.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT Age, EstimatedSalary, Purchased FROM customers')
#     rows = cursor.fetchall()
#     for row in rows:
#         dataset.append([row[0], row[1]])
#         labels.append(row[2])
#     return dataset, labels

# def train_model():
#     dataset, labels = load_dataset()
#     model = KNeighborsClassifier(n_neighbors=20)
#     model.fit(dataset, labels)
#     return model




"""Rough KNN Model"""
from model import knn


"""## Flask"""

@app.route('/', methods=['GET', 'POST'])
def input_page():
    global prediction
    global nearest_customers
    global chance_of_buying


    if request.method == 'POST':
        # global model
        # model = train_model()
        age = int(request.form['age'])
        salary = int(request.form['salary'])
        prediction, nearest_customers, chance_of_buying = knn(age, salary)
        # print(nearest_customers)
        # ##### another thread for parallel operation (since flask performs parallel operations)
        # conn = sqlite3.connect('car_prediction.db')
        # cursor = conn.cursor()
        # cursor.execute('SELECT Age, EstimatedSalary, Purchased FROM customers')
        # rows = cursor.fetchall()
        # nearest_customers = [{'Age': row[0], 'EstimatedSalary': row[1], "Purchased": row[2]} for row in rows]       #### Yaha nearest customers daalna hai model se, this is temporary\
        # # distances, nearest_customers = get_nearest_neighbors(model, data_point=[[age, salary]], k = 20)
        # # print(nearest_customers)
        prediction = "YES" if prediction == 1 else "NO"
        return render_template('output.html', age=age, salary=salary, prediction=prediction+",\t"+str(chance_of_buying*100)+"percent chances of buying", nearest_customers=nearest_customers, data_saved = "Has the new customer purchased the car ?")
    return render_template('input.html')

@app.route('/output', methods=['GET', 'POST'])
def output_page():
    global prediction
    global nearest_customers
    global chance_of_buying

    # model = train_model()
    age = int(request.form['age'])
    salary = int(request.form['salary'])
    # prediction = request.form['prediction']
    
    ###### another thread for parallel operation (since flask performs parallel operations)
    conn = sqlite3.connect('car_prediction.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        button_id = request.form['button_id']
        purchase = 1 if button_id == 'yes' else 0
        # Update the purchase status in the database
        cursor.execute('INSERT INTO customers (Age, EstimatedSalary, Purchased) VALUES (?, ?, ?)', (age, salary, purchase))
        conn.commit()   

    # # Fetching full db again #################################################################
    # cursor.execute('SELECT Age, EstimatedSalary, Purchased FROM customers')
    # rows = cursor.fetchall()
    # nearest_customers = [{'Age': row[0], 'EstimatedSalary': row[1], "Purchased": row[2]} for row in rows]       #### Yaha nearest customers daalna hai model se, this is temporary

    return render_template('output.html', age=age, salary=salary, prediction=prediction+",\t"+str(chance_of_buying*100)+"% chances of buying", nearest_customers=nearest_customers, data_saved = "Data Saved to DB")

if __name__ == '__main__':
    app.run(debug = True, port = 5001)