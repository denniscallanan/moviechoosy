import os, psycopg2

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, static_url_path='/static')


def tempcode(s):
	return s.decode('unicode_escape').encode('ascii','ignore')

@app.route('/')
def home():

	conn = psycopg2.connect(

	database="da301k7aqru948", 
	user="oaskaojnytkyke", 
	password="e71735b255a8b198f17966271880fa5658a98e18a507d0ae776e38ed6c09ec3d", host="ec2-54-247-119-245.eu-west-1.compute.amazonaws.com",
	port="5432"

	)

	cur = conn.cursor()

	# unicode id=7088

	cur.execute("select * from movies order by random() limit 1")

	data = cur.fetchone()

	conn.close()
	return render_template('index.html', title=tempcode(data[1]), info=tempcode(data[2]), backdrop=data[4], imdbrat=data[7], rtrat=data[9], cert=tempcode(data[10]), yt=data[11], runtime=data[12], year=data[6]);

if __name__ == '__main__':
	print "Server starting..."
	port = int(os.environ.get('PORT', 5000))
	app.run(host='127.0.0.1', port=port, debug=True, threaded=True)