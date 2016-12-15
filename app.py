import os, psycopg2

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():

	data = []

	conn = psycopg2.connect(

	database="da301k7aqru948", 
	user="oaskaojnytkyke", 
	password="e71735b255a8b198f17966271880fa5658a98e18a507d0ae776e38ed6c09ec3d", host="ec2-54-247-119-245.eu-west-1.compute.amazonaws.com",
	port="5432"

	)

	cur = conn.cursor()

	cur.execute("select * from movies limit 10")

	data = cur.fetchall()

	conn.close()



	return render_template('index.html', vals = data)

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	print "Server starting..."
	app.run(host='0.0.0.0', port=port, debug=True, threaded=True)