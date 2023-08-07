import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from eli5.sklearn import PermutationImportance
from sklearn.ensemble import GradientBoostingRegressor
import eli5
from sklearn.impute import SimpleImputer

from sklearn.preprocessing import StandardScaler,MinMaxScaler, MaxAbsScaler, RobustScaler, QuantileTransformer, PowerTransformer,Normalizer
import shap
import math
from sklearn.feature_selection import mutual_info_regression
import matplotlib.pyplot as plt


def read_df(file_path,file_name):
    df = pd.read_csv(file_path+'/'+file_name,encoding='ISO-8859-1')
    #print("file_path;   ",file_path)
    #print(file_name+"Dataset")
    #print(df.head())
    return df

## --- only numerical columns
def get_numerical_columns(file_path, file_name):
    dataframe = pd.read_csv(file_path+'/'+file_name, encoding='ISO-8859-1')
    numerical_cols = dataframe.select_dtypes(include=[np.number]).columns
    return numerical_cols

def allFeatures(file_path,file_name):
    df = pd.read_csv(file_path+'/'+file_name,encoding='ISO-8859-1')
    features = df.columns
    return features

def df_nulls(file_path,file_name):
     df = pd.read_csv(file_path+'/'+file_name,encoding='ISO-8859-1')
     df_nulls = df.isnull().sum()
     cols = df.columns
     return df_nulls

def feature_outliers(file_path,file_name,col_name):
    df =  pd.read_csv(file_path+'/'+file_name,encoding='ISO-8859-1')
    col_nulls = df[col_name].isnull().sum()
    return col_nulls

# describe
def get_dataframe_stats(file_path, file_name):
    df = pd.read_csv(file_path + '/' + file_name, encoding='ISO-8859-1')
    stats = df.describe().to_html()
    return stats

def dataframe_dtypes(file_path,file_name):
    df =  pd.read_csv(file_path+'/'+file_name,encoding='ISO-8859-1')
    dtypes_list =  df.dtypes.tolist()
    return dtypes_list

def dataframe_shape(file_path,file_name):
    df =  pd.read_csv(file_path+'/'+file_name,encoding='ISO-8859-1')
    dfshape = df.shape
    return dfshape

def feature_distribution(file_path, file_name, col_name):
    df = pd.read_csv(file_path+'/'+file_name, encoding='ISO-8859-1')
    
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    if col_name not in numerical_cols:
        print(f"{col_name} is not a numerical column.")
        return
    
    plt.figure()
    plt.title(f'Histogram Plots for {col_name}')
    plt.xlabel(f'{col_name}')
    plt.ylabel("Density")
    plt.legend()
    sns.distplot(a=df[col_name], hist=True, kde=True)
    fig = plt.savefig('./static/images/distribution.png')

    #plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

def heatmap_data(data, column1, column2):
    if column1 not in data.columns or column2 not in data.columns:
        raise ValueError("The specified columns do not exist in the DataFrame.")
    X = data[[column1, column2]]
    plt.figure()
    ax = plt.figure(dpi=500, facecolor='white')
    ax.tight_layout()
    sns.set(font_scale=0.5)
    plt.title('Correlation Matrix')
    sns.heatmap(abs(X.corr()), fmt=".2f", cmap="seismic", annot=True, linewidths=.5)
    fig = plt.savefig('./static/images/distribution.png')

def boxplot_data(data):
    plt.figure()
    X = data
    columns = X.select_dtypes(include=np.number).columns
    figure = plt.figure(figsize=(20, 10))
    figure.add_subplot(1, len(columns), 1)
    sns.set(font_scale=1.6)
    for index, col in enumerate(columns):
        if index > 0:
            figure.add_subplot(1, len(columns), index + 1)
        sns.boxplot(y=col, data=data, palette='Reds', showmeans=True)
        plt.ylabel(X.columns[index], fontsize='20')
    figure.tight_layout()
    # return fig_to_base64(figure)
    fig = plt.savefig('./static/images/distribution.png')
    #plt.show()

def pairplot_data(data):
    X = data
    plt.figure(facecolor='white')
    plt.figure(dpi=300, facecolor='white')
    sns.set(font_scale=1.1)
    ax = sns.pairplot(X, diag_kind='hist', kind='scatter', hue=None)
    # ax.fig.set_size_inches(20,15)
    fig = plt.savefig('./static/images/distribution.png')
    #plt.show()

def histogram_data(data, columns, hue='Select'):
    sns.set(font_scale=0.8)
    #print("****************inside histogram_data1")
    plt.figure(dpi=600, facecolor='white')
    if hue != 'Select':
        sns.histplot(data, x=columns, hue=hue, palette="tab10")
        #print("****************inside histogram_data2")
    else:
        sns.histplot(data, x=columns)
        #print("****************inside histogram_data3")
    fig = plt.savefig('./static/images/distribution.png')
    #return fig_to_base64(plt)
    #plt.show()


def Perm_plot(df, out_column, inputs):
    y = df[out_column]
    X = df[inputs]

    # Handle missing values in the target variable y
    y = y.dropna()

    # Handle missing values in the feature variables using SimpleImputer
    imputer = SimpleImputer(strategy='mean')
    X_imputed = imputer.fit_transform(X)

    train_X, val_X, train_y, val_y = train_test_split(X_imputed, y, random_state=42)
    my_model = GradientBoostingRegressor(
        learning_rate=0.01, n_estimators=1000, min_samples_split=3, max_depth=3).fit(train_X, train_y)
    perm = PermutationImportance(my_model, random_state=42).fit(val_X, val_y)

    table = eli5.formatters.as_dataframe.explain_weights_df(
        perm, feature_names=inputs)
    
    plt.figure(figsize=(25, 15), dpi=200)
    sns.set(font_scale=1.3)
    x = table['weight']
    y = table['feature']
    plt.barh(y, x)
    plt.ylabel("Feature")
    plt.xlabel("Weights")
    plt.title("Feature importance")
    fig = plt.savefig('./static/images/distribution.png')


def Scaleplot(data, inputs):
    X = data[inputs]
    scalers = [
        StandardScaler(), MinMaxScaler(), MaxAbsScaler(), RobustScaler(),
        QuantileTransformer(output_distribution='uniform'),
        QuantileTransformer(output_distribution='normal'),
    ]

    sns.set(font_scale=1.6)
    plt.figure(figsize=(20, 20), dpi=100, facecolor='white')
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.1, hspace=0.9)

    for i, scale in enumerate(scalers):
        scaler = scale.fit(X)
        data_scaled = pd.DataFrame(scaler.transform(X), columns=list(X.columns))

        plt.subplot(4, 2, i + 1)
        plt.title(str(scale), fontsize='20')
        sns.boxplot(data=data_scaled, showmeans=True)
        plt.xticks(fontsize=14, rotation=90)

    fig = plt.savefig('./static/images/distribution.png')


def Shap_plot(data,out_column,inputs):
    y = data[out_column]  # Convert from string "Yes"/"No" to binary
    #feature_names = [i for i in data.columns if data[i].dtype in [np.int64, np.int64]]
    X = data[inputs]
    train_X, val_X, train_y, val_y = train_test_split(X, y,test_size=0.25, random_state=42)
    my_model = GradientBoostingRegressor(learning_rate = 0.01,n_estimators = 1000, 
                                         min_samples_split= 3, max_depth = 3 ).fit(train_X, train_y)
    shap_values = shap.TreeExplainer(my_model).shap_values(train_X)
    plt.figure(figsize=(50, 20),dpi=200, facecolor='white',frameon=True,linewidth=10)
    shap.summary_plot(shap_values, train_X,show=False)
    plt.ylabel(f"Feature- {out_column}")
    # return fig_to_base64(plt)
    fig = plt.savefig('./static/images/distribution.png')

###################### not implemented ####################

def mutual_index(data, inputs, outputs):

    n = 0
    X = data[inputs]
    n_inputs = len(inputs)
    output_coulumns = len(outputs)
    xes = math.trunc(output_coulumns % 2)
    if xes == 0:
        xes = math.trunc(output_coulumns/2)
    else:
        xes = math.trunc(output_coulumns/2 + 0.5)

    if output_coulumns == 1:
        fig = plt.figure(figsize=(10, 10))
        y = data[outputs[0]]
        mi_scores = mutual_info_regression(X, y)
        mi_scores = pd.Series(mi_scores, name="MI Scores", index=X.columns)
        scores = mi_scores.sort_values(ascending=True)
        height = scores.values
        bars = (scores.keys())
        y_pos = list(range(len(bars)))
        x_pos = list(range(len(height)))
        plt.barh(y_pos, height)
        plt.yticks(y_pos, bars)
        plt.title(outputs[0])

    elif output_coulumns == 2:
        fig = plt.figure(figsize=(20, 10))
        for i, j in enumerate(outputs):
            plt.subplot(1, 2, i+1)
            plt.subplots_adjust(wspace=0.5, hspace=5)
            y = data[j]
            mi_scores = mutual_info_regression(X, y)
            mi_scores = pd.Series(mi_scores, name="MI Scores", index=X.columns)
            scores = mi_scores.sort_values(ascending=True)
            height = scores.values
            bars = (scores.keys())
            y_pos = list(range(len(bars)))
            x_pos = list(range(len(height)))
            plt.barh(y_pos, height)
            plt.yticks(y_pos, bars)
            plt.title(j)
            n = n + 1

    else:
        fig, axes = plt.subplots(xes, 2, sharex=False,
                                 sharey=True, figsize=(15, 10))
        plt.rcParams["axes.grid"] = False
        plt.xticks(fontsize=9,)
        #fig.add_subplot(111, frameon=False)
        # hide tick and tick label of the big axis
        plt.subplots_adjust(wspace=0.1, hspace=0.5)
       # sns.set(font_scale=2)
        for i, row in enumerate(axes):
            for j, cell in enumerate(row):
                y = data[outputs[n]]
                mi_scores = mutual_info_regression(X, y)
                mi_scores = pd.Series(
                    mi_scores, name="MI Scores", index=X.columns)
                scores = mi_scores.sort_values(ascending=True)
                height = scores.values
                bars = (scores.keys())
                y_pos = list(range(len(bars)))
                x_pos = list(range(len(height)))
                sns.set(font_scale=1)
                cell.barh(y_pos, height)
                plt.yticks(y_pos, bars)
                #plt.xticks(x_pos, height)
                plt.xticks(fontsize=9,)
                cell.set_title(outputs[n])
                n = n + 1
                if n > output_coulumns-1:
                    break
    # return fig_to_base64(plt)
    fig = plt.savefig('./static/images/distribution.png')

def bubble_plot(data, X, Y, Z = 'Select', hue = 'Select' ):
    sns.set(font_scale=0.5)
    plt.figure(dpi=300,facecolor='white') # use the scatterplot function to build the bubble map
    if hue != 'Select' and Z != 'Select':
        sns.scatterplot(data=data, x=X, y=Y, size=Z, legend='auto', sizes=(50, 150),hue=hue,palette = 'tab10',alpha=0.5)
    elif hue == 'Select' and Z != 'Select':
        sns.scatterplot(data=data, x=X, y=Y, size=Z, legend='auto', sizes=(50, 150),hue=None,palette = 'tab10',alpha=0.5)
    elif hue != 'Select' and Z == 'Select':
        sns.scatterplot(data=data, x=X, y=Y, size=None, legend='auto', sizes=(50, 150),hue=hue,palette = 'tab10',alpha=0.5)
    else:
        sns.scatterplot(data=data, x=X, y=Y, size=None, legend='auto', sizes=(50, 500),hue=None,palette = 'tab10',alpha=0.5)
    plt.legend(markerscale = 0.5)
    # return fig_to_base64(plt)
    fig = plt.savefig('./static/images/distribution.png')
