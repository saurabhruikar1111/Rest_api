from email import parser
from multiprocessing import connection
from flask_restful import Resource,reqparse
import sqlite3
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type=int,
    required = True,
    help = 'you must enter the price'
    )
    
    @jwt_required()
    def get(self,name):
        item = self.find_by_name(name)
        if item:
            return {'item': {'name':item['name'],'price':item['price']}}
        return {'message':'item not found'}
    
    @classmethod
    def find_by_name(cls,name):
        connection=sqlite3.connect('data.db')
        cursor = connection.cursor()
        '''  
        function find_by_name takes name of the item and returns
        dictionary of {name:somrthing,price:something} of 
        a item if present otherwise returns None
        '''
        select_query = "SELECT * FROM  items WHERE name=?"
        result = cursor.execute(select_query,(name,))
        row=result.fetchone()
        connection.close()
        if row:
            item={'name':row[1],'price':row[2]}
            return item
    
    def post(self,name):
        if self.find_by_name(name):
            return {'message': f'an item with {name} aleready exisits'},400
        
        data = Item.parser.parse_args()
        item = {'name':name,'price':data['price']}
        try:
            Item.insert(item)
        except:
            return {'msg':'can not insert item right now please try again later'},500
        
        return item,201

    def delete(self,name):
        connection=sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query,(name,))
        
        connection.commit()
        connection.close()
        return {'msg': f"{name} deleted sucessfully"}

    def put(self,name):
        data = Item.parser.parse_args()
        item=self.find_by_name(name)
        updated_item={'name':name,'price':data['price']}
        if item is None:
            try:
                Item.insert(updated_item)
                
            except:
                return f"unable to add item to server please try again later",500
            
        else:
            self.update(updated_item) 
        return updated_item

    @classmethod
    def update(cls,item):
        connection=sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query,(item['price'],item['name']))
        
        connection.commit()
        connection.close()
    @classmethod
    def insert(cls,item):
        connection=sqlite3.connect('data.db')
        cursor = connection.cursor()

        insert_query= "INSERT INTO items VALUES(NULL,?,?)"
        cursor.execute(insert_query,(item['name'],item['price']) )
        connection.commit()
        connection.close()


class ItemList(Resource):
    def get(self):
        connection=sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM items"
        res=cursor.execute(query)
        items=[]
        for row in res:
            items.append( {'name':row[1], 'price':row[2] } )
        
        if res is None:
            return {'msg':'no item found'}
        connection.commit()
        connection.close()

        return items