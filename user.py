import sqlite3
from flask_restful import Resource,reqparse


class User:
    def __init__(self,id,username,password) :
        self.id=id
        self.username = username
        self.password=password

    @classmethod
    def find_by_username(cls,username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM users WHERE username=?'
        result = cursor.execute(query,(username,))
        row = result.fetchone()
        if  row:
            user = cls(*row)
        else:
            user=None
        connection.close()
        return user

    @classmethod
    def find_by_id(cls,id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM users WHERE id=?'
        result = cursor.execute(query,(id,))
        row = result.fetchone()
        if  row:
            user = cls(*row)
        else:
            user=None
        connection.close()
        return user

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
    type=str,
    required = True,
    help = 'you must enter the username'
    )
    
    parser.add_argument('password',
    type=str,
    required = True,
    help = 'you must enter the password'
    )
    
    def post(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'INSERT INTO users VALUES(NULL,?,?)'
        data = UserRegister.parser.parse_args()
        
        user=User.find_by_username(data['username'])
        if user:
            return f"user with name {data['username']} aleready exisits please"
        
        cursor.execute(query, (data['username'],data['password']) )

        connection.commit()
        connection.close()

        return {'msg':'User created sucessfully'}
