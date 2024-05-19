from flask import Flask, request,jsonify, render_template
import  json
import sqlite3

app = Flask(__name__)

#an in memory users storage(using a list)
#users = []
#instead of a list,we need to create a connection to database where we store users
def db_connection():
	conn = None
	try:
		conn = sqlite3.connect('users.sqlite')
	except sqlite3.error as e:
		print(e)
	return conn

@app.route("/users" , methods=["GET","POST"])
def users():
	#access the db connection
	conn = db_connection()
	#access the cursor object
	cursor = conn.cursor()

#createing our GET request for all users
	if request.method == "GET":
		cursor = conn.execute("SELECT * FROM users")
		users = [
		  dict(id = row[0], firstname = row[1], lastname = row[2], gender = row[3] , age = row[4])
		  for row in cursor.fetchall()
		]

		if users is not None:
			return jsonify(users)
#createing our POST request for a user
	if request.method == "POST":
		firstname = request.form["firstname"]
		lastname = request.form["lastname"]
		gender = request.form["gender"]
		age  = request.form["age"]
		#SQL  query to INSERT a user INTO our database
		sql = """INSERT INTO users (firstname, lastname, gender, age)
				 VALUES (?, ?, ?, ?) """

		cursor = cursor.execute(sql, (firstname, lastname, gender, age))
		conn.commit()
		return f"User with id: {cursor.lastrowid} created successfully"

#a route with all the neccesary request methods for a single user	
@app.route('/user/<int:id>',methods=[ "GET", "PUT", "DELETE" ])
def user(id):
	conn = db_connection()
	cursor = conn.cursor()
	user = None

#createing our GET request for a user
	if request.method == "GET":
		cursor.execute("SELECT * FROM users WHERE id=?",(id,) )
		rows = cursor.fetchall()
		for row in rows:
			user = row
		if user is not None:
			return jsonify(user), 200
		else:
			return "Something went wrong", 404

#createing our PUT request for a user
	if request.method == "PUT":
		sql = """ UPDATE users SET firstname = ?,lastname = ?, gender = ? , age = ?
				  WHERE id = ? """

		firstname = request.form["firstname"]
		lastname = request.form["lastname"]
		gender = request.form["gender"]
		age = request.form["age"]

		updated_user = {
			"id": id,
			"firstname": firstname,
			"lastname" : lastname,
			"gender" : gender,
			"age" : age
		}

		conn.execute(sql,(firstname, lastname, gender, age, id))
		conn.commit()
		return jsonify(updated_user)

#createing our DELETE request for a user
	if request.method == "DELETE":
		sql= """ DELETE FROM users WHERE id=? """
		conn.execute(sql, (id,))
		conn.commit()

		return "The User with id: {} has been deleted.".format(id),200

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8000, debug=False)
