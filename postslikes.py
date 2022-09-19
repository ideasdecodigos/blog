from flask import flash, session
from IPython.display import HTML
from model.funcs import cipherAbb

class PostsLikes():
    def __init__(self) -> None:
        pass    
    
    def switchLikes(self, id_post, conn):
        try:        
            cursor = conn.connection.cursor()
            cursor.execute("call likes(%s, %s)",(id_post, session['id_user']))
            conn.connection.commit()
            return True
        except:
            return False
        
    def dislike(self, id_post, conn):
        try:
            cursor = conn.connection.cursor()
            cursor.execute("DELETE FROM posts_likes WHERE post_like= %s AND user_like = %s ",(id_post, session['id_user']))
            conn.connection.commit()
            return True
        except:
            return False
            
    def likes(self,id_post, conn):
        try:
            cursor = conn.connection.cursor()
            # cursor.execute("SELECT COUNT(post_like)AS likes FROM posts_likes WHERE post_like = %s ",(id_post,))  
            cursor.execute("""SELECT id_post,
                        (SELECT counter_view FROM posts_views WHERE post_view = id_post)AS vistas, 
                        (SELECT COUNT(*) FROM comments WHERE post_comment=id_post)AS comments, 
                        (SELECT COUNT(*) FROM posts_likes WHERE post_like=id_post)AS likes 
                        FROM posts WHERE id_post={} """.format(id_post))  
            datas = cursor.fetchall() 
            for data in datas:
                return (data[0],cipherAbb(data[1]),cipherAbb(data[2]),cipherAbb(data[3]))
                
        except:
            return '-<>>'
        
    def isliked(self,id_post, conn):
        try:
            cursor = conn.connection.cursor()
            cursor.execute("SELECT COUNT(post_like) FROM posts_likes WHERE post_like = %s AND user_like = %s",(id_post, session['id_user']))  
            likes = cursor.fetchone()
            return True if likes[0] > 0 else False
        except:
            return False
        
            