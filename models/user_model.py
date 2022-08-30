from datetime import datetime, timedelta
import mysql.connector
import json
from flask import make_response, jsonify
import jwt
from configs.config import dbconfig
from app import cursor

class user_model():
        
    def all_user_model(self):
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        if len(result)>0:
            return {"payload":result}
            # return make_response({"payload":result},200)
        else:
            return "No Data Found"
    
    def add_user_model(self,data):
        cursor.execute(f"INSERT INTO users(name, email, phone, role, password) VALUES('{data['name']}', '{data['email']}', '{data['phone']}', '{data['role']}', '{data['password']}')")
        return make_response({"message":"CREATED_SUCCESSFULLY"},201)

    def delete_user_model(self,id):
        cursor.execute(f"DELETE FROM users WHERE id={id}")
        if cursor.rowcount>0:
            return make_response({"message":"DELETED_SUCCESSFULLY"},202)
        else:
            return make_response({"message":"CONTACT_DEVELOPER"},500)
        
    
    def update_user_model(self,data):
        cursor.execute(f"UPDATE users SET name='{data['name']}', email='{data['email']}', phone='{data['phone']}' WHERE id={data['id']}")
        if cursor.rowcount>0:
            return make_response({"message":"UPDATED_SUCCESSFULLY"},201)
        else:
            return make_response({"message":"NOTHING_TO_UPDATE"},204)

    def patch_user_model(self, data):
        qry = "UPDATE users SET "
        for key in data:
            if key!='id':
                qry += f"{key}='{data[key]}',"
        qry = qry[:-1] + f" WHERE id = {data['id']}"
        cursor.execute(qry)
        if cursor.rowcount>0:
            return make_response({"message":"UPDATED_SUCCESSFULLY"},201)
        else:
            return make_response({"message":"NOTHING_TO_UPDATE"},204)

    def pagination_model(self, pno, limit):
        pno = int(pno)
        limit = int(limit)
        start = (pno*limit)-limit
        qry = f"SELECT * FROM users LIMIT {start}, {limit}"
        cursor.execute(qry)
        result = cursor.fetchall()
        if len(result)>0:
            return make_response({"page":pno, "per_page":limit,"this_page":len(result), "payload":result})
        else:
            return make_response({"message":"No Data Found"}, 204)

    def upload_avatar_model(self, uid, db_path):
        cursor.execute(f"UPDATE users SET avatar='{db_path}' WHERE id={uid}")
        if cursor.rowcount>0:
            return make_response({"message":"FILE_UPLOADED_SUCCESSFULLY", "path":db_path},201)
        else:
            return make_response({"message":"NOTHING_TO_UPDATE"},204)

    def get_avatar_path_model(self, uid):
        cursor.execute(f"SELECT avatar FROM users WHERE id={uid}")
        result = cursor.fetchall()
        if len(result)>0:
            print(type(result))
            return {"payload":result}
        else:
            return "No Data Found"  
        
    def user_login_model(self, username, password):
        cursor.execute(f"SELECT id, roleid, avatar, email, name, phone from users WHERE email='{username}' and password='{password}'")
        result = cursor.fetchall()
        if len(result)==1:
            exptime = datetime.now() + timedelta(minutes=1)
            exp_epoc_time = exptime.timestamp()
            data = {
                "payload":result[0],
                "exp":int(exp_epoc_time)
            }
            print(int(exp_epoc_time))
            jwt_token = jwt.encode(data, "Sagar@123", algorithm="HS256")
            return make_response({"token":jwt_token.decode('UTF-8')}, 200)
        else:
            return make_response({"message":"NO SUCH USER"}, 204)
            