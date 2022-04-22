
from colorama import Cursor
from flask import Flask, flash,request,render_template,url_for,redirect,session
import os
from flask_dropzone import Dropzone
from werkzeug.utils import secure_filename
import secrets
import similarité_cosinus_deux_doc
import Nltk_similarity
import similarity_strsimpy
import sqlite3


secret = secrets.token_urlsafe(32)


basedir=os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)
app.config.update(
    UPLOADED_PATH= os.path.join(basedir,'uploads_'),
    DROPZONE_MAX_FILE_SIZE = 1024,
    DROPZONE_TIMEOUT = 5*60*1000)
app.secret_key = secret

dropzone = Dropzone(app)

@app.route("/")
def rooter():
    return render_template("login.html")


@app.route('/login-form',methods=['POST'])
def checklogin():
    
    UN=request.form['username']
    PW= request.form['password']
    
    sqlconnection=sqlite3.Connection(basedir+'\Login.db')
    Cursor=sqlconnection.cursor()
    query1=f"SELECT username, password From users WHERE username = {UN} AND password={PW}"
    rows=Cursor.execute(query1)
    rows=rows.fetchall()
    if len(rows)>0:
        return render_template("/home.html")
    return redirect("/")
    
   

@app.route('/signup-form',methods=['POST','GET'])
def signup():
    if request.method=="POST":
        dUN=request.form['dusername']
        dPW= request.form['dpassword']
        dmail=request.form['dE-mail']
        dtown=request.form['dTown']
        
        sqlconnection=sqlite3.Connection(basedir+'\Login.db')
        Cursor=sqlconnection.cursor()
        query1=f"INSERT INTO users  VALUES ({dUN} ,{dPW},{ dmail},{dtown})"
        Cursor.execute(query1)
        sqlconnection.commit()
        return redirect("/home.html")
        
    return render_template("login.html")
        


database={'stage':'123456','STAGE':'123456','STAGE':'123456'}
@app.route('/login-form',methods=['POST','GET'])
def login():
    if(request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')     
        if username == database['username'] and password == database['password']:
            
            session['user'] = username
            return redirect('/dashboard')

        return "<h1>Wrong username or password</h1>"    #if the username or password does not matches 

    return render_template("home.html")


@app.route("/home.html",methods=['POST','GET'])
def home():
    return render_template("home.html")

@app.route("/contact.html",methods=['POST','GET'])
def contact():
    return render_template("contact.html")


@app.route("/similarity.html",methods=['POST','GET'])
def similarity():
    return render_template("similarity.html")



@app.route('/',methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(app.config['UPLOADED_PATH'],secure_filename(f.filename)))
    return render_template("similarity.html")

@app.route('/predict',methods=['POST'])
def predict():
    
    '''
    store txt
    
    '''
    if request.method == 'POST':
        import glob
        import os
        from similarité_cosinus_deux_doc import similarity_cosine
        from similarity_strsimpy import Levenshtein_,jarowinkler_,nGramSimilarity_,normalized_Levenshtein_
        from Nltk_similarity import cosine_sim
        list=["",""]
        files_path=basedir.join("uploads_")
        for filename in glob.glob(files_path.join('*.txt')):
            compt=0
            with open(os.path.join(os.getcwd(), filename), 'r') as f:
                text = f.read()
                list[compt]=text
                compt=1
        text1,text2=list[0]  , list[1]
        choice_similarity=request.form.get("similarity_select")
        
        if choice_similarity=="Similarity spacy":
            output=similarity_cosine(text1,text2)
        elif choice_similarity=="Nlp similarity":
            # output=cosine_sim(text1,text2)
            output=similarity_cosine(text1,text2)
        elif choice_similarity=='Levenshtein':
            paseur= Levenshtein_
            output=paseur(text1,text2)
        elif choice_similarity=='Normalized levenshtein':
            paseur= normalized_Levenshtein_
            output=paseur(text1,text2)
        elif choice_similarity=='Jarowinkler':
            paseur= jarowinkler_
            output=paseur(text1,text2)
        elif choice_similarity=='NGram similarity':
            paseur= nGramSimilarity_
            output=paseur(text1,text2,4)
        else:
            output ="error"
            
        flash('   {} '.format(output))
        for py_file in glob.glob(files_path.join('*.txt')):
            os.remove(py_file)
         
    return render_template("similarity.html")
       
@app.route("/signin.html",methods=['POST','GET'])
def signin():
    return render_template("signin.html")         



if __name__=="__main__":
    app.run(debug=True)


