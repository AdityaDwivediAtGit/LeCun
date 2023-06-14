import sqlite3
from sklearn.neighbors import KNeighborsClassifier

conn = sqlite3.connect('car_prediction.db')
cursor = conn.cursor()

# GLOBAL DATASET
dataset = []
labels = []

def load_dataset():
    global dataset
    global labels
    ###### another thread for parallel operation (since flask performs parallel operations)
    conn = sqlite3.connect('car_prediction.db')
    cursor = conn.cursor()
    cursor.execute('SELECT Age, EstimatedSalary, Purchased FROM customers')
    rows = cursor.fetchall()
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
    dataset, labels = load_dataset()
    model = KNeighborsClassifier(n_neighbors=20)
    model.fit(dataset, labels)
    return model

def get_nearest_neighbors(model, data_point, k):
    distances, indices = model.kneighbors(data_point, n_neighbors=k)
    return distances, indices

def knn(age, salary):
    model = train_model()
    data_point = [[age, salary]]
    prediction = int(model.predict(data_point))
    distances, indices = get_nearest_neighbors(model, data_point, k=20)

    nearest_neighbors = []
    for i in indices[0]:
        neighbor = dataset[i]+[int(labels[i])]  # Assuming 'dataset' is accessible here
        nearest_neighbors.append(neighbor)

    return (prediction, nearest_neighbors, one_counter(nearest_neighbors)/len(nearest_neighbors))

# print(knn(24,30000))