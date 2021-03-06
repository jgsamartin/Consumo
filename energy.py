import csv
import numpy as np
import random
import tensorflow as tf

# Parámetros de configuración de la red
pTest = 0.2             # % Datos usados para la validación
pTrain = 1 - pTest      # % Datos usados para el entrenamiento

# Leemos el fichero CSV
data = []
with open('./energy-data.csv', 'r') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        data.append(list(map(int, row)))

# Ordenamos aleatoriamente el array
np.random.shuffle(data)
data = np.array(data, dtype=float)

# Creamos conjunto de entrenamiento y de validación
limite = round(pTest * len(data))

x_test = data[:limite, :2]
y_test = data[:limite, 2]
x_train = data[limite:, :2]
y_train = data[limite:, 2]

# Llevamos los valores al intervalo [0, 1]
y_train, y_test = y_train / np.amax(y_train), y_test / np.amax(y_test)

# Define the network by stacking layers
network = tf.keras.models.Sequential([
  #tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(2, input_shape=[2], activation='relu'),
  tf.keras.layers.Dense(10, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(1)
])

# Create the training system 
network.compile(optimizer='adam',
                loss='mse',
                metrics=['accuracy'])

# Train the network with train data
network.fit(x_train, y_train, epochs=5)

# Evaluate the network on test data
loss, accuracy = network.evaluate(x_test, y_test)