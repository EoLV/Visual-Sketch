from flask import Flask, render_template, request, redirect, url_for, Blueprint
import json
import numpy as np

from package.webelements import pgdata_local
from package.webelements.pgsysinfo import pgsysinfo
from package.webelements.pgtraffic import pgtraffic
from package.webelements.pgdistri import pgdistri
from package.webelements.pgelephant import pgelephant
from package.webelements.pgflows import pgflows
from package.webelements.chsidebar import chsidebar
from package.webelements.chflowhis import chflowhis

class CustomEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, np.integer):
			return int(obj)
		elif isinstance(obj, np.floating):
			return float(obj)
		elif isinstance(obj, np.ndarray):
			return obj.tolist()
		else:
			return super(CustomEncoder, self).default(obj)

pgdata = pgdata_local.PGData('mysql+pymysql://root:9999@localhost:3306/test2')

app = Flask(__name__)

@app.route('/')
def index():
	dataid = request.args.get('id')
	chart = chsidebar(pgdata, dataid)
	return render_template('index.html', pageid=0, sidedata=chart)

@app.route('/show/1')
def show1():
	dataid = request.args.get('id')
	chart = chsidebar(pgdata, dataid)
	return render_template('show1.html', pageid=1, sidedata=chart)

@app.route('/show/2')
def show2():
	dataid = request.args.get('id')
	chart = chsidebar(pgdata, dataid)
	return render_template('show2.html', pageid=2, sidedata=chart)

@app.route('/show/3')
def show3():
	dataid = request.args.get('id')
	chart = chsidebar(pgdata, dataid)
	return render_template('show3.html', pageid=3, sidedata=chart)

@app.route('/show/4')
def show4():
	dataid = request.args.get('id')
	chart = chsidebar(pgdata, dataid)
	return render_template('show4.html', pageid=4, sidedata=chart)

@app.route('/getflowhistory', methods=['GET', 'POST'])
def getflowhistory():
	flowid = int(request.args.get('flowid'))
	result = chflowhis(pgdata, flowid)
	return json.dumps(result, cls=CustomEncoder)


@app.route('/getdata', methods=['GET', 'POST'])
def getdata():
	pageid = int(request.args.get('pageid'))
	dataid = request.args.get('dataid')
	result = []
	if pageid == 0:
		result = pgsysinfo(pgdata, dataid)
	if pageid == 1:
		result = pgtraffic(pgdata, dataid)
	if pageid == 2:
		result = pgdistri(pgdata, dataid)
	if pageid == 3:
		result = pgelephant(pgdata, dataid)
	if pageid == 4:
		result = pgflows(pgdata, dataid)
	return json.dumps(result, cls=CustomEncoder)

@app.route('/reflesh', methods=['GET', 'POST'])
def reflesh():
	pgdata.reflesh()
	url = request.args.get('url')
	return redirect(url)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
