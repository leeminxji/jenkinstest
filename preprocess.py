import tensorflow as tf
import numpy as np
from typing import Tuple
import os

def get_data() -> Tuple[np.ndarray, np.ndarray]:
    data_file = "raw_data/station.csv"
    f = open(data_file)
    data = f.read()
    f.close()
    lines = data.split('\n')
    header = lines[0].split(',')
    lines = lines[1:]
    temperatures = []
    for line in lines:
        if line:
            linedata = line.split(',')
            linedata = linedata[1:13]
            for item in linedata:
                if item:
                    temperatures.append(float(item))
    series = np.asarray(temperatures)
    time = np.arange(len(temperatures), dtype="float32")
    return time, series


# Normalize
time, series = get_data()
mean = series.mean(axis=0)
series -= mean
std = series.std(axis=0)
series /= std

os.makedirs('./data', exist_ok=True)
f = open("./data/meanstd.txt", "w")
f.write("%f, %f" %(mean, std))
f.close()

# Split into training and validation sets
split_time = 792
time_train = time[:split_time]
x_train = series[:split_time]
time_valid = time[split_time:]
x_valid = series[split_time:]

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


# Data is now numpy array
window_size = 24
batch_size = 12
shuffle_buffer_size = 48
# train_dataset = windowed_dataset(x_train, window_size, batch_size, shuffle_buffer_size)
# valid_dataset = windowed_dataset(x_valid, window_size, batch_size, shuffle_buffer_size)
train_dataset = x_train
valid_dataset = x_valid


# Save as numpy array
np.save('./data/train_dataset', train_dataset)
np.save('./data/valid_dataset', valid_dataset)
np.save('./data/time_train', time_train)
np.save('./data/time_valid', time_valid)

