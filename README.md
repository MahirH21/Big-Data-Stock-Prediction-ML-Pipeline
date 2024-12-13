# Big-Data-Stock-Prediction-ML-Pipeline
## Data Source
- **Stock Market Prediction Data - Nifty 100** ([Kaggle link](https://www.kaggle.com/datasets/debashis74017/stock-market-data-nifty-50-stocks-1-min-data/data))

### Goal
Develop a machine learning model to predict next day stock closing price using 66 gigabytes of historical stock data from the Nifty 100 index. The features include opening price, volume, date, and more than 55 technical indicators. This project utilizes big data and cloud technologies to create a machine learning pipeline. This project aims to help stock investors and business oriented professionals make data driven decisions

### Summary
1. Data Acquisition: Used GCP VM instance to download dataset into Google Cloud Storage bucket
2. Exploratory Data Analysis/Cleaning: Used GCP Dataproc cluster to create statistics, visualizations, remove null data, and create ticker column
3. Feature Engineering and Modeling: Used GCP Dataproc Cluster and PySpark to transform data and create ML pipeline
4. Visualizations: Used GCP Dataproc Cluster to use Matplotlib and Seaborn libraries to visualize prediction results and feature importance

### Results
- **Best Model R squared score:**  0.999994735293215
- **Best Model RMSE score**: 7.4824094473582
- **Best Model 3 Fold Cross Validation Metric Score (RMSE)**: 7.797832097041481
- **Best Model Regularization Parameter**: 0.5
- **Best Model Elastic Net Parameter**: 0
- **Significant Features**: CCI10, macd510, macd520, CCI15, MFI, ema15, ATR, ADX10, WILLR, macd1226

### Tech Stack
- **Language**: Python
- **Framework**: Spark (PySpark)
- **Libraries**: Google Cloud SDK, Matplotlib, Seaborn, Scikit-learn, Pandas
- **Tool**: Google Cloud Platform (Storage, Dataproc, Compute Engine)
