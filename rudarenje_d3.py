# -*- coding: utf-8 -*-
"""Rudarenje_d3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15QwvgUYWuZ4-t89npRjP4Ph_tWsaYIgl
"""

import pandas as pd
from sklearn.model_selection import train_test_split

# Load the CSV file into a pandas dataframe
df = pd.read_csv("db.csv")

df.head()

# Split the data into features (X) and labels (y)
X = df.drop("Diabetes_binary", axis=1)
y = df["Diabetes_binary"]

# Split the data into train and test datasets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

X_train.to_csv('x_train.csv')
y_train.to_csv('y_train.csv')
X_test.to_csv('x_test.csv')
y_test.to_csv('y_test.csv')

pip install pyspark

# Import SparkSession
from pyspark.sql import SparkSession
# Create a Spark Session
spark = SparkSession.builder.master("local[*]").getOrCreate()

df = spark.read.csv("x_train.csv", header=True, inferSchema=True)

pandas_df = df.toPandas()

import matplotlib.pyplot as plt

plt.hist(pandas_df["Age"], bins=50)
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.title("Histogram of Age")
plt.show()

plt.hist(pandas_df["Sex"], bins=3)
plt.xlabel("Sex")
plt.ylabel("Frequency")
plt.title("Histogram of Age")
plt.show()

plt.plot(pandas_df["MentHlth"].value_counts().sort_index())
plt.xlabel("MentHlth")
plt.ylabel("Frequency")
plt.title("Histogram of MentHlth")
plt.show()

import matplotlib.pyplot as plt

plt.hist(pandas_df["BMI"], bins=50)
plt.xlabel("BMI")
plt.ylabel("Frequency")
plt.title("Histogram of Age")
plt.show()

plt.hist(pandas_df["Education"], bins=50)
plt.xlabel("Education")
plt.ylabel("Frequency")
plt.title("Histogram of Age")
plt.show()

from pyspark.sql.functions import udf, col
from pyspark.sql.types import IntegerType

def get_age_category(number):
  if number < 4:
    return 0
  if number >= 4 and number <= 8:
    return 1
  if number >= 8 and number <= 12:
    return 2
  if number >= 12:
    return 3

age_category_function = udf(get_age_category, IntegerType())

df = df.withColumn("age_category", age_category_function(col("Age")))

df.show(5)

df_sample = df.select("age", "HighBP", "HvyAlcoholConsump", "PhysHlth", "Sex", "GenHlth", "HeartDiseaseorAttack")

X_train_offline, X_test_offline, y_train_offline, y_test_offline = train_test_split(df_sample.toPandas(), y_train, test_size=0.2, random_state=0)

import pandas as pd 

def train_model(model):
  clf = tree.DecisionTreeClassifier() # defining decision tree classifier
  clf=clf.fit(X_train_offline, y_train_offline) # train data on new data and new target
  y_pred = pd.Series(clf.predict(X_test_offline)) #  assign removed data as input

  f1_score = metrics.f1_score(y_pred, y_test_offline)
  return f1_score

from sklearn.linear_model import LogisticRegression

train_model(LogisticRegression())

from sklearn import tree

train_model(tree.DecisionTreeClassifier())

from sklearn.ensemble import RandomForestClassifier

train_model(RandomForestClassifier())