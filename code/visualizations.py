# -*- coding: utf-8 -*-
"""Visualizations

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19v6P9eKhPlNnyN83_-Ydv-By5YKXD0Nx
"""

#Actual vs Predicted Values Plot
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
df = test_results.select('next_day_close', 'prediction').sample(False, 0.15).toPandas()
sns.set_style("white")
sns.lmplot(x='next_day_close', y='prediction', data=df)
plt.title("Actual vs Predicted Next Day Close")
plt.show()




import io
from google.cloud import storage
# Create a memory buffer named img_data to hold the figure
img_data = io.BytesIO()
# Write the figure to the buffer
plt.savefig(img_data, format='png', bbox_inches='tight')
# Rewind the pointer to the start of the data
img_data.seek(0)


# Connect to Google Cloud Storage
storage_client = storage.Client()
# Point to the bucket
bucket = storage_client.get_bucket(source_bucket_name)
# Create a blob to hold the data. Give it a file name
blob = bucket.blob("actualvspredictedplot.png")
# Upload the img_data contents to the blob
blob.upload_from_file(img_data)




#Residual Plot
df = test_results.select('next_day_close','prediction').sample(False,0.15).toPandas()
df['residuals'] = df['next_day_close'] - df['prediction']


# Set the style for Seaborn plots
sns.set_style("white")


plt.title("Residuals vs Predicted Values")


sns.regplot(x = 'prediction', y = 'residuals', data = df, scatter = True, color = 'red')


# Create a memory buffer named img_data to hold the figure
img_data = io.BytesIO()
# Write the figure to the buffer
plt.savefig(img_data, format='png', bbox_inches='tight')
# Rewind the pointer to the start of the data
img_data.seek(0)


# Connect to Google Cloud Storage
storage_client = storage.Client()
# Point to the bucket
bucket = storage_client.get_bucket(source_bucket_name)
# Create a blob to hold the data. Give it a file name
blob = bucket.blob("residualvsprediction.png")
# Upload the img_data contents to the blob
blob.upload_from_file(img_data)

#Close Price Distribution Plot


df = test_results.select('next_day_close').sample(False,0.55).toPandas()
sns.set_style("white")
sns.displot(df, kde=True, color='green')
plt.title('Close Price Distribution Plot')
plt.show()


# Create a memory buffer named img_data to hold the figure
img_data = io.BytesIO()
# Write the figure to the buffer
plt.savefig(img_data, format='png', bbox_inches='tight')
# Rewind the pointer to the start of the data
img_data.seek(0)


# Connect to Google Cloud Storage
storage_client = storage.Client()
# Point to the bucket
bucket = storage_client.get_bucket(source_bucket_name)
# Create a blob to hold the data. Give it a file name
blob = bucket.blob("closepricedistribution.png")
# Upload the img_data contents to the blob
blob.upload_from_file(img_data)

#CCI10 Distribution Plot
df = test_results.select('CCI10').sample(False,0.55).toPandas()
sns.set_style("white")
sns.displot(df, kde=True, color='green')
plt.title('CCI10 Distribution Plot')
plt.show()


# Create a memory buffer named img_data to hold the figure
img_data = io.BytesIO()
# Write the figure to the buffer
plt.savefig(img_data, format='png', bbox_inches='tight')
# Rewind the pointer to the start of the data
img_data.seek(0)


# Connect to Google Cloud Storage
storage_client = storage.Client()
# Point to the bucket
bucket = storage_client.get_bucket(source_bucket_name)
# Create a blob to hold the data. Give it a file name
blob = bucket.blob("CCI10pricedistribution.png")
# Upload the img_data contents to the blob
blob.upload_from_file(img_data)