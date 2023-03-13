import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def read_df(file_path,file_name):
    df = pd.read_csv(file_path+'/'+file_name,encoding='ISO-8859-1')
    #print("file_path;   ",file_path)
    #print(file_name+"Dataset")
    #print(df.head())
    return df


def allFeatures(file_path,file_name):
    df = pd.read_csv(file_path+'/'+file_name,encoding='ISO-8859-1')
    features = df.columns
    return features

def df_nulls(file_path,file_name):
     df = pd.read_csv(file_path+'/'+file_name,encoding='ISO-8859-1')
     df_nulls = df.isnull().sum()
     cols = df.columns
     return df_nulls

def feature_nulls(file_path,file_name,col_name):
    df =  pd.read_csv(file_path+'/'+file_name,encoding='ISO-8859-1')
    col_nulls = df[col_name].isnull().sum()
    return col_nulls

def dataframe_dtypes(file_path,file_name):
    df =  pd.read_csv(file_path+'/'+file_name,encoding='ISO-8859-1')
    dtypes_list =  df.dtypes.tolist()
    return dtypes_list

def dataframe_shape(file_path,file_name):
    df =  pd.read_csv(file_path+'/'+file_name,encoding='ISO-8859-1')
    dfshape = df.shape
    return dfshape

def feature_distribution(file_path,file_name,col_name):
    df =  pd.read_csv(file_path+'/'+file_name,encoding='ISO-8859-1')
    #plt.figure(figsize=(12,7))
    plt.figure()
    plt.title(f'Histogram Plots for {col_name}')
    plt.xlabel(f'{col_name}')
    plt.ylabel("Density")
    plt.legend()
    sns.distplot(a=df[col_name],hist=True,kde=True)
    fig = plt.savefig('./static/images/distribution.png')
    #plt.show()

def heatmap_data(data):
    #print("*****************inside heatmap_data*********************")
    #print(data)
    plt.figure()
    X = data
    ax = plt.figure(dpi=500, facecolor='white')
    ax.tight_layout()
    sns.set(font_scale=0.5)
    plt.title('Correlation Matrix')
    sns.heatmap(abs(X.corr()), fmt=".2f", cmap="seismic",
                annot=True, linewidths=.5, )
    fig = plt.savefig('./static/images/distribution.png')
    #plt.show()

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