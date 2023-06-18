import sqlite3
from sklearn.neighbors import KNeighborsClassifier

conn = sqlite3.connect('car_prediction.db')
cursor = conn.cursor()

# GLOBAL VARS
dataset = []
labels = []
K = 0

def load_dataset():
    global dataset
    global labels
    global K
    ###### another thread for parallel operation (since flask performs parallel operations)
    conn = sqlite3.connect('car_prediction.db')
    cursor = conn.cursor()
    cursor.execute('SELECT Age, EstimatedSalary, Purchased FROM customers')
    rows = cursor.fetchall()
    conn.close()

    dataset = []
    labels = []
    K = int(len(rows)**0.5)    # sqrt of the number of customers
    for row in rows:
        dataset.append([row[0], row[1]])
        labels.append(row[2])
    return dataset, labels

def one_counter(nearest_neighbors):
    count = 0
    for l in nearest_neighbors:
        if l[2]: count+=1
    return count


from sklearn.neighbors import KNeighborsClassifier

def train_model():
    global K
    dataset, labels = load_dataset()
    model = KNeighborsClassifier(n_neighbors=K)
    model.fit(dataset, labels)
    return model

def get_nearest_neighbors(model, data_point, k):
    distances, indices = model.kneighbors(data_point, n_neighbors=k)
    return distances, indices

def knn(age, salary):
    model = train_model()
    data_point = [[age, salary]]
    prediction = int(model.predict(data_point))
    distances, indices = get_nearest_neighbors(model, data_point, k=K)

    nearest_neighbors = []
    for i in indices[0]:
        neighbor = dataset[i]+[int(labels[i])]  # Assuming 'dataset' is accessible here
        nearest_neighbors.append(neighbor)
    probability = round(one_counter(nearest_neighbors)/K , 4+2) # this gives probability in range [0,1], so we have to round it to 6 to get 4 digit precision (due to x100)
    return (prediction, nearest_neighbors, probability)

# print(knn(24,30000))