#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Imports
import pandas as pd
import numpy as np
from pathlib import Path
import hvplot.pandas
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from joblib import dump
from src.get_country_data_grouped import get_country_data_grouped


# In[2]:


# Manually add dummy variables to allow us to train a model on a per country basis 
# while still including all information of the other countries
grouped_transpose = get_country_data_grouped().copy()

country_codes = list(set(grouped_transpose.columns.get_level_values(0)))

df = None

for code in country_codes:
    country_data = grouped_transpose[code]
    country_data['country_code'] = code
    country_data = country_data.reset_index(drop=True)
    
    if df is None:
        df = pd.DataFrame(columns=country_data.columns)
    
    df = pd.concat([df, country_data], ignore_index=True)

series_code_total_fertility_rate = 'SP.DYN.TFRT.IN'

df = df[df[series_code_total_fertility_rate].notna()]

df.head()


# In[3]:


# Save the output to JSON for repeat use
df.to_json(Path('processed.json'))


# In[4]:


df.info()


# In[5]:


# Create a OneHotEncoder instance
enc = OneHotEncoder(sparse=False)

# Encode (convert to dummy variables) the country_code column
scaled_data = enc.fit_transform(df[['country_code']])

df_country_code = pd.DataFrame(data=scaled_data, columns=enc.get_feature_names_out(['country_code']))

dump(enc, 'onehotencoder.joblib')

df_country_code


# In[6]:


df_scaled = df.drop(columns='country_code')

scaler = StandardScaler().fit(df_scaled)

dump(scaler, 'scaler.joblib')

scaled_data = scaler.transform(df_scaled)

df_scaled = pd.DataFrame(data=scaled_data, columns=df_scaled.columns)

df_scaled


# In[21]:


df_final = pd.concat([df_scaled, df_country_code], axis=1)

df_final = df_final.fillna(0).sample(frac=1).reset_index(drop=True)


# In[8]:


y = df_final[series_code_total_fertility_rate]
X = df_final.copy().drop(columns=series_code_total_fertility_rate)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)


# In[9]:


# Define the the number of inputs (features) to the model
number_input_features = len(X_train.iloc[0])

# Review the number of features
number_input_features


# In[10]:


# Define the number of neurons in the output layer
number_output_neurons = 1


# In[11]:


# Define the number of hidden nodes for each layer
hidden_nodes_layer1 =  (number_input_features + number_output_neurons) // 2
hidden_nodes_layer2 =  (hidden_nodes_layer1 + number_output_neurons) // 2
hidden_nodes_layer3 =  (hidden_nodes_layer2 + number_output_neurons) // 2
hidden_nodes_layer4 =  (hidden_nodes_layer3 + number_output_neurons) // 2
hidden_nodes_layer5 =  (hidden_nodes_layer4 + number_output_neurons) // 2
hidden_nodes_layer6 =  (hidden_nodes_layer5 + number_output_neurons) // 2


# In[12]:


# Create the Sequential model instance
nn = Sequential()

# Add the first hidden layer
nn.add(Dense(units=hidden_nodes_layer1, input_dim=number_input_features, activation="relu"))

# Add the second hidden layer
nn.add(Dense(units=hidden_nodes_layer2, activation="relu"))

# Add the third hidden layer
nn.add(Dense(units=hidden_nodes_layer3, activation="relu"))

# Add the fourth hidden layer
nn.add(Dense(units=hidden_nodes_layer4, activation="relu"))

# Add the fifth hidden layer
nn.add(Dense(units=hidden_nodes_layer5, activation="relu"))

# Add the sixth hidden layer
nn.add(Dense(units=hidden_nodes_layer6, activation="relu"))

# Add the output layer we want to have an unlimited negative or positive number so we use the linear activation
nn.add(Dense(units=number_output_neurons, activation="linear"))

# Display the Sequential model summary
nn.summary()


# In[13]:


# Compile the Sequential model
nn.compile(loss="mean_squared_error", optimizer="adam", metrics=["mse"])


# In[14]:


fit_model = nn.fit(X_train, y_train, epochs=25)


# In[25]:


# Evaluate the model loss and mse metrics using the evaluate method and the test data
model_loss, model_accuracy = nn.evaluate(X_test, y_test, verbose=2)

# Display the model loss and accuracy results
print(f"Loss: {model_loss}, Accuracy: {1 - model_accuracy}")


# In[24]:


plt.plot(fit_model.history["loss"])
plt.title("DNN Mean Square Error per Epoch")
plt.legend(["MSE"])
plt.show()


# In[17]:


file_path = 'WorldBankFertilityModel.h5'

# Export the model to a HDF5 file
nn.save(file_path)

