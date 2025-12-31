#!/usr/bin/env python
# coding: utf-8

# # Mobile Price Classification

# The task is to classify the price of mobile phones in to 4 classes. For multinomial logistic regression, the softmax function
# is used to classify the input function which is z = wx + b into classes k.

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")


# In[2]:


df = pd.read_csv("train.csv")              # reading the training set
df2 = pd.read_csv("test.csv")              # reading the test set
x = df.to_numpy()                          # converting to numpy array
x2 = df2.to_numpy()                        # doing the same thing for both the set
np.set_printoptions(suppress=True)         # Making it suppress scientific notations


# In[3]:


mean = np.mean(x[:, :-1], axis=0)
std = np.std(x[:, :-1], axis=0)


# In[16]:


train_normal_data = (x[:, :-1] - mean) / std     # Normalised using z-score to help GD navigate easily
train_target = x[:, -1]
test_normal_data = (x2[:, 1:] - mean) / std     # Normalise both using the same mean and std of the training set
m = train_normal_data.shape[0]


# #### Important notes
# we have to calculate gradient, then gradient descent
# ###### y = w.T@x + b
# the input value for softmax, we don't use sigmoid here since it is not binary classification

# In[17]:


## This is a multinomial logistic regression function because we are classifying to sections more than two


# In[18]:


# The soft max funciton
def softmax(z):
    z = z - np.max(z, axis=1, keepdims=True)
    exp_z = np.exp(z)
    return exp_z / np.sum(exp_z, axis=1, keepdims=True)

# One Active Encoding, The rest inactive
def one_active(y, num_classes=4):
    act = np.zeros((m, num_classes))
    for i in range(m):
        act[i][y[i]] = 1
    return act

# Cross Cost Function
def cross(Y, Y_pred):
    e = 1e-9
    return -np.mean(np.sum(Y * np.log(Y_pred + e), axis=1))
cost = []
# Train Function
def train(X, y, num_classes=4, lr=0.001, epochs=5000):
    Y = one_active(y, num_classes)
    W = np.zeros((20, num_classes))
    b = np.zeros((1, num_classes))
    for epoch in range(epochs):
        z = X @ W + b
        P = softmax(z)
        loss = cross(Y, P)
        cost.append(loss)

        grad_w = (X.T @ (P - Y)) / m
        grad_b = np.mean(P - Y, axis=0, keepdims=True)
        W -= lr * grad_w
        b -= lr * grad_b

        if epoch % 200 == 0:
            print(f"Epoch {epoch}, Loss: {loss:.4f}")
    return W, b

# Prediction
def predict(X, W, b):
    z = X @ W + b
    P = softmax(z)
    return np.argmax(P, axis=1)

def predict_probability(X, W, b):
    z = X @ W + b
    P = softmax(z)
    return P


# In[19]:


target = train_target.astype(int) # Integer labels
W, b = train(train_normal_data, target)


# In[20]:


fig, ax = plt.subplots()
ax.plot(cost)
ax.set_ylabel("Cost")
ax.set_xlabel("Iteration")
fig.show()


# The model is doing perfect. As you can see the cost is decreasing smothly. It is as expected, so the prediction is going to be great.
# For the sake of computation, I minimised the epochs.

# In[21]:


test = predict(test_normal_data, W, b)
test[:10]


# In[22]:


# Unfortunately, the test set I downloaded from kaggle has no price range so I can not check the accuracy of the model. 


# In[23]:


streamlit_code = f"""
import streamlit as st
import numpy as np

st.title('Multinomial Logistic Regression Predictor')

W = np.array({W.tolist()})
b = np.array({b.tolist()})
mean = np.array({mean.tolist()})
std = np.array({std.tolist()})

def softmax(z):
    z = z - np.max(z, axis=1, keepdims=True)
    exp_z = np.exp(z)
    return exp_z / np.sum(exp_z, axis=1, keepdims=True)

def predict(X, W, b):
    P = softmax(X @ W + b)
    return np.argmax(P, axis=1)

features = []
for i in range({train_normal_data.shape[1]}):
    val = st.number_input(f'Feature {{i+1}}', value=0.0)
    features.append(val)

if st.button('Predict'):
    x_input = np.array(features).reshape(1, -1)
    x_input = (x_input - mean) / std
    pred_class = predict(x_input, W, b)
    st.write('Predicted class:', pred_class)
"""

with open("app.py", "w") as f:
    f.write(streamlit_code)

print("Streamlit app saved as app.py. Run: streamlit run app.py")


# In[ ]:


get_ipython().system('streamlit run app.py')


# In[1]:


## Streamlit is simple, but here you can't run it, I made sure that it runs from jupyter!


# In[ ]:




