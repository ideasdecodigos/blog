from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash, session
from IPython.display import HTML
from model.funcs import *

class Users():
    def __init__(self) -> None:
        pass
    
    
    def report(self, origen, actions, info, table, conn):
        try:
            info = info.encode('ascii', 'xmlcharrefreplace')
            cursor = conn.connection.cursor()            
            cursor.execute("""INSERT INTO reports(user_report,origen_report, action_report, info_report, table_report)
                        VALUES(%s,%s,%s,%s,%s)""",(session['id_user'], origen, actions, info, table))
            conn.connection.commit()
            return True
        except:
            flash('Somenthing went wrong!','error')
            return False
    
    def createUser(self, name, mail, password, conn):
        try:
            name = name.encode('ascii', 'xmlcharrefreplace')
            passEncripted = generate_password_hash(password)
            cursor = conn.connection.cursor()
            
            cursor.execute("SELECT COUNT(mail_user) FROM users WHERE mail_user = %s ",(mail,)) 
            counter = cursor.fetchone()
            if counter[0] > 0:
                flash(f'This mail ({mail}) is already registred!','warning')
                return False
            else:
                cursor.execute("INSERT INTO users(name_user, mail_user, pass_user)VALUES(%s,%s,%s)",(name, mail, passEncripted))
                conn.connection.commit()
                flash('Created successfully','success')
                return True
        except:
            flash('Somenthing went wrong!','error')
            return False
        
    def updateUser(self, name, mail, password, phone, country,about, conn):
        try:
            #EMOJI FORMAT
            name = name.encode('ascii', 'xmlcharrefreplace')
            country = country.encode('ascii', 'xmlcharrefreplace')
            about = about.encode('ascii', 'xmlcharrefreplace')
            
            passEncripted = generate_password_hash(password)
            cursor = conn.connection.cursor()
            cursor.execute("""UPDATE users SET 
                    name_user=%s, mail_user=%s, pass_user=%s, phone_user=%s, country_user=%s, about_user=%s
                    WHERE id_user=%s """,(name, mail, passEncripted,phone,country,about,session['id_user']))
            conn.connection.commit()
            self.isRegistred(mail,password,conn)
            flash("Updated successfully!", 'success')
            return True
        except:
            flash("We couldn't update your data!" , 'error')
            return False
            
    def getUserById(self, id, conn):
        try:
            cursor = conn.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE id_user = %s ",(id,)) 
            data = cursor.fetchone()
            user={
                'id_user':data[0],
                'name_user':data[1].title(),
                'mail_user':data[2],
                'phone_user':data[4],
                'country_user':data[5],
                'about_user':data[6],
                'foto_user':data[7],
                'wallpaper_user':data[8],
                'date_user':data[9].strftime("%b %d, %Y")
            }            
            return user
        except:
            return []
            
    def getRandomUsers(self, conn):
        try:
            cursor = conn.connection.cursor()
                # cursor.execute("SELECT DISTINCT id_user, name_user, foto_user FROM users WHERE id_user != %s ORDER BY RAND() LIMIT 25",(session['id_user'],)) 
            cursor.execute("""SELECT DISTINCT id_user, name_user,about_user, foto_user,
                (SELECT 'true' FROM followers WHERE followed=id_user AND follower=%s) AS follow,
                (SELECT COUNT(followed) FROM followers WHERE followed=id_user) AS following,
                (SELECT COUNT(follower) FROM followers WHERE follower=id_user) AS followers 
                FROM users WHERE id_user != %s ORDER BY RAND() LIMIT 15""",(session['id_user'],session['id_user'])) 
            array_data = cursor.fetchall()
            users=[]
            
            for user in array_data:                
                foto = "<strong>"+user[1][:1].title()+"</strong>"  if user[3] == '' or user == None else "<img width='50px' src='"+user[3]+"'>"                
                follow = "Unfollow"  if user[4] == 'true' else "Follow"
                
                users.append( (user[0],user[1].title(),user[2].title(),foto,follow,cipherAbb(user[5]),cipherAbb(user[6])) )
            return users
        
        except:
            return []
            
    def mailExists(self, email,  conn):            
        try:
            cursor = conn.connection.cursor()
            cursor.execute("SELECT COUNT(mail_user) FROM users WHERE mail_user = %s ",(email,))  
            user = cursor.fetchone()            
            return True if user[0] > 0 else False   
        except:
            return False
        
    def isRegistred(self, email, password, conn):            
        try:
            cursor = conn.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE mail_user = %s ",(email,)) 
            # cursor.execute("SELECT id_user, name_user, mail_user, pass_user, date_user FROM users WHERE mail_user = %s",(email,)) 
            user = cursor.fetchone()
            
            if check_password_hash(user[3],password):
                session['id_user']=user[0]
                session['name_user']=HTML(user[1].title())
                session['mail_user']=user[2]
                session['phone_user']=user[4]
                session['country_user']=HTML(user[5])
                session['about_user']=HTML(user[6])
                session['foto_user']=user[7]
                session['wallpaper_user']=user[8]
                session['date_user']=user[9].strftime("%b %d, %Y")
                return True        
            return False 
        except:
            flash('Something went wrong!','error')      
                    
    def updateImg(self, fcell, fpath, conn):        
        try:
            if 'static/uploads/' in fpath: fpath = fpath.replace('static/uploads/','../static/uploads/')
            
            cursor = conn.connection.cursor()
            cursor.execute("UPDATE users SET {} = '{}' WHERE id_user={}".format(fcell, fpath, session['id_user'])) 
            conn.connection.commit()
            return True    
        except:
            return False             