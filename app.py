from flask import Flask, jsonify, render_template, request, redirect, session, url_for, make_response, flash
from flask_mysqldb import MySQL
from model.postslikes import PostsLikes
from model.comments import Comments
from model.commentslikes import CommentsLikes
from model.followers import Followers
from config import config
from model.users import Users
from model.nofications import Notify
from model.posts import Posts
# from werkzeug.security import generate_password_hash, check_password_hash
from IPython.display import HTML
import os

app =Flask(__name__)

conn = MySQL(app)

# @app.before_request
# def before_request():
#     print("execute code before a petition")
    
# @app.after_request
# def after_request(response):
#     print("execute code after a petition")
#     return response

def multi_params():
    #****example with several params
    # http://localhost:5000/params?prm1=maria mena&prm2=todo va bien'
    print(request)
    print(request.args)
    print(request.args.get('prm1'))
    return 'Ok'

def no_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    # session['theme'] = "theme-dark"
    return render_template('index.html')

#------------------USERS AREA-----------------
@app.route('/verify_mail', methods = ['POST'])
def verify_mail():
    if request.method == 'POST' and Users().mailExists(request.form.get('mail'),conn):
        return {'info':'Email already exists!','color':'red'}
    return {'info':'','color':'white'}

@app.route('/signup', methods=['GET', 'POST'])
def signup(): 
    if request.method == 'POST' and request.form['mail'] != "" and request.form['password'] != "" and request.form['username'] != "":
        if Users().createUser(request.form['username'],request.form['mail'],request.form['password'], conn):
            if Users().isRegistred(request.form['mail'],request.form['password'], conn):
                return redirect(url_for('account'))
    return render_template('signup.html')

@app.route('/updateUser', methods=['GET', 'POST'])
def updateUser(): 
    if request.method == 'POST' and request.form['usermail'] != "" and request.form['password'] != "" and request.form['username'] != "":
        if Users().updateUser(request.form['username'],request.form['usermail'],request.form['password'],request.form['userphone'],request.form['usercountry'],request.form['userabout'], conn):
            return redirect(url_for('account'))
    return render_template('updateUser.html')

@app.route('/upload/<actions>', methods = ['GET', 'POST'])
def upload(actions):
    if request.method == 'POST':
        fullPath = request.form.get('fpath')
        if actions == 'ftupload' or actions == 'wpupload':
            f = request.files['fpath']
            fullPath = f"static/uploads/{f.filename}"
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
                    
        if Users().updateImg(request.form.get('fcell'), fullPath, conn) :
            session[request.form.get('fcell')]  = fullPath   
            return redirect(url_for('account'))          
    return render_template('upload.html', data=actions)
	
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and request.form['mail'] != "" and request.form['password'] != "":        
        if Users().isRegistred(request.form['mail'],request.form['password'], conn):
            flash(message='Welcome!', category='info')
            return redirect(url_for('account'))
        else:
            flash('Invalid credentials', 'warning')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    # remove the user from the session if it's there
    session.pop('id_user', None)
    session.pop('name_user', None)
    session.pop('mail_user', None)
    session.pop('date_user', None)
    return redirect(url_for('index'))

#---------------LOGGED USER-------------------
@app.route('/account')
def account():
    data={
        'posts':Posts().getPostByAuthor(session['id_user'], conn),
        'followers' : Followers().followers(session['id_user'],conn),
        'following' : Followers().following(session['id_user'],conn)
    }     
    return render_template('account.html', data = data)

@app.route('/profile/<id>')
def profile(id):
    follow = None
    if 'id_user' in session and Followers().isFollowing(id, session['id_user'], conn):
        follow = 'Unfollow'
    else:
        follow = 'Follow'
    
    
    data={
        'user':Users().getUserById(id, conn),
        'posts':Posts().getPostByAuthor(id, conn),
        'following' : Followers().following(id,conn),
        'followers' : Followers().followers(id,conn),
        'follow' : follow
    } 
        
    return render_template('profile.html', data = data)

@app.route('/follow', methods=['POST'])
def follow():    
    if request.method == "POST" and 'id_user' in session:
        userid = request.form.get('profile')
        if Followers().isFollowing(userid, session['id_user'], conn):
            Followers().unfollow(userid, conn)
            return  {'text':'Follow','followers':Followers().followers(userid,conn)}
        else:
            Followers().follow(userid, conn)
            return {'text':'Unfollow','followers':Followers().followers(userid,conn)}

#---------------POSTS AREA--------------------
@app.route('/forum', methods=['GET', 'POST'])
def forum():
    
    if request.method == "POST" and request.form['currentPage'] != None: 
        posts = Posts().infiniteScroll(request.form['currentPage'], conn)
        return jsonify(posts)
    elif request.method == "POST" and request.form['browser'] != "":        
        posts = Posts().getPostByContent(request.form['browser'],conn)
        return jsonify(posts)
    
    return render_template('forum.html')

@app.route('/forum_filter', methods=['POST'])
def forum_filter():
    if request.method == "POST" and request.form['browser'] != "":        
        posts = Posts().getPostByContent(request.form['browser'],conn)
        return jsonify(posts)

@app.route('/popular_posts', methods=['POST'])
def popular_posts():
    if request.method == "POST" and request.form['request'] != "":     
        popular={
            'recent':Posts().newestPosts(conn),
            'likes':Posts().mostLikedPosts(conn),
            'comments':Posts().mostCommentedPosts(conn),
            'visits':Posts().mostVisitedPosts(conn)
        }    
        return jsonify(popular)

@app.route('/notifications', methods=['POST'])
def notifications():
    if request.method == "POST" and request.form['info'] == '':        
        posts = Notify().alerts(conn)
        return jsonify(posts)
    
@app.route('/readAlerts', methods=['POST'])
def readAlerts():
    if request.method == "POST" and request.form['id_alert'] != '':        
        posts = Notify().read_alerts(request.form['id_alert'],conn)
        return jsonify(posts)
    
@app.route('/delAlerts', methods=['POST'])
def delAlerts():
    if request.method == "POST" and request.form['id_alert'] != '':        
        posts = Notify().del_alerts(request.form['id_alert'],conn)
        return jsonify(posts)

@app.route('/createpost',  methods=['GET', 'POST'])
def createPost():
    if request.method =='POST' and 'id_user' in session and request.form['title'] !='' and request.form['post'] != '':
        if Posts().createPost(request.form['title'],request.form['category'],request.form['post'], session['id_user'],conn):
            return redirect(url_for('forum'))
    return render_template('createPost.html')

@app.route('/updatepost/<id>',  methods=['GET', 'POST'])
def updatePost(id):
    if request.method =='POST' and request.form['title'] !='' and request.form['post'] != '' and 'id_user' in session:
        if Posts().updatePost(id, request.form['title'],request.form['category'], request.form['post'], conn):
            return redirect('/post/'+ id)
        
    data = Posts().getPostById(id, conn) 
    post={
        'id':data[0],
        'title':data[1],
        'content':data[2],
        'author':data[3],
        'categories':data[4],
        'date':data[5],
        'author_name':data[6]
    }   
    return render_template('updatePost.html', post=post)

@app.route('/deletepost/<id>')
def deletePost(id):
    if Posts().deletePost(id, conn):
        return redirect(url_for('forum'))
    flash("Something went wrong!")

@app.route('/post/<id>')
def post(id):
    
    data = Posts().setView(id, conn) 
    data = Posts().getPostById(id, conn) 
    post={
        'id':data[0],
        'title':HTML(data[1]), 
        'content':HTML(data[2]),
        'author':data[3],
        'categories':data[4],
        'date':data[5].strftime("%A, %b %d, %Y | %H:%M%p"),
        'author_name':HTML(data[6]),
        'posts':Posts().getPostByAuthorLimited(data[3], conn)
    }       
    return render_template('post.html', post=post)

@app.route("/addComent", methods=['POST'])
def addComment():
    if request.method == "POST"  and request.form.get('comment') != "" and 'id_user' in session:
        Comments().addComment(request.form['id_post'], request.form['comment'], request.form.get('id_reply'),request.form.get('text_reply'), conn)
    return ""

@app.route("/delcomment", methods=['POST'])
def delComment():
    if request.method == "POST" and request.form.get('id_comment') != "" and 'id_user' in session:
        Comments().deleteComment(request.form['id_comment'], conn)
        flash(request.form.get('id_comment'),'info')
    return ""

@app.route("/showComments", methods=['POST'])
def showComments():
    if request.method == "POST"  and request.form.get('id_post'):
        comments = Comments().comments(request.form['id_post'],conn)
        return jsonify(comments)
        
@app.route("/randomUsers", methods=['GET','POST'])
def randomUsers():
    # if request.method == "POST":
    #     users = Users().getRandomUsers(conn)
    #     return jsonify(users) 
    return render_template("randomusers.html")
        
@app.route("/reports", methods=['POST'])
def reports():
    if request.method == "POST": 
        if Users().report(request.form.get('origen'),request.form.get('actions'),request.form.get('info'),request.form.get('table'), conn) : 
            return ""    
        return "" 
        
@app.route("/getlikes", methods=['POST'])
def getlikes():
    if request.method == "POST" and request.form['id_post'] != "":
        likes=PostsLikes().likes(request.form['id_post'], conn)
        return jsonify(likes)

@app.route("/postslikes", methods=['POST'])
def postslikes():
    if request.method == "POST" and request.form['id_post'] != "" and 'id_user' in session:
        if PostsLikes().switchLikes(request.form['id_post'], conn):
            likes = PostsLikes().likes(request.form['id_post'], conn)
            return str(likes[0])
    
@app.route("/getcommentslikes", methods=['POST'])
def getcommentslikes():
    if request.method == "POST" and request.form.get('id_comment') != "":
        favorites = CommentsLikes().favorites(request.form['id_comment'], conn)
        return str(favorites[0])

@app.route("/commentslikes", methods=['POST'])
def commentslikes():
    if request.method == "POST" and request.form.get('id_comment') != "" and 'id_user' in session:
        if CommentsLikes().switchFavorite(request.form['id_comment'], conn):
            favorites = CommentsLikes ().favorites(request.form['id_comment'], conn)
            return str(favorites[0])
    
#------------------OTHER PAGES---------------
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/gallery')
def gallery(): 
    outputs=[]
    try:
        x='jose@gmail.com'
        cursor = conn.connection.cursor()
        cursor.execute("SELECT name_user FROM users WHERE mail_user ='"+x+"'")
        
        outputs = cursor.fetchone()
    except Exception as ex:
        outputs='Error'
    return render_template('gallery.html',data=outputs)

@app.route('/friends')
def friends(): 
    return render_template('friends.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        ruta=f"static/uploads/{f.filename}"
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        
        return """file uploaded successfully 
    <h1>hola</h1>
    <img src='{}'>
    """.format(ruta)

if __name__ == '__main__':
    app.config.from_object(config['configurations'])
    # app.add_url_rule('/params',view_func=multi_params)
    
    app.register_error_handler(404, no_found) 
    app.run(debug=True)