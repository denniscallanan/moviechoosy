import os, psycopg2

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():

	data = []

	print "connecting to postgre database"

	conn = psycopg2.connect(

	database="da301k7aqru948", 
	user="oaskaojnytkyke", 
	password="e71735b255a8b198f17966271880fa5658a98e18a507d0ae776e38ed6c09ec3d", host="ec2-54-247-119-245.eu-west-1.compute.amazonaws.com",
	port="5432"

	)

	cur = conn.cursor()

	cur.execute("select * from movies order by id desc limit 5")

	data = cur.fetchall()

	conn.close()

	return '<br><br>'.join(map(str,data))

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	print "Server starting..."
	app.run(host='127.0.0.1', port=port, debug=True, threaded=True)