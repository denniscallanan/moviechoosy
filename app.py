import os, psycopg2, psycopg2.extensions, random, string

from flask import Flask, render_template, request, redirect, url_for, session

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

app = Flask(__name__, static_url_path='/static')

app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

sessionData = {}

class Predata:

	def __init__(self, data, v):

		self.data = data
		self.vote = v 


def knndiff(a,b):

	distance = 0

	for i in range(len(a)):

		#print i, a[i], b[i]

		diff = float(abs(a[i]-b[i]))

		if i == 0:
			diff = diff/400000000
		elif i==1 or i==2 or i==4:
			diff = diff/100
		elif i==3:
			diff = diff/100000
		elif i==5:
			diff = diff/300
		else:
			diff = diff/3

		#print i, diff

		distance+=diff

	return distance



def impList(m):

	return [m[i] for i in range(5,10)]+[m[j] for j in range(12,32)]

def randString():
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))


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

	best = 100

	# opening link first time

	if 'mid' not in request.form:

		print "first time opening link"

		session['id'] = randString()

		cur.execute("select * from movies order by random() limit 1")

		print "returning random movie"

		best = cur.fetchone()[0]

	# not opening link for first time

	else:

		lastmovie = request.form['mid']
		lastslideval = int(request.form['slideval'])

		print "first slide val ", lastslideval

		# clicking next for first time

		if session['id'] not in sessionData:

			print "first time clicking next"

			cur.execute("select * from movies where id=%s", (lastmovie,))

			mov = cur.fetchone()

			sessionData[session['id']] = Predata(impList(mov), lastslideval)

			print "returning random movie"

			cur.execute("select * from movies order by random() limit 1")

			best = cur.fetchone()[0]

		# not clicking next for first time
		
		else:

			print "not 1st time clicking next"


			if lastslideval > sessionData[session['id']].vote:

				cur.execute("select * from movies where id=%s", (lastmovie,))

				mov = cur.fetchone()

				sessionData[session['id']] = Predata(impList(mov), lastslideval)

			print sessionData[session['id']].data[1]

			print "vote ", sessionData[session['id']].vote

			if int(sessionData[session['id']].vote) <6:
				print 'pciking random'
				cur.execute("select * from movies order by random() limit 1")
				best = cur.fetchone()[0]

			else:

				smallest = 10000000

				cur.execute("select * from movies order by random() limit 100")

				for row in cur.fetchall():
					
					diff = knndiff(impList(row), sessionData[session['id']].data)
					if diff < smallest:

						print "new best diff = ", diff
						smallest = diff
						best = row[0]


	cur.execute("select * from movies where id=%s", (best,))

	data = cur.fetchone()

	conn.close()

	return render_template('index.html', mid=data[0], title=data[1], info=data[2], backdrop=data[4], imdbrat=data[7], rtrat=data[9], cert=data[10].encode("utf-8"), yt=data[11], runtime=data[12], year=data[6], imdb=data[32]);

if __name__ == '__main__':
	print "Server starting..."
	port = int(os.environ.get('PORT', 5000))
	app.run(host='127.0.0.1', port=port, debug=True, threaded=True)