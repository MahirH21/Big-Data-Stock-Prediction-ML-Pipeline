# -*- coding: utf-8 -*-
"""Feature Engineering and Modeling

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19v6P9eKhPlNnyN83_-Ydv-By5YKXD0Nx
"""

#Import functions modules, regression models, window, evaluation modules, tuning modules
from pyspark.sql.functions import *
from pyspark.sql import Window
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler, MinMaxScaler
from pyspark.ml import Pipeline
from pyspark.ml.regression import LinearRegression, GeneralizedLinearRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator, RegressionEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.ml.tuning import *
from pyspark.ml.evaluation import *




#Create source bucket name for paths
source_bucket_name = "my-bigdata-project-mh"




#Read parquet files from cleaned bucket and create dataframe
sdf = spark.read.parquet(f"gs://{source_bucket_name}/cleaned")




#Configure time policy settings to allow for date parsing with timezones
#Source code: https://stackoverflow.com/questions/74984049/inconsistent-behavior-cross-version-parse-datetime-by-new-parser
spark.conf.set("spark.sql.parquet.int96RebaseModeInWrite", "CORRECTED")
spark.conf.set("spark.sql.legacy.timeParserPolicy", "LEGACY")




# Convert the date column to an actual date data type
sdf = sdf.withColumn("date", to_date(sdf.date, "yyyy-MM-dd"))




# Create a window specification where each stock is within its own partition and then the data is ordered by Date
windowSpec = Window.partitionBy("ticker_symbol").orderBy("date")




# Use the 'lead' function to "look ahead" one day and create the next_day_close column
sdf = sdf.withColumn("next_day_close", lead("close", 1).over(windowSpec))




# Remove records with nulls
sdf = sdf.na.drop()




# Create an indexer for the ticker symbol
indexer = StringIndexer(inputCol="ticker_symbol", outputCol="tickerIndex", handleInvalid="keep")




# Create an encoder for ticker index
encoder = OneHotEncoder(inputCol="tickerIndex", outputCol="tickerVector", dropLast=True, handleInvalid="keep")




# List of numeric columns for scaling and assembling
numeric_columns_list = ["open", "high", "low", "volume", "sma5", "sma10", "sma15", "sma20", "ema5", "ema10","ema15", "ema20",
                   "upperband", "middleband", "lowerband", "HT_TRENDLINE", "KAMA10", "KAMA20", "KAMA30", "SAR", "TRIMA5",
                   "TRIMA10", "TRIMA20", "ADX5", "ADX10", "ADX20", "APO", "CCI5", "CCI10", "CCI15", "macd510", "macd520",
                   "macd1020", "macd1520", "macd1226", "MFI", "MOM10", "MOM15", "MOM20", "ROC5", "ROC10", "ROC20", "PPO",
                   "RSI14", "RSI8", "slowk", "slowd", "fastk", "fastd", "fastksr", "fastdsr", "ULTOSC",  "WILLR", "ATR",
                   "Trange", "TYPPRICE", "HT_DCPERIOD", "BETA"]




# Assemble the numeric features into their own feature vector
numeric_assembler = VectorAssembler(inputCols=numeric_columns_list, outputCol="numeric_features_vector")




# Create a scaler over the numeric_features_vector
scaler = MinMaxScaler(inputCol="numeric_features_vector", outputCol="scaled_features_vector")




# Create an assembler for scaled features vector and ticker vector
assembler = VectorAssembler(inputCols=["scaled_features_vector", "tickerVector"], outputCol="features")




# Save dataset to trusted folder
sdf.write.parquet(f"gs://{source_bucket_name}/trusted/features_data_5")




# Load trusted folder
sdf = spark.read.parquet(f"gs://{source_bucket_name}/trusted/features_data_5")




# Split the data into training and test sets
trainingData, testData = sdf.randomSplit([0.7, 0.3], seed=42)




# Create a Linear Regression Estimator
linear_reg = LinearRegression(labelCol="next_day_close")




# Create a regression evaluator (to get RMSE, R2, RME, etc.)
evaluator = RegressionEvaluator(labelCol="next_day_close")




# Create the pipeline
pipeline = Pipeline(stages=[indexer, encoder, numeric_assembler, scaler, assembler, linear_reg])




# Create a grid to hold hyperparameters
grid = ParamGridBuilder()
grid = grid.addGrid(linear_reg.regParam, [0.0, 0.5, 1.0])
grid = grid.addGrid(linear_reg.elasticNetParam, [0, 1])




# Build the parameter grid
grid = grid.build()


# How many models to be tested
print('Number of models to be tested: ', len(grid))


# Create the CrossValidator using the hyperparameter grid
cv = CrossValidator(estimator=pipeline, estimatorParamMaps=grid, evaluator=evaluator, numFolds=3)


# Train the models
all_models  = cv.fit(trainingData)




# Get the best model from all of the models trained
bestModel = all_models.bestModel




# Use the model 'bestModel' to predict the test set
test_results = bestModel.transform(testData)




# Show the predictions for stock prices
test_results.select(
    "ticker_symbol", "date", "next_day_close", "open", "high", "low", "volume", "sma5", "sma10", "sma15", "sma20",
    "ema5", "ema10","ema15", "ema20", "upperband", "middleband", "lowerband", "HT_TRENDLINE", "KAMA10", "KAMA20", "KAMA30", "SAR", "TRIMA5",
    "TRIMA10", "TRIMA20", "ADX5", "ADX10", "ADX20", "APO", "CCI5", "CCI10", "CCI15", "macd510", "macd520", "macd1020", "macd1520", "macd1226",
    "MFI", "MOM10", "MOM15", "MOM20", "ROC5", "ROC10", "ROC20", "PPO", "RSI14", "RSI8", "slowk", "slowd", "fastk", "fastd", "fastksr", "fastdsr",
    "ULTOSC",  "WILLR", "ATR", "Trange", "TYPPRICE", "HT_DCPERIOD", "BETA", "prediction").show(truncate=False)


# Save model to model folder
bestModel.write().overwrite().save(f"gs://{source_bucket_name}/models/stock_price_model5")


# Calculate RMSE and R2 on test data
rmse = evaluator.evaluate(test_results, {evaluator.metricName: "rmse"})
r2 = evaluator.evaluate(test_results, {evaluator.metricName: "r2"})
print(f"RMSE: {rmse} R-squared: {r2}")


# Show the average performance over the three folds
print(f"Average metric {all_models.avgMetrics}")


# bestModel.coeff. and int
coefficients = bestModel.stages[5].coefficients
print("bestModel coefficients", coefficients)
intercept = bestModel.stages[5].intercept
print("bestModel intercept", intercept)


# bestModel.hyperparamters
reg_param = bestModel.stages[5].getRegParam()
print("bestModel reg param", reg_param)
elastic_net_param = bestModel.stages[5].getElasticNetParam()
print("bestModel elastic net param", elastic_net_param)


for i in range(len(testData.columns)-1):
  print(testData.columns[i],coefficients[i])