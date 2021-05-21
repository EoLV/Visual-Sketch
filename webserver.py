from flask import Flask, render_template, request, redirect, url_for, Blueprint
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

import json
import numpy as np

from package.dbconsole.data import data
from package.webelements import table
from package.webelements import chart

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

dbengine = sqlalchemy.create_engine('mysql+pymysql://root:9999@localhost:3306/sketchestest')#, echo=True)
DBSession = scoped_session(sessionmaker(bind=dbengine))
Data = data(DBSession)

app = Flask(__name__)

@app.route('/')
def index():
	return redirect('/show/1')

@app.route('/show/<id>')
def show(id):
	return '404 Not Found.' + id

@app.route('/show/1')
def show1():
	attrid = request.args.get('id')
	if not attrid or int(attrid) not in Data.attrid():
		attrid = sorted(Data.attrid().keys())[-1]
	else:
		attrid = int(attrid)
	chart2 = chart.sidebarchart(Data, attrid)
	return render_template('show1.html', pageid=1, dataid=attrid, chart2=chart2)

@app.route('/show/2')
def show2():
	attrid = request.args.get('id')
	if not attrid or int(attrid) not in Data.attrid():
		attrid = sorted(Data.attrid().keys())[-1]
	else:
		attrid = int(attrid)
	chart2 = chart.sidebarchart(Data, attrid)
	return render_template('show2.html', pageid=2, dataid=attrid, chart2=chart2)

@app.route('/show/3')
def show3():
	attrid = request.args.get('id')
	if not attrid or int(attrid) not in Data.attrid():
		attrid = sorted(Data.attrid().keys())[-1]
	else:
		attrid = int(attrid)
	chart2 = chart.sidebarchart(Data, attrid)
	return render_template('show3.html', pageid=3, dataid=attrid, chart2=chart2)

@app.route('/show/4')
def show4():
	attrid = request.args.get('id')
	if not attrid or int(attrid) not in Data.attrid():
		attrid = sorted(Data.attrid().keys())[-1]
	else:
		attrid = int(attrid)
	table1 = table.flowtable(Data, attrid)
	chart2 = chart.sidebarchart(Data, attrid)
	return render_template('show4.html', pageid=4, dataid=attrid, table1=table1, chart2=chart2)

@app.route('/getdata', methods=['GET', 'POST'])
def getdata():
	pageid = int(request.args.get('pageid'))
	dataid = request.args.get('id')
	if not dataid or int(dataid) not in Data.attrid():
		dataid = sorted(Data.attrid().keys())[-1]
	else:
		dataid = int(dataid)
	data = {}
	if pageid == 1:
		data = chart.trafficchart(Data, dataid)
	elif pageid == 2:
		data = chart.distrchart(Data, dataid)
	elif pageid == 3:
		data = chart.elephantchart(Data, dataid)
	elif pageid == 4:
		data = table.flowtable(Data, dataid)
	elif pageid == 5:
		data = chart.sidebarchart(Data, dataid)
	# data['dataid'] = dataid
	return json.dumps(data, cls=CustomEncoder)


@app.route('/reflesh', methods=['GET', 'POST'])
def reflesh():
	Data.reflesh()
	url = request.args.get('url')
	return redirect(url)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
