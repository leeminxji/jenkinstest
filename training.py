import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os
from typing import Tuple


def load_dataset() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    train_dataset = np.load('./data/train_dataset.npy')
    valid_dataset = np.load('./data/valid_dataset.npy')
    time_train = np.load('./data/time_train.npy')
    time_valid = np.load('./data/time_valid.npy')
    return train_dataset, valid_dataset, time_train, time_valid


def windowed_dataset(
        series: np.ndarray, window_size: int, batch_size: int, shuffle_buffer=None):
    series = tf.expand_dims(series, axis=-1)
    dataset = tf.data.Dataset.from_tensor_slices(series)
    dataset = dataset.window(window_size + 1, shift=1, drop_remainder=True)
    dataset = dataset.flat_map(lambda window: window.batch(window_size + 1))

    if shuffle_buffer is not None:
        dataset = dataset.shuffle(shuffle_buffer)

    dataset = dataset.map(lambda window: (window[:-1], window[-1]))
    dataset = dataset.batch(batch_size).prefetch(1)
    return dataset


train_dataset, valid_dataset, time_train, time_valid = load_dataset()

# Data is now numpy array
window_size = 24
batch_size = 12
shuffle_buffer_size = 48
dataset = windowed_dataset(train_dataset, window_size,
                           batch_size, shuffle_buffer_size)
valid_dataset = windowed_dataset(
    valid_dataset, window_size, batch_size, shuffle_buffer_size)

# Using RNN for Sequence Modeling
model = tf.keras.models.Sequential([
    tf.keras.layers.InputLayer((window_size, 1)),
    tf.keras.layers.Bidirectional(
        tf.keras.layers.GRU(100, return_sequences=True,
                            dropout=0.1, recurrent_dropout=0.1)),
    tf.keras.layers.Bidirectional(
        tf.keras.layers.GRU(100, dropout=0.1, recurrent_dropout=0.1)),
    tf.keras.layers.Dense(1),
])


optimizer = tf.keras.optimizers.SGD(learning_rate=1.5e-6, momentum=0.9)
model.compile(loss=tf.keras.losses.Huber(),
              optimizer=optimizer, metrics=["mae"])

model.summary()

# Pretrained Model
model_path = "model/train.ckpt"

if os.path.exists("model/checkpoint"):
    model.load_weights(model_path)
    print("Loaded saved model from '{}'".format(model_path))

history = model.fit(dataset, epochs=10, verbose=1,
                    validation_data=valid_dataset)

model.save_weights(model_path)

# Exploring the accuracy and loss of model
fig, loss_ax = plt.subplots()

loss_ax.plot(history.history['loss'], 'tab:red', label='train_loss')
loss_ax.plot(history.history['val_loss'], 'tab:blue', label='val_loss')
loss_ax.set_xlabel('epoch')
loss_ax.set_ylabel('loss')
loss_ax.legend(loc='upper left')
plt.savefig('./plt/training.png')


# def plot_series(time: np.ndarray, series: np.ndarray, format='-', start=0, end=None):
#     plt.plot(time[start:end], series[start:end], format)
#     plt.xlabel('Time')
#     plt.ylabel('Value')
#     plt.grid(True)


# def model_forecast(model, series, window_size):
#     ds = tf.data.Dataset.from_tensor_slices(series)
#     ds = ds.window(window_size, shift=1, drop_remainder=True)
#     ds = ds.flat_map(lambda w: w.batch(window_size))
#     ds = ds.batch(32).prefetch(1)
#     forecast = model.predict(ds)
#     return forecast


# forecast = model_forecast(model, series[..., np.newaxis], window_size)
# print(forecast.shape)

# results = forecast[split_time-window_size:-1, 0]

# plot_series(time_valid, x_valid)
# plot_series(time_valid, results)

forecast = model.predict(valid_dataset)
forecast = forecast[:, 0]

answers = valid_dataset.flat_map(lambda _, y: tf.data.Dataset.from_tensor_slices(y))
answers = np.fromiter(answers.as_numpy_iterator(), dtype=float)

f = open("./data/meanstd.txt", "r")
line = f.readline()
result = [line.strip() for line in line.split(',')]
mean = result[0]
std = result[1]

forecast *= float(std)
forecast += float(mean)
answers *= float(std)
answers += float(mean)

plt.figure()
plt.plot(time_valid[:-window_size], answers)
plt.plot(time_valid[:-window_size], forecast)
plt.xlabel("date")
plt.ylabel("temperature")
plt.legend(["answer", "forecast"])
plt.grid(True)
plt.savefig('./plt/result.png')