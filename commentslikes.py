from flask import flash, session
from IPython.display import HTML

class CommentsLikes():
    def __init__(self) -> None:
        pass    
    
    def switchFavorite(self, id_comment, conn):
        try:        
            cursor = conn.connection.cursor()
            cursor.execute("call switch_favorite_comment(%s, %s)",(id_comment, session['id_user']))
            conn.connection.commit()
            return True
        except:
            return False
    
    def favorites(self,id_comment, conn):
        try:
            cursor = conn.connection.cursor()
            cursor.execute("SELECT COUNT(comment_favorite)AS likes FROM comments_likes WHERE comment_favorite = %s ",(id_comment,))  
            favorites = cursor.fetchone() 
            return favorites 
        except:
            return 'none'
            