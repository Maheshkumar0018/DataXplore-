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
            flash(filename+'  is not an '+'CSV or XLXS')
    
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

        if (feature_1 != 'Select' and feature_2 != 'Select'):
            df = pd.read_csv(file_path+'/'+filename,encoding='ISO-8859-1')
            heat = heatmap_data(df,feature_1,feature_2)
        else:
            blank_image = Image.new('RGB', (800, 600), (255, 255, 255))
            # Add the text to the image
            draw = ImageDraw.Draw(blank_image)
            text = " Please select Features to create HeatMap."
            font = ImageFont.truetype("arial.ttf", 24)   # Replace "arial.ttf" with the path to your font file.
            text_width, text_height = draw.textsize(text, font=font)
            text_position = ((blank_image.width - text_width) // 2, (blank_image.height - text_height) // 2)
            fill_color = (255, 0, 0)  # Red color
            draw.text(text_position, text, font=font, fill=fill_color)
            blank_image.save('./static/images/distribution.png')

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

        if (pairfeat1 != 'Select' and pairfeat2 != 'Select' and pairfeat3 != 'Select'):
            df = pd.read_csv(file_path+'/'+filename,encoding='ISO-8859-1')
            data = df[[pairfeat1,pairfeat2,pairfeat3]]
            pair = pairplot_data(data)
        else:
            blank_image = Image.new('RGB', (800, 600), (255, 255, 255))
            # Add the text to the image
            draw = ImageDraw.Draw(blank_image)
            text = " Please select Features to create Pairplot."
            font = ImageFont.truetype("arial.ttf", 24)   # Replace "arial.ttf" with the path to your font file.
            text_width, text_height = draw.textsize(text, font=font)
            text_position = ((blank_image.width - text_width) // 2, (blank_image.height - text_height) // 2)
            fill_color = (255, 0, 0)  # Red color
            draw.text(text_position, text, font=font, fill=fill_color)
            blank_image.save('./static/images/distribution.png')


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

        if (feat1 != 'Select' and feat2 != 'Select' and feat3 != 'Select'):
            df = pd.read_csv(file_path+'/'+filename,encoding='ISO-8859-1')
            data = df[[feat1,feat2,feat3]]
            box = boxplot_data(data)
        else:
            blank_image = Image.new('RGB', (800, 600), (255, 255, 255))
            # Add the text to the image
            draw = ImageDraw.Draw(blank_image)
            text = " Please select Features to create BoxPlot."
            font = ImageFont.truetype("arial.ttf", 24)   # Replace "arial.ttf" with the path to your font file.
            text_width, text_height = draw.textsize(text, font=font)
            text_position = ((blank_image.width - text_width) // 2, (blank_image.height - text_height) // 2)
            fill_color = (255, 0, 0)  # Red color
            draw.text(text_position, text, font=font, fill=fill_color)
            blank_image.save('./static/images/distribution.png')

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

        if histcol != 'Select':
            data = pd.read_csv(file_path+'/'+filename,encoding='ISO-8859-1')
            his = histogram_data(data, histcol, hue='Select')
        else:
            blank_image = Image.new('RGB', (800, 600), (255, 255, 255))
            # Add the text to the image
            draw = ImageDraw.Draw(blank_image)
            text = " Please select Features to create Histogram's."
            font = ImageFont.truetype("arial.ttf", 24)   # Replace "arial.ttf" with the path to your font file.
            text_width, text_height = draw.textsize(text, font=font)
            text_position = ((blank_image.width - text_width) // 2, (blank_image.height - text_height) // 2)
            fill_color = (255, 0, 0)  # Red color
            draw.text(text_position, text, font=font, fill=fill_color)
            blank_image.save('./static/images/distribution.png')

        return render_template('Histogram.html',columns=columns,img_path=img_path,filename=filename,
                               numerical_columns=numerical_columns)
    return render_template('Histogram.html',columns=columns,filename=filename,
                           numerical_columns=numerical_columns)



@app.route('/permplot',methods = ['GET','POST'])
def permplot():
    img_path = '../static/images/distribution.png'
    numerical_columns = get_numerical_columns(file_path,filename)
    if request.method == 'POST':
        output_cols = request.form.get('perm_fet_1')
        if output_cols != 'Select':
            df = pd.read_csv(file_path+'/'+filename,encoding='ISO-8859-1')
            # Identify non-numeric columns
            non_numeric_columns = df.select_dtypes(include=['object']).columns.tolist()
            # Drop non-numeric columns
            df = df.drop(non_numeric_columns, axis=1) 
            # Handle missing values in df
            df.dropna(subset=[output_cols], inplace=True)
            out_column = output_cols
            inputs = df.columns.tolist()
            inputs.remove(out_column)

            perm = Perm_plot(df, out_column, inputs)
        else:
            blank_image = Image.new('RGB', (800, 600), (255, 255, 255))
            # Add the text to the image
            draw = ImageDraw.Draw(blank_image)
            text = " Please select Features to create PermPlot."
            font = ImageFont.truetype("arial.ttf", 24)   # Replace "arial.ttf" with the path to your font file.
            text_width, text_height = draw.textsize(text, font=font)
            text_position = ((blank_image.width - text_width) // 2, (blank_image.height - text_height) // 2)
            fill_color = (255, 0, 0)  # Red color
            draw.text(text_position, text, font=font, fill=fill_color)
            blank_image.save('./static/images/distribution.png')

        return render_template('permplot.html',img_path=img_path,numerical_columns=numerical_columns,
                           filename=filename)
    
    return render_template('permplot.html',numerical_columns=numerical_columns,filename=filename)



@app.route('/scaleplot',methods = ['GET','POST'])
def scaleplot():
    img_path = '../static/images/distribution.png'
    if request.method == 'POST':
        inputs =request.form.get('sale_feat')
        if inputs == 'Yes':
            df = pd.read_csv(file_path+'/'+filename,encoding='ISO-8859-1')
            # Select and drop object columns
            non_object_columns = df.select_dtypes(exclude=['object'])
            object_columns = df.select_dtypes(include=['object'])
            df = df.drop(object_columns, axis=1)
            # Get the list of input columns after dropping object columns
            inputs = non_object_columns.columns.tolist()
            Scaleplot(df, inputs)
        else:
            blank_image = Image.new('RGB', (800, 600), (255, 255, 255))
            # Add the text to the image
            draw = ImageDraw.Draw(blank_image)
            text = " Please select Yes to create ScalePlot."
            font = ImageFont.truetype("arial.ttf", 24)  # Replace "arial.ttf" with the path to your font file.
            text_width, text_height = draw.textsize(text, font=font)
            text_position = ((blank_image.width - text_width) // 2, (blank_image.height - text_height) // 2)
            fill_color = (255, 0, 0)  # Red color
            draw.text(text_position, text, font=font, fill=fill_color)
            blank_image.save('./static/images/distribution.png')

        return render_template('scaleplot.html',img_path=img_path,filename=filename)
    
    return render_template('scaleplot.html',filename=filename)



@app.route('/shapplot',methods = ['GET','POST'])
def shapplot():
    numerical_columns = get_numerical_columns(file_path,filename)
    img_path = '../static/images/distribution.png'
    if request.method == 'POST':
        out_column =request.form.get('shap_feat')
        if out_column != 'Select':
            df = pd.read_csv(file_path+'/'+filename,encoding='ISO-8859-1')
            # Select and drop object columns
            non_object_columns = df.select_dtypes(exclude=['object'])
            object_columns = df.select_dtypes(include=['object'])
            df = df.drop(object_columns, axis=1)
            inputs = df.columns.tolist() 
            Shap_plot(df,out_column,inputs)
        else:
            blank_image = Image.new('RGB', (800, 600), (255, 255, 255))
            # Add the text to the image
            draw = ImageDraw.Draw(blank_image)
            text = " Please select Yes to create ShapPlot."
            font = ImageFont.truetype("arial.ttf", 24)  # Replace "arial.ttf" with the path to your font file.
            text_width, text_height = draw.textsize(text, font=font)
            text_position = ((blank_image.width - text_width) // 2, (blank_image.height - text_height) // 2)
            fill_color = (255, 0, 0)  # Red color
            draw.text(text_position, text, font=font, fill=fill_color)
            blank_image.save('./static/images/distribution.png')

        return render_template('shapplot.html',img_path=img_path,filename=filename,
                               numerical_columns=numerical_columns)
    
    return render_template('shapplot.html',filename=filename,numerical_columns=numerical_columns)



@app.route('/mutual_index',methods = ['GET','POST'])
def mutual_index():
    numerical_columns = get_numerical_columns(file_path,filename)
    img_path = '../static/images/distribution.png'
    if request.method == 'POST':
        out_column =request.form.get('mutal_indx')
        if out_column != 'Select':
            df = pd.read_csv(file_path + '/' + filename, encoding='ISO-8859-1')
            non_object_columns = df.select_dtypes(exclude=['object'])
            object_columns = df.select_dtypes(include=['object'])
            df = df.drop(object_columns, axis=1)
            inputs = df.columns.tolist()
            mutual_index_plot(df, inputs, [out_column])
        else:
            blank_image = Image.new('RGB', (800, 600), (255, 255, 255))
            # Add the text to the image
            draw = ImageDraw.Draw(blank_image)
            text = " Please select Yes to create Mutual Index Plot."
            font = ImageFont.truetype("arial.ttf", 24)  # Replace "arial.ttf" with the path to your font file.
            text_width, text_height = draw.textsize(text, font=font)
            text_position = ((blank_image.width - text_width) // 2, (blank_image.height - text_height) // 2)
            fill_color = (255, 0, 0)  # Red color
            draw.text(text_position, text, font=font, fill=fill_color)
            blank_image.save('./static/images/distribution.png')

        return render_template('mutual_index.html',img_path=img_path,filename=filename,
                               numerical_columns=numerical_columns)
    
    return render_template('mutual_index.html',filename=filename,numerical_columns=numerical_columns)



@app.route('/bubbleplot',methods = ['GET','POST'])
def bubbleplot():
    numerical_columns = get_numerical_columns(file_path,filename)
    img_path = '../static/images/distribution.png'
    if request.method == 'POST':
        X = request.form.get('bubble_1')
        Y = request.form.get('bubble_2')
        Z = request.form.get('bubble_3')

        if (X != 'Select' and Y != 'Select' and Z != 'Select'):
            df = pd.read_csv(file_path + '/' + filename, encoding='ISO-8859-1')
            non_object_columns = df.select_dtypes(exclude=['object'])
            object_columns = df.select_dtypes(include=['object'])
            df = df.drop(object_columns, axis=1)
            bubble_plot(df, X, Y, Z, hue = Z )
           
        else:
            blank_image = Image.new('RGB', (800, 600), (255, 255, 255))
            # Add the text to the image
            draw = ImageDraw.Draw(blank_image)
            text = " Please select Yes to create Mutual Index Plot."
            font = ImageFont.truetype("arial.ttf", 24)  # Replace "arial.ttf" with the path to your font file.
            text_width, text_height = draw.textsize(text, font=font)
            text_position = ((blank_image.width - text_width) // 2, (blank_image.height - text_height) // 2)
            fill_color = (255, 0, 0)  # Red color
            draw.text(text_position, text, font=font, fill=fill_color)
            blank_image.save('./static/images/distribution.png')

        return render_template('bubble_plot.html',img_path=img_path,filename=filename,
                               numerical_columns=numerical_columns)
    
    return render_template('bubble_plot.html',filename=filename,numerical_columns=numerical_columns)


if __name__ == '__main__':
	app.run(debug=True)