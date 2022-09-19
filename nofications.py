from flask import flash, session
from IPython.display import HTML

class Notify():
    def __init__(self) -> None:
        pass    
            
    def read_alerts(self, id, conn):
        try:
            cursor = conn.connection.cursor()
            cursor.execute("UPDATE notifications SET status_info='false' WHERE id_info= '{}' ".format(id))
            conn.connection.commit()
            return True
        except:
            return False
        
    def del_alerts(self, id, conn):
        try:
            cursor = conn.connection.cursor()
            cursor.execute("DELETE FROM notifications WHERE id_info= '{}' ".format(id))
            conn.connection.commit()
            return True
        except:
            return False
            
    def alerts(self, conn):
        try:
            if 'id_user' in session:
                sqlquery ="SELECT * FROM notifications WHERE user_info={} OR scope_info='public' ORDER BY id_info DESC".format(session['id_user'])
            else:
                sqlquery = "SELECT * FROM notifications WHERE scope_info='public' ORDER BY id_info DESC"
                
            cursor = conn.connection.cursor()
            cursor.execute(sqlquery)  
            return cursor.fetchall()
        except:
            return ['']
        
            