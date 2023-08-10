import math
import pandas as pd
from visual import bubble_plot


# Load data
data = pd.read_csv('./uploads/car_data.csv')

# Select and drop object columns
non_object_columns = data.select_dtypes(exclude=['object'])
object_columns = data.select_dtypes(include=['object'])
data = data.drop(object_columns, axis=1)

X = 'Kms_Driven'
Y = 'Present_Price'
Z = 'Year'

bubble_plot(data, X, Y, Z, hue = Z )
