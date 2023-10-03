'''
This notebook provides a quick example showing how to train a TF model. 

As part of our framework, we'll also load and deploy this trained 
model object as part of a containerized service that runs on Google GKE.
'''

import numpy as np
import pandas as pd
import pathlib
import random
import os

# Developed with TF 2.8.3
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

GCS_MODEL_PATH = os.environ['GCS_MODEL_PATH']

# Generate Dataset used for Demo
simulations  = 10000
player_count = int(simulations * 0.05)

data = []
for i in range(simulations):
    event_payload = {
        "playerid": f'player_{random.randint(100000,100000+player_count)}',
        "xcoord": random.random() * random.choice([-1,1]),
        "ycoord": random.random() * random.choice([-1,1]),
        "zcoord": random.random() * random.choice([-1,1]),
        "dow": random.randint(0,6),
        "hour": random.randint(0,23),
        "score": random.randint(1,100),
        "minutesPlayed": random.randint(0,60),
        "timeInStore": random.randint(0,30),
        "purchaseAmount": random.triangular(0,100,0) if random.random() >= 0.65 else 0,
    }
    data.append(event_payload)

dataset = pd.DataFrame.from_records(data)

dataset = dataset.dropna()

dataset.isna().sum()

# Remove playerid from training data
dataset.pop("playerid")

# Test and Train Dataset Split
train_dataset = dataset.sample(frac=0.8,random_state=0)
test_dataset  = dataset.drop(train_dataset.index)

# Set target as the "purchaseAmount"

train_target = train_dataset.pop('purchaseAmount')
test_target  = test_dataset.pop('purchaseAmount')

train_stats = train_dataset.describe()
train_stats = train_stats.transpose()
train_stats

# Normalize the input variables
def norm(x):
  return (x - train_stats['mean']) / train_stats['std']

normed_train_data = norm(train_dataset)
normed_test_data  = norm(test_dataset)

# Build our demo Model

def build_model():
  model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=[len(train_dataset.keys())]),
    layers.Dense(64, activation='relu'),
    layers.Dense(1)
  ])
  
  optimizer = tf.keras.optimizers.RMSprop(0.001)
  
  model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['mae', 'mse'])
  return model

model = build_model()

model.summary()

# The patience parameter is the amount of epochs to check for improvement
early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=15)

early_history = model.fit(normed_train_data, train_target, 
                    epochs=1000, validation_split=0.2, 
                    callbacks=[early_stop])

# Save Training Model to GCS
print(f'Saving ML Model to GCS: {GCS_MODEL_PATH}')
model.save(GCS_MODEL_PATH)
