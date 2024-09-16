# -*- coding: utf-8 -*-
"""Digit recognizer KERAS .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1OoShaOt1-QG5mslp_uCppSyMlfZ-KOzU

## Importación de librería TensorFlow
"""

import tensorflow as tf
print("TensorFlow version:", tf.__version__)

"""## Acceder al conjunto de datos MNIST dentro del módulo tensrflow.keras.datasets.

The MNIST database of handwritten digits has a training set of 60,000 examples, and a test set of 10,000 examples.
"""

#Acceder al conjunto de datos de MNIST
mnist = tf.keras.datasets.mnist

#creación de dos tuplas: para train y test

(x_train, y_train), (x_test, y_test) = mnist.load_data()


# x_train contiene las imágenes de entrenamiento(60k imágenes de 28x28 píxeles cada una)
# y_train contiene las etiquetas de las imágenes de entrenamiento (num del 0 al 9)
# x_test contiene las imágenes de prueba (10,000 imágenes de 28x28 píxles)
# y_test contiene las etiquetas de las imágenes de prueba

"""Normalización de datos: x_train y x_test

x_test y x_train contiene imágenes de dígitos escritos a mano, donde cada píxel de las imágenes tiene un calor de entre 0 y 255. Dichos valores representan la intensidad de color de cada píxel (0=nego, 255=blanco).

Normalización:
Dividir cada valor de píxel por 255 convierte todos los valores de los píxles del rango original (0 a 255) a un rango entre 0 y 1.

  un píxel con valor 0 (negro) se convertirá en 0/255 = 0.0
  un píxel con valor 255 (blanco) se convertirá en 255/255 = 1.0
  un píxel con valor 128 (gris medio) se convertirá en 128/255 = 0.502

La mayoría de los modelos de aprendizaje automático, especialmente las redes neuronales, funcionan mejor y aprenden más rápido cuando los datos están en un rango pequeño (por ejemplo, entre 0 y 1 o -1 y 1).
"""

#normalizar

x_train, x_test = x_train / 255.0, x_test / 255.0

"""## Modelo secuencial:
"Sequential" significa que las capas del modelo se apilan unas tras otras, de manera secuencial. Es decir, construir un modelo en bloques, donde cada capa está conectada directamente con la siguiente.
"""

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)), #toma imagen de 28x28 y lo aplana en un vecto de 784; 2D-->1D
  tf.keras.layers.Dense(128, activation='relu'), #esta capa tiene 128 neuronas que recibe valor de capa anterior; usa funcion ReLU para aprender relaciones no lineales
  tf.keras.layers.Dropout(0.2), #apaga 20% de neuronas en cada paso de entrenamiento, preveien overfitting
  tf.keras.layers.Dense(10) #Capa de salida, tiene 10 neuronas, una para cada posble clase: 0 al 9,
])

"""Vamos a tomar el dato del conjunto de entrenamiento, el modelo predice su clase, y luego imprimimos la predicción."""

predictions = model(x_train[:1]).numpy() #toma el primer conjunyo de datos de entrenamiento y lo pasa al modelo, luego convierte el TENSOR en un ARRAY
predictions #Ver la predicción: logits, no son probabilidades

# La función SOFTMAX convierte las predicciones (LOGITS) y los convierte en probabilidades, es decir, toma los resultados crudos y los transforma en probabilidades que suma 1,
# es decir, convierte el resultado del Tensor Flow a un Array de Numpy

tf.nn.softmax(predictions).numpy()

"""De lo anterior, pondré de ejemplo:
Si el modelo predijo [2.0, 1.0, 0.1] para tres clases, el softmax lo convierte en algo como [0.7, 0.2, 0.1], lo que significa que el modelo cree que la primera clase tiene un 70% de probabilidad de ser correcta, la segunda un 20%, y la tercera un 10%.
"""

# Crear una función de pérdida(loss) para entrenar un modelo de clasificación en TensorFlow y Keras.

loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

"""La función de pérdida para problemas de clasificación multicategoría y que las etiquetas son números enteros(no vectores). El término "SparseCategoricalCrossentropy" se refiere a que las etiquetas están en forma de enteros simples (0,1,2...) en lugar de ONE-HOT ENCODED: 0 y 1.

CategoricalCrossentropy calcula qué tan "bien" las predicciones del modelo coinciden con las etiquetas verdaderas usando una medida conocida como entropía cruzada.

El argumento from_logits=True indica que las salidas del modelo son logits, es decir, valores crudos que aún no han pasado por una función de activación como softmax (que convierte los logits en probabilidades).
"""

loss_fn(y_train[:1], predictions).numpy()

#Preparar el modelo para el proceso de entrenamiento

model.compile(optimizer='adam',
              loss=loss_fn,
              metrics=['accuracy'])

""""model.compile()" configurar el modelo antes de entrenarlo, especificar algoritmo de optimización: adam --> muy popular para ajustar pesos dle modelo eficientemente-->; la función de pérdida: loss_fn --> mide qué tan bien el modelo precide las cas clases correctas; y las métricas: ['accuracy'] --> forma en que evaluas el rendimeinto del modelo."""

# entrena el modelo durante 5 ciclos (epochs), usando las imágenes y etiquetas de
# entrenamiento para que el modelo aprenda a reconocer y clasificar correctamente los dígitos

model.fit(x_train, y_train, epochs=5) #epochs: el modelo va a pasar por todos los datos 5 veces para intentar mejorar su aprendizaje en cada pasada.

""""model.fit()" comando de entreno del modelo; x_train: son las imágenes de entrenamiento, entradas que usa el modelo para aprender, los dígitos del data set MNIST; y_train: son etiquetas de entrenamiento, cada imagen tiene una etiqueta de 0 al 9; epochs: indica las veces que el modelo va a revisar todo el conjunto de datos durante el entrenamiento."""

#evalúa qué tan bien el modelo clasifica las imágenes del conjunto de prueba (datos no usados en el entrenamiento) y muestra los resultados

model.evaluate(x_test,  y_test, verbose=2)

""""model.evaluate()" : mide el rendimiento del modelo con datos que no ha visto antes (los datos de prueba).
"x_test": Son las imágenes de prueba que el modelo no ha usado para entrenar
"y_test": Son las etiquetas reales de las imágenes de prueba
"verbose=2":ontrola cuánta información se imprime; El valor 2 muestra un resumen básico con los resultados de la evaluación
"""

#crea un modelo que da como resultado probabilidades en lugar de puntajes de salida


probability_model = tf.keras.Sequential([
  model,
  tf.keras.layers.Softmax()
])

"""* "tf.keras.Sequential([])" --> Crea un modelo secuencial, que significa que las capas se ejecutan en orden, una después de otra.

* "model" --> El modelo entrenado original se incluye aquí, que ya puede hacer predicciones, pero esas predicciones aún no son probabilidades (solo números o "logits").

* "tf.keras.layers.Softmax()" --> Agrega una capa Softmax que toma los resultados del modelo y los convierte en probabilidades (números entre 0 y 1) para cada posible clase.
"""

# toma las primeras 5 imágenes de prueba (x_test[:5]) y las pasa a través del modelo de
#  probabilidad para obtener las predicciones en forma de probabilidades.

predictions = probability_model(x_test[:5])
predictions

# Muestra las predicciones
print("Predicciones:", predictions.numpy())

# Encuentra la etiqueta predicha (la clase con la mayor probabilidad)
predicted_labels = np.argmax(predictions.numpy(), axis=1)
print("Etiquetas predichas:", predicted_labels)