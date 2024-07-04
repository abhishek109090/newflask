from flask import Flask,redirect,url_for,render_template,jsonify,request
import psycopg2
from psycopg2 import Error,extras
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def con():
    connection=None
    try:
        connection = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="Abhi@2001",
    dbname="postgres",
    port=5432  
        )
    except Error as e:
        print(f"the error is '{e}")
    return connection



@app.route('/item/<int:id>',methods=["GET"])
def fun(id):
    connection= con()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('select * from login where id = %s',(id,))
    items = cursor.fetchone()
    cursor.close()
    connection.close()
    if items:
        return jsonify(dict(items))
    else:
        return jsonify({"error":"item not found"})
 
@app.route('/postitem',methods=["POST"])
def createitem():
    data = request.get_json()
    email=data.get('email')
    phone=data.get('phone')
    name=data.get('name')
    connection=con()
    cursor= connection.cursor()
    cursor.execute("insert into login (email,phone,name) values(%s,%s,%s)",(email,phone,name))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message":"item inserted to the database"})


@app.route('/home/<val>')
def myfun(val):
    x=int(val)
    y=x*x
    return "the value is %s" %y
@app.route('/one/<var>')
def myfun1(var):
    if var=='mrv':
        return redirect(url_for('myfun',name=var))
    else:
        return redirect(url_for('fun'))

if __name__=="__main__":
    app.run()
