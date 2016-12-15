import os

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	print "Server starting..."
	app.run(host='0.0.0.0', port=port, debug=True, threaded=True)