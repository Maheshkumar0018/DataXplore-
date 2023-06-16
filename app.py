from flask import Flask,render_template,redirect,request,flash,url_for
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os
from visual import *

file_path = r'C:\Users\mkmt724\Documents\App\uploads'

app = Flask(__name__)
app.config['SECRET_KEY'] = "Exploratory_Data_Analysis"
app.config['ALLOWED_EXTENSIONS'] = ['csv','xlsx']


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload',methods=['GET', 'POST'])
def upload():
    global filename
    if request.method == 'POST':
        upload_file = request.files['file']
        filename = secure_filename(upload_file.filename) 
        print("*****file_name:", filename)
        # submit without any file
        
        if upload_file.filename == '':
            flash('Please Select the File')
            return redirect(url_for('upload'))
        extension = filename.split('.')[1]
        if extension in app.config['ALLOWED_EXTENSIONS']:
        
            upload_file.save(os.path.join(
            'uploads/',
            secure_filename(upload_file.filename)))
            print("file_name:",filename)
            flash("file Uploaded")
            #fun = read_df(file_path,filename)
            #print(fun)
        else:
            print("Please Select Correct File")
            flash("Please Select Correct File")
    
    return redirect('/')


@app.route('/features',methods=['GET', 'POST'])
def features():
     global filename
     print('******File_name******:',filename)
     columns = allFeatures(file_path,filename)
     numerical_columns = get_numerical_columns(file_path,filename)
     img_path = '../static/images/distribution.png'
     if request.method == 'POST':
        features = request.form.get('allfeatues')
        nulls = request.form.get('df_nulls')
        col_null = request.form.get('column_null')
        dtype = request.form.get('data_types')
        dfshape = request.form.get('dfshape')
        dist_col = request.form.get('distribution')
        #column_name = request.form.get('dropfeature')
        #print("***dropfeature***",column_name)
        
        if features not in ['None','Select','NO']:
            feature_columns =  allFeatures(file_path,filename)
            feature_columns = feature_columns.tolist()
            #print("All Columns:",feature_columns)
        else:
            feature_columns="Please Select the Column"

        if nulls not in ['None','Select','NO']:
            dnulls = df_nulls(file_path,filename)
            #print("All Nulls:",dnulls)
        else:
            dnulls="Please Select the Column"

        if col_null not in ['None','Select','NO']:
            col_nulls = feature_outliers(file_path,filename,col_null)
            #print("Feature_outliers:",col_nulls)
        else:
            col_nulls="Please Select the Column"

        if dtype not in ['None','Select','NO']:
            df_dtypes = dataframe_dtypes(file_path,filename)
            #print("df_dtypes:",df_dtypes)
        else:
            df_dtypes="Please Select the Column"

        if dfshape not in ['None','Select','NO']:
            df_shape = dataframe_shape(file_path,filename)
            #print("dfshape:",df_shape)
        else:
            df_shape="Please Select the Column"

        if dist_col not in ['None','Select','NO']:
            dist = feature_distribution(file_path,filename,dist_col)
        else:
            dist="Please Select the Column"


        return render_template('features_analysis.html',columns=columns,feature_columns=feature_columns,dnulls=dnulls,
                               col_nulls=col_nulls,df_dtypes=df_dtypes,df_shape=df_shape,dist=dist,img_path=img_path,
                               col_null=col_null,filename=filename)

     return render_template('features_analysis.html',columns=columns,filename=filename,
                            numerical_columns=numerical_columns)


@app.route('/visuallandingpage')
def visuallandingpage():
    global filename
    img_path = '../static/images/distribution.png'
    #print("*******selected_file:", filename)
    data = read_df(file_path,filename)

    return render_template('visual_index.html',filename=filename)

@app.route('/heatmap')
def heatmap():
    global filename
    img_path = '../static/images/distribution.png'
    #print("*******selected_file:", filename)
    data = read_df(file_path,filename)
    #print("***head:",data)
    heat = heatmap_data(data)

    return render_template('heatmap.html',img_path=img_path,filename=filename)

@app.route('/pairplot',methods=['GET', 'POST'])
def pairplot():
    global filename
    img_path = '../static/images/distribution.png'
    columns = allFeatures(file_path,filename)
    columns = columns.to_list()
    if request.method == 'POST':
        pairfeat1 = request.form.get('pairfeature1')
        pairfeat2 = request.form.get('pairfeature2')
        pairfeat3 = request.form.get('pairfeature3')
        #print("****Feature1*****",pairfeat1)
        #print("****Feature2*****",pairfeat2)
        #print("****Feature3*****",pairfeat3)
        df = pd.read_csv(file_path+'/'+filename,encoding='ISO-8859-1')
        data = df[[pairfeat1,pairfeat2,pairfeat3]]
        pair = pairplot_data(data)

        return render_template('pairplot.html',columns=columns,img_path=img_path,filename=filename)
    return render_template('pairplot.html',columns=columns,filename=filename)

@app.route('/boxplot',methods=['GET', 'POST'])
def boxplot():
    img_path = '../static/images/distribution.png'
    columns = allFeatures(file_path,filename)
    columns = columns.to_list()
    if request.method == 'POST':
        feat1 =  request.form.get('feature1')
        feat2 =  request.form.get('feature2')
        feat3 =  request.form.get('feature3')
        #print("*****feature1*******",feat1)
        #print("*****feature2*******",feat2)
        #print("*****feature3*******",feat3)
        df = pd.read_csv(file_path+'/'+filename,encoding='ISO-8859-1')
        data = df[[feat1,feat2,feat3]]
        box = boxplot_data(data)

        return render_template('boxplot.html',columns=columns,img_path=img_path,filename=filename)
    return render_template('boxplot.html',columns=columns,filename=filename)

@app.route('/histogram',methods=['GET', 'POST'])
def histogram():
    img_path = '../static/images/distribution.png'
    columns = allFeatures(file_path,filename)
    columns = columns.to_list()
    if request.method == 'POST':
        histcol =  request.form.get('histfeature')
        #print("*******Histogram*********",hist)
        data = pd.read_csv(file_path+'/'+filename,encoding='ISO-8859-1')
        his = histogram_data(data, histcol, hue='Select')

        return render_template('Histogram.html',columns=columns,img_path=img_path,filename=filename)
    return render_template('Histogram.html',columns=columns,filename=filename)

if __name__ == '__main__':
	app.run(debug=True)