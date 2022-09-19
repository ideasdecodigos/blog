
import re, pickle
from turtle import pos, position
from flask_mysqldb import MySQL
from flask import flash, session
from IPython.display import HTML
from model.funcs import *


class Posts():
    def __init__(self) -> None:
        pass
    
    
    def createPost(self, title, category, post, author, conn):
        try:
            #EMOJI FORMAT
            title = title.encode('ascii', 'xmlcharrefreplace')
            post = post.encode('ascii', 'xmlcharrefreplace')
            
            cursor = conn.connection.cursor()
            cursor.execute("INSERT INTO posts(title_post, categories_post, content_post, author_post)VALUES(%s,%s,%s,%s)",(title, category, post, author))
            conn.connection.commit()
            flash("Published succefully!","success")
            return True
        except:
            flash("Your Post wasn't published!", "error")
            return False
        
    def updatePost(self, id, title, category, post, conn):
        try:
            title = title.encode('ascii', 'xmlcharrefreplace')
            post = post.encode('ascii', 'xmlcharrefreplace')
            cursor = conn.connection.cursor()
            cursor.execute("UPDATE posts SET title_post=%s, categories_post=%s, content_post=%s WHERE id_post=%s",(title,category, post, id))
            conn.connection.commit()
            flash("Updated succefully!",'success')
            return True
        except:
            flash("Something went wrong!","error")
            return False
        
    def getPostById(self, id, conn):
        try:
            cursor = conn.connection.cursor()
            cursor.execute("SELECT *, (SELECT name_user FROM users WHERE id_user = author_post )AS author FROM posts WHERE id_post= %s",(id,))
            return cursor.fetchone()
        except:
            return []
        
    def getPostByContent(self, filter, conn):
        filter = "%"+filter+"%"
        try:
            cursor = conn.connection.cursor()
            cursor.execute("""SELECT id_post,title_post,content_post,author_post,categories_post,date_post,name_user,foto_user,
                        (SELECT counter_view FROM posts_views WHERE post_view = id_post)AS vistas, 
                        (SELECT COUNT(*) FROM comments WHERE post_comment=id_post)AS comments, 
                        (SELECT COUNT(*) FROM posts_likes WHERE post_like=id_post)AS likes 
                        FROM users INNER JOIN posts ON users.id_user=posts.author_post 
                        WHERE title_post LIKE %s OR content_post LIKE %s OR name_user LIKE %s OR categories_post LIKE %s """,(filter,filter,filter,filter)) 
            data_posts = cursor.fetchall()
            posts=[]
            for post in data_posts:
                
                # Remove tags HTML from content posts and limit to 200 characters
                if len(post[2]) > 200:
                    content=re.sub(r'<[^>]*?>', '-', post[2])
                    content = content[:200] +' ...'
                else:
                    content=re.sub(r'<[^>]*?>', '', post[2])
                    
                    
                if post[8] == None or post[8] == "": 
                    views=0
                else:
                    views=post[8]
                
                
                if 'static/imgs/' in post[7]:
                    foto=post[7].replace('static/imgs/', '../static/imgs/')
                else:
                    foto = post[7]  
                    
                posts.append((post[0],post[1][:50].title(),content,post[3],post[4].split(' '),post[5].strftime("%b %d, %Y"),post[6].title(),foto,views,post[9],post[10]))
            
            return posts
        except:
            return ["--"]
        
    def getPostByAuthorLimited(self, author, conn):
        try:
            cursor = conn.connection.cursor()
            cursor.execute("""SELECT id_post,title_post,content_post,author_post,categories_post,date_post,name_user,
                        (SELECT COUNT(*) FROM posts WHERE author_post = %s)AS total FROM users INNER JOIN posts 
                        ON users.id_user=posts.author_post WHERE author_post = %s ORDER BY RAND() LIMIT 6""",(author, author))
            
            data_posts = cursor.fetchall()
            posts=[]
            for post in data_posts:
                # Remove tags HTML from content posts and limit to 200 characters
                if len(post[2]) > 200:
                    content=re.sub(r'<[^>]*?>', '-', post[2])
                    content = content[:200] +' ...»'
                else:
                    content=re.sub(r'<[^>]*?>', '', post[2])
                posts.append((post[0], HTML(post[1][:30].title()), content, post[3], post[4].split(' '),post[5].strftime("%b %d, %Y"),post[6],post[7]))
                # id[0], title[1], content[2],author[3],categoria[4]list, date[5],username[6],total[7]
            if len(posts) == 0:
                posts=[0]
            return posts
        except:
            return []
        
    def setView(self, id_post, conn):
        try:
            cursor = conn.connection.cursor()
            cursor.execute("CALL set_posts_views(%s)",(id_post, ))
            conn.connection.commit()
            
            return True
        except:
            return False
        
    def getPostByAuthor(self, author, conn):
        try:
            cursor = conn.connection.cursor()
            cursor.execute("""SELECT id_post,title_post,content_post,author_post,categories_post,date_post,name_user,
                        (SELECT COUNT(*) FROM posts WHERE author_post = %s)AS total FROM users INNER JOIN posts 
                        ON users.id_user=posts.author_post WHERE author_post = %s """,(author, author))
            
            data_posts = cursor.fetchall()
            posts=[]
            for post in data_posts:
                # Remove tags HTML from content posts and limit to 200 characters
                if len(post[2]) > 200:
                    content=re.sub(r'<[^>]*?>', '-', post[2])
                    content = content[:200] +' ...'
                else:
                    content=re.sub(r'<[^>]*?>', '', post[2])
                posts.append((post[0], post[1][:50].title(), content, post[3], post[4].split(' '),post[5].strftime("%b %d, %Y"),post[6],post[7]))
                # id[0], title[1], content[2],author[3],categoria[4]list,date[5],username[6],total[7]
            if len(posts) == 0:
                posts=[0]
            return posts
        except:
            return []
        
    def deletePost(self, id, conn):
        try:
            cursor = conn.connection.cursor()
            cursor.execute("DELETE FROM posts WHERE id_post = %s ",(id,))
            conn.connection.commit()
            return True
        except:
            return False
            
    def posts(self, conn):
        try:
            cursor = conn.connection.cursor()
            cursor.execute("""SELECT id_post,title_post,content_post,author_post,categories_post,date_post,name_user 
                        FROM users INNER JOIN posts ON users.id_user=posts.author_post ORDER BY RAND()""")    
            data_posts = cursor.fetchall()
            posts=[]
            for post in data_posts:
                # Remove tags HTML from content posts and limit to 200 characters
                if len(post[2]) > 200:
                    content=re.sub(r'<[^>]*?>', '-', post[2])
                    content = content[:200] +' ...'
                else:
                    content=re.sub(r'<[^>]*?>', '', post[2])
                posts.append((post[0], post[1][:50].title(), content, post[3], post[4].split(' '), post[5].strftime("%b %d, %Y"),post[6]))
            
            return posts
        except:
            return ['']
            
    def infiniteScroll(self, page, conn):
        try:
            limit = 10
            position = (int(page ) - 1) * limit
            cursor = conn.connection.cursor()
            cursor.execute("""SELECT id_post,title_post,content_post,author_post,categories_post,date_post,name_user,foto_user,
                        (SELECT counter_view FROM posts_views WHERE post_view = id_post)AS vistas, 
                        (SELECT COUNT(*) FROM comments WHERE post_comment=id_post)AS comments, 
                        (SELECT COUNT(*) FROM posts_likes WHERE post_like=id_post)AS likes 
                        FROM users INNER JOIN posts ON users.id_user=posts.author_post ORDER BY RAND() LIMIT {}, {}""".format(position, limit))    
            data_posts = cursor.fetchall()
            posts=[]
            for post in data_posts:
                
                # Remove tags HTML from content posts and limit to 200 characters
                if len(post[2]) > 200:
                    content=re.sub(r'<[^>]*?>', '-', post[2])
                    content = content[:200] +' ...'
                else:
                    content=re.sub(r'<[^>]*?>', '', post[2])
                    
                    
                if post[8] == None or post[8] == "": 
                    views=0
                else:
                    views=post[8]
                
                
                if 'static/imgs/' in post[7]:
                    foto=post[7].replace('static/imgs/', '../static/imgs/')
                else:
                    foto = post[7]
                
                posts.append((post[0],post[1][:300].title(),content,post[3],post[4].split(' '),post[5].strftime("%b %d, %Y"),post[6].title(),foto, cipherAbb(views),cipherAbb(post[9]),cipherAbb(post[10])))
            
            return posts
        except:
            return ['---']
        
    def newestPosts(self, conn):
        try:
            cursor = conn.connection.cursor()
            cursor.execute("""SELECT id_post,author_post,title_post,
                            (SELECT name_user FROM users WHERE id_user=author_post)AS name,
                            (SELECT COUNT(post_like) FROM posts_likes WHERE post_like=id_post)AS likes,
                            (SELECT COUNT(post_comment) FROM comments WHERE post_comment=id_post)AS comments,
                            (SELECT counter_view FROM posts_views WHERE post_view=id_post)AS visits,
                            date_post FROM posts ORDER BY id_post DESC LIMIT 3""")   
            data_posts = cursor.fetchall()
            posts=[]
            for post in data_posts:                    
                if post[6] == None or post[6] == "": 
                    views=0
                else:
                    views=post[6]              
                posts.append((post[0],post[1],post[2].title(),post[3].title(),cipherAbb(post[4]), cipherAbb(post[5]), cipherAbb(views), post[7].strftime("%b %d, %Y")))               
            return posts
        except:
            return ['']
        
    def mostLikedPosts(self, conn):
        try:
            cursor = conn.connection.cursor()
            cursor.execute("""SELECT id_post,author_post,title_post,
                            (SELECT name_user FROM users WHERE id_user=author_post)AS name,
                            (SELECT COUNT(post_like) FROM posts_likes WHERE post_like=id_post)AS likes,
                            (SELECT COUNT(post_comment) FROM comments WHERE post_comment=id_post)AS comments,
                            (SELECT counter_view FROM posts_views WHERE post_view=id_post)AS visits,
                            date_post FROM posts ORDER BY likes DESC LIMIT 3""")   
            data_posts = cursor.fetchall()
            posts=[]
            for post in data_posts:                    
                if post[6] == None or post[6] == "": 
                    views=0
                else:
                    views=post[6]              
                    posts.append((post[0],post[1],post[2].title(),post[3].title(),cipherAbb(post[4]), cipherAbb(post[5]), cipherAbb(views), post[7].strftime("%b %d, %Y")))                 
            return posts
        except:
            return ['']
        
    def mostCommentedPosts(self, conn):
        try:
            cursor = conn.connection.cursor()
            cursor.execute("""SELECT id_post,author_post,title_post,
                            (SELECT name_user FROM users WHERE id_user=author_post)AS name,
                            (SELECT COUNT(post_like) FROM posts_likes WHERE post_like=id_post)AS likes,
                            (SELECT COUNT(post_comment) FROM comments WHERE post_comment=id_post)AS comments,
                            (SELECT counter_view FROM posts_views WHERE post_view=id_post)AS visits,
                            date_post FROM posts ORDER BY comments DESC LIMIT 3""")   
            data_posts = cursor.fetchall()
            posts=[]
            for post in data_posts:                    
                if post[6] == None or post[6] == "": 
                    views=0
                else:
                    views=post[6]              
                    posts.append((post[0],post[1],post[2].title(),post[3].title(),cipherAbb(post[4]), cipherAbb(post[5]), cipherAbb(views), post[7].strftime("%b %d, %Y")))                 
            return posts
        except:
            return ['']
        
    def mostVisitedPosts(self, conn):
        try:
            cursor = conn.connection.cursor()
            cursor.execute("""SELECT id_post,author_post,title_post,
                            (SELECT name_user FROM users WHERE id_user=author_post)AS name,
                            (SELECT COUNT(post_like) FROM posts_likes WHERE post_like=id_post)AS likes,
                            (SELECT COUNT(post_comment) FROM comments WHERE post_comment=id_post)AS comments,
                            (SELECT counter_view FROM posts_views WHERE post_view=id_post)AS visits,
                            date_post FROM posts ORDER BY visits DESC LIMIT 3""")   
            data_posts = cursor.fetchall()
            posts=[]
            for post in data_posts:       
                if post[6] == None or post[6] == "": 
                    views=0
                else:
                    views=post[6]              
                posts.append((post[0],post[1],post[2].title(),post[3].title(),cipherAbb(post[4]), cipherAbb(post[5]), cipherAbb(views), post[7].strftime("%b %d, %Y")))              
            return posts
        except:
            return ['']
            