# -*- coding: utf-8 -*-
"""Crop Production data Analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KESrEvYLtX38LlVutubo5168bVt51_9U

Load and Explore the Dataset
"""

import pandas as pd

df = pd.read_csv('Crop Production data.csv')
df.head(10)

df.info()
df.describe()

"""Data Cleaning and Preprocessing

Handling Missing Values
"""

# Checking for missing values
missing_values = df.isnull().sum()
print(missing_values)

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from xgboost import XGBRegressor
from sklearn.ensemble import GradientBoostingRegressor

from sklearn.preprocessing import LabelEncoder

label_encoders = {}
for column in df.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

import numpy as np

# Filling missing values with the mean for numeric columns only
numeric_cols = df.select_dtypes(include=np.number).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

"""Outlier Detection and Handling"""

from scipy import stats

# Z-score method to detect outliers
z_scores = stats.zscore(df.select_dtypes(include=[float, int]))
abs_z_scores = abs(z_scores)
filtered_entries = (abs_z_scores < 3).all(axis=1)
df_clean = df[filtered_entries]

print("Original dataset shape:", df.shape)
print("Dataset shape after removing outliers:", df_clean.shape)

"""Feature Engineering

Creating New Features
"""

df_clean['Yield_per_Hectare'] = df_clean['Production'] / df_clean['Area']

"""Exploratory Data Analysis (EDA)

Correlation Matrix and Heatmap
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Identify non-numeric columns
non_numeric_cols = df_clean.select_dtypes(exclude=['number']).columns
print("Non-numeric columns:", non_numeric_cols)


df_numeric = df_clean.drop(non_numeric_cols, axis=1)

plt.figure(figsize=(12, 8))
if 'df_numeric' in locals():
    correlation_matrix = df_numeric.corr()
else:
    correlation_matrix = df_clean.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Matrix')
plt.show()



"""Crop Production Trends Over the Years

Analyze how crop production has changed over time.
"""

print(df_clean.columns)

if 'Year' in df_clean.columns:
    print(df_clean['Crop_Year'].dtype)
else:
    print("The 'Year' column does not exist in the DataFrame.")

"""Pie Chart: Crop Production Distribution by Crop Type"""

crop_production = df.groupby('Crop')['Production'].sum()
plt.figure(figsize=(10, 6))
plt.pie(crop_production, labels=crop_production.index, autopct='%1.1f%%', startangle=140, labeldistance=1.1)
plt.title('Crop Production Distribution by Crop Type')
plt.tight_layout()
plt.show()

"""Crop Production by Area"""

plt.figure(figsize=(14, 8))
sns.barplot(x=df['Crop'], y=df['Production'], palette='viridis')
plt.title('Crop Production by Area')
plt.xlabel('Crop')
plt.ylabel('Production')
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)  # Adjust layout
plt.show()

""" Production Trends Over Years"""

plt.figure(figsize=(14, 8))
sns.lineplot(x='Crop_Year', y='Production', hue='Crop', data=df, marker='o')
plt.title('Production Trends Over Year (2000)')
plt.xlabel('Year')
plt.ylabel('Production')
plt.show()

"""Histogram: Distribution of Production Values"""

plt.figure(figsize=(10, 6))
sns.histplot(df['Production'], bins=10, kde=True, color='orange')
plt.title('Distribution of Production Values')
plt.xlabel('Production')
plt.ylabel('Frequency')
plt.show()

"""Crop Production Distribution by State"""

state_production = df.groupby('State_Name')['Production'].sum()

# Plotting the pie chart
plt.figure(figsize=(10, 6))
plt.pie(state_production, labels=state_production.index, autopct='%1.1f%%', startangle=140)
plt.title('Crop Production Distribution by State')
plt.show()

"""Top 10 Crops by Production"""

import seaborn as sns

# Aggregate production by crop
crop_production = df.groupby('Crop')['Production'].sum().sort_values(ascending=False).head(10)

# Plotting the bar plot
plt.figure(figsize=(12, 6))
sns.barplot(x=crop_production.values, y=crop_production.index, palette='viridis')
plt.title('Top 10 Crops by Production')
plt.xlabel('Production')
plt.ylabel('Crop')
plt.show()

"""Production Trends Over Years for Top 3 Crops"""

# Select top 3 crops
top_crops = crop_production.index[:3]
df_top_crops = df[df['Crop'].isin(top_crops)]

# Plotting the line plot
plt.figure(figsize=(14, 8))
sns.lineplot(x='Crop_Year', y='Production', hue='Crop', data=df_top_crops, marker='o')
plt.title('Production Trends Over Years for Top 3 Crops')
plt.xlabel('Year')
plt.ylabel('Production')
plt.show()

"""Area vs. Production with Yield per Hectare as Color"""

# Calculate yield per hectare
df['Yield_per_Hectare'] = df['Production'] / df['Area']

# Scatter plot with yield per hectare as color
plt.figure(figsize=(12, 8))
scatter = plt.scatter(df['Area'], df['Production'], c=df['Yield_per_Hectare'], cmap='coolwarm', alpha=0.7)
plt.colorbar(scatter, label='Yield per Hectare')
plt.title('Area vs. Production with Yield per Hectare')
plt.xlabel('Area')
plt.ylabel('Production')
plt.show()

"""Crop Production Trends Over the Years"""

print(df_clean.columns)


plt.figure(figsize=(14, 8))
sns.lineplot(x='Crop_Year', y='Production', hue='Crop', data=df_clean)
plt.title('Crop Production Trends Over the Years')
plt.show()

""" Predictive Modeling

Preparing the Data for Modeling
"""

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np

"""# Example dataset (replace with your actual data)
# Assuming df is your DataFrame and you have 'features' and 'target' columns
# Example:
# df = pd.read_csv('your_data.csv')
# X = df[['feature1', 'feature2', 'feature3']]  # Feature columns
# y = df['target']  # Target column
"""

np.random.seed(42)
X = np.random.rand(100, 5)
y = np.random.rand(100)

# Splitting the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Training a Random Forest model
model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
rmse = mean_squared_error(y_test, y_pred, squared=False)
print('RMSE (Random Forest):', rmse)

# Training a Linear Regression model (for comparison)
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

# Predict and evaluate for Linear Regression
y_pred_lr = lr_model.predict(X_test)
rmse_lr = mean_squared_error(y_test, y_pred_lr, squared=False)
print('RMSE (Linear Regression):', rmse_lr)

# Predict and evaluate for Linear Regression
y_pred_lr = lr_model.predict(X_test)
rmse_lr = mean_squared_error(y_test, y_pred_lr, squared=False)
print('RMSE (Linear Regression):', rmse_lr)

"""Plotting the Results

 Plot Predictions vs. Actual Values
"""

plt.figure(figsize=(12, 6))

# Plot Random Forest Predictions
plt.subplot(1, 2, 1)
plt.scatter(y_test, y_pred, color='blue', alpha=0.7, label='Random Forest Predictions')
plt.plot([0, 1], [0, 1], color='red', linestyle='--', label='Perfect Fit')
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Random Forest: Actual vs Predicted')
plt.legend()

# Plot Linear Regression Predictions
plt.subplot(1, 2, 2)
plt.scatter(y_test, y_pred_lr, color='green', alpha=0.7, label='Linear Regression Predictions')
plt.plot([0, 1], [0, 1], color='red', linestyle='--', label='Perfect Fit')
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Linear Regression: Actual vs Predicted')
plt.legend()

plt.tight_layout()
plt.show()

"""Plot RMSE Comparison"""

# RMSE values
models = ['Random Forest', 'Linear Regression']
rmses = [rmse, rmse_lr]

plt.figure(figsize=(8, 6))
sns.barplot(x=models, y=rmses, palette='viridis')
plt.ylabel('Root Mean Squared Error (RMSE)')
plt.title('Comparison of RMSE for Different Models')
plt.show()

"""CONCLUSION:


Based on the RMSE values and the plots:


**(i).RMSE (Random Forest):** Displays how well the Random Forest model performed on the test set. Lower RMSE indicates better performance.

**(ii).RMSE (Linear Regression):** Displays how well the Linear Regression model performed on the test set.
In the Conclusion Section:

**(iii)Model Comparison:**

Compare the RMSE values of Random Forest and Linear Regression. A lower RMSE indicates a better fit to the data.

**(iv).Visualization:** The scatter plots will show how close the predicted values are to the actual values for each model. A scatter around the diagonal line (perfect fit) indicates a good model.
"""

# RMSE values
models = ['Random Forest', 'Linear Regression']
rmses = [rmse, rmse_lr]

plt.figure(figsize=(8, 6))
sns.barplot(x=models, y=rmses, palette='viridis')
plt.ylabel('Root Mean Squared Error (RMSE)')
plt.title('Comparison of RMSE for Different Models')
plt.show()

# RMSE values
models = ['Random Forest', 'Linear Regression']
rmses = [rmse, rmse_lr]

plt.figure(figsize=(8, 6))
sns.barplot(x=models, y=rmses, palette='viridis')
plt.ylabel('Root Mean Squared Error (RMSE)')
plt.title('Comparison of RMSE for Different Models')
plt.show()

# RMSE values
models = ['Random Forest', 'Linear Regression']
rmses = [rmse, rmse_lr]

plt.figure(figsize=(8, 6))
sns.barplot(x=models, y=rmses, palette='viridis')
plt.ylabel('Root Mean Squared Error (RMSE)')
plt.title('Comparison of RMSE for Different Models')
plt.show()

