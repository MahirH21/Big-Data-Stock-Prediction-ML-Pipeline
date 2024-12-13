# -*- coding: utf-8 -*-
"""EDA

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19v6P9eKhPlNnyN83_-Ydv-By5YKXD0Nx
"""

#Import libraries/modules
from google.cloud import storage
from io import StringIO
import pandas as pd


#EDA Function
def perform_EDA(df: pd.DataFrame, filename: str):

    print(f"{filename} Number of records:")
    print(df.count())
    print(f"{filename} Number of duplicate records: { len(df)-len(df.drop_duplicates())}" )
    print(f"{filename} Info")
    print(df.info())
    print(f"{filename} Describe")
    print(df.describe())
    print(f"{filename} Columns with null values")
    print(df.columns[df.isnull().any()].tolist())
    rows_with_null_values = df.isnull().any(axis=1).sum()
    print(f"{filename} Number of Rows with null values: {rows_with_null_values}" )
    integer_column_list = df.select_dtypes(include='int64').columns
    print(f"{filename} Integer data type columns: {integer_column_list}")
    float_column_list = df.select_dtypes(include='float64').columns
    print(f"{filename} Float data type columns: {float_column_list}")

    # Basic graphs/plots with Matplotlib
    import matplotlib.pyplot as plt
    # Plot a histogram from the volume data
    plt.hist(df['volume'], bins = [0,100,200,300,400,500,1000,1500])
    # Show the plot
    plt.show()


#Point to bucket
source_bucket_name="my-bigdata-project-mh"


#Create a client object that points to GCS
storage_client = storage.Client()


#Get a list of the 'blobs' (objects or files) in the bucket
blobs = storage_client.list_blobs(source_bucket_name, prefix="landing/")


#Make a list
filtered_blobs = [blob for blob in blobs if blob.name.endswith('.csv')]


#Go through each file and do an EDA on each file
for blob in filtered_blobs:
    print(f"File {blob.name} with size {blob.size} bytes")
    source_file_path=f"gs://{source_bucket_name}/landing/{blob.name}"
    df = pd.read_csv(StringIO(blob.download_as_text()), header=0, sep=",")
    perform_EDA(df, blob.name)