from flask import flash, session
from IPython.display import HTML

class Comments():
    def __init__(self) -> None:
        pass

    def addComment(self, id_post, comment, id_reply, text_reply, conn):
        try:
            comment = comment.encode('ascii', 'xmlcharrefreplace')
            text_reply = text_reply.encode('ascii', 'xmlcharrefreplace')
            cursor = conn.connection.cursor()
            cursor.execute("""INSERT INTO comments(post_comment, user_comment, content_comment, id_reply, content_reply)
                        VALUES(%s,%s,%s,%s,%s)""", (id_post, session['id_user'], comment, id_reply, text_reply))
            conn.connection.commit()
            return True
        except:
            flash("We counldn't add your comment!", "error")
            return False

    def deleteComment(self, id, conn):
        try:
            cursor = conn.connection.cursor()
            cursor.execute(
                "DELETE FROM comments WHERE id_comment = %s ", (id,))
            conn.connection.commit()
            return True
        except:
            return False

    def comments(self, id_post, conn):
        try:
            cursor = conn.connection.cursor()
            cursor.execute("""SELECT *, (SELECT name_user FROM users WHERE id_user=user_comment)AS user, 
                        (SELECT COUNT(*) FROM comments_likes WHERE comment_favorite = id_comment) AS likes
                        FROM comments WHERE post_comment = %s """, (id_post,))
            data_posts = cursor.fetchall()
            posts = []
            aux1 = ''
            aux2 = ''
            for post in data_posts:
                aux1 = post[6].strftime("%b %d, %Y")
                if aux1 != aux2:
                    aux2 = aux1
                    aux1 = post[6].strftime("%b %d, %Y")
                    aux_date = post[6].strftime("%b %d, %Y")
                else:
                    aux_date = ''
                posts.append((post[0], post[1], post[2], HTML(post[3]), post[4], post[5], aux_date, post[6].strftime("%H:%M%p"), post[7], post[8]))
            return posts
            # return a list with 8 positions, id-comment[0], id-post[1], id-user[2], comment[3], id-reply[4]
            # content-reply[5] ,date[6], hour[7] and user_name[8], comment_likes[9]
        except:
            return []

    
