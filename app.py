import os, psycopg2, psycopg2.extensions

from flask import Flask, render_template, request, redirect, url_for

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

app = Flask(__name__, static_url_path='/static')


def tempcode(s):
	return s.decode('unicode_escape').encode('ascii','ignore')

@app.route('/', methods=['POST', 'GET'])
def home():

	conn = psycopg2.connect(

	database="da301k7aqru948", 
	user="oaskaojnytkyke", 
	password="e71735b255a8b198f17966271880fa5658a98e18a507d0ae776e38ed6c09ec3d", host="ec2-54-247-119-245.eu-west-1.compute.amazonaws.com",
	port="5432"

	)

	cur = conn.cursor()

	if 'mid' not in request.form:

		cur.execute("select * from movies order by random() limit 1")

	else:

		lastmovie = request.form['mid']
		lastslideval = request.form['slideval']
		cur.execute("select * from movies where id=%s", (lastmovie,))
		# return movie based on predicition

	data = cur.fetchone()

	conn.close()

	return render_template('index.html', mid=data[0], title=data[1], info=data[2], backdrop=data[4], imdbrat=data[7], rtrat=data[9], cert=data[10].encode("utf-8"), yt=data[11], runtime=data[12], year=data[6], imdb=data[32]);

if __name__ == '__main__':
	print "Server starting..."
	port = int(os.environ.get('PORT', 5000))
	app.run(host='127.0.0.1', port=port, debug=True, threaded=True)