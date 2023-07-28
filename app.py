from flask import Flask,render_template,redirect,request,flash,url_for
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os
from PIL import Image, ImageDraw, ImageFont
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

        # describe
        if col_null not in ['None','Select','NO']:
            stats_table = get_dataframe_stats(file_path, filename)
        else:
            stats_table = 'Please Select the Column'

        if dtype not in ['None','Select','NO']:
            df_dtypes = dataframe_dtypes(file_path,filename)
        else:
            df_dtypes="Please Select the Column"

        if dfshape not in ['None','Select','NO']:
            df_shape = dataframe_shape(file_path,filename)
        else:
            df_shape="Please Select the Column"

        if dist_col not in ['None', 'Select', 'NO']:
            dist = feature_distribution(file_path,filename,dist_col)       
        else:
            #print('it enters into no numeric fun')
            blank_image = Image.new('RGB', (800, 600), (255, 255, 255))
            # Add the text to the image
            draw = ImageDraw.Draw(blank_image)
            text = " No Numerical columns, unable to create the Distribution plot."
            font = ImageFont.truetype("arial.ttf", 24)  # Replace "arial.ttf" with the path to your font file.
            text_width, text_height = draw.textsize(text, font=font)
            text_position = ((blank_image.width - text_width) // 2, (blank_image.height - text_height) // 2)
            fill_color = (255, 0, 0)  # Red color
            draw.text(text_position, text, font=font, fill=fill_color)
            blank_image.save('./static/images/distribution.png')


        return render_template('features_analysis.html',columns=columns,feature_columns=feature_columns,dnulls=dnulls,
                               stats_table=stats_table,df_dtypes=df_dtypes,df_shape=df_shape,img_path=img_path,
                               filename=filename)

     return render_template('features_analysis.html',columns=columns,filename=filename,
                            numerical_columns=numerical_columns)


@app.route('/visuallandingpage')
def visuallandingpage():
    global filename
    img_path = '../static/images/distribution.png'
    #print("*******selected_file:", filename)
    data = read_df(file_path,filename)

    return render_template('visual_index.html',filename=filename)

@app.route('/heatmap',methods=['GET', 'POST'])
def heatmap():
    global filename
    img_path = '../static/images/distribution.png'
    data = read_df(file_path,filename)
    numerical_columns = get_numerical_columns(file_path,filename)
    if request.method == 'POST':
        feature_1 = request.form.get('heatmap_fe_1')
        feature_2 = request.form.get('heatmap_fe_2')
        #print('column_heatmap_1',feature_1)
        #print('column_heatmap_2',feature_2)
        df = pd.read_csv(file_path+'/'+filename,encoding='ISO-8859-1')
        heat = heatmap_data(df,feature_1,feature_2)

        return render_template('heatmap.html',img_path=img_path,filename=filename,
                           numerical_columns=numerical_columns)

    return render_template('heatmap.html',filename=filename,
                           numerical_columns=numerical_columns)

@app.route('/pairplot',methods=['GET', 'POST'])
def pairplot():
    global filename
    img_path = '../static/images/distribution.png'
    columns = allFeatures(file_path,filename)
    columns = columns.to_list()
    numerical_columns = get_numerical_columns(file_path,filename)
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

        return render_template('pairplot.html',columns=columns,img_path=img_path,filename=filename,
                               numerical_columns=numerical_columns)
    return render_template('pairplot.html',columns=columns,filename=filename,
                           numerical_columns=numerical_columns)

@app.route('/boxplot',methods=['GET', 'POST'])
def boxplot():
    img_path = '../static/images/distribution.png'
    columns = allFeatures(file_path,filename)
    columns = columns.to_list()
    numerical_columns = get_numerical_columns(file_path,filename)
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

        return render_template('boxplot.html',columns=columns,img_path=img_path,filename=filename,
                               numerical_columns=numerical_columns)
    return render_template('boxplot.html',columns=columns,filename=filename,
                           numerical_columns=numerical_columns)

@app.route('/histogram',methods=['GET', 'POST'])
def histogram():
    img_path = '../static/images/distribution.png'
    columns = allFeatures(file_path,filename)
    columns = columns.to_list()
    numerical_columns = get_numerical_columns(file_path,filename)
    if request.method == 'POST':
        histcol =  request.form.get('histfeature')
        #print("*******Histogram*********",hist)
        data = pd.read_csv(file_path+'/'+filename,encoding='ISO-8859-1')
        his = histogram_data(data, histcol, hue='Select')

        return render_template('Histogram.html',columns=columns,img_path=img_path,filename=filename,
                               numerical_columns=numerical_columns)
    return render_template('Histogram.html',columns=columns,filename=filename,
                           numerical_columns=numerical_columns)

if __name__ == '__main__':
	app.run(debug=True)