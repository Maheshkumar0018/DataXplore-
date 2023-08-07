from visual import Shap_plot

import pandas as pd


data = pd.read_csv('./uploads/car_data.csv')

# Select and drop object columns
non_object_columns = data.select_dtypes(exclude=['object'])
object_columns = data.select_dtypes(include=['object'])
data = data.drop(object_columns, axis=1)

out_column = 'Selling_Price'
inputs = data.columns.tolist()  

Shap_plot(data,out_column,inputs)