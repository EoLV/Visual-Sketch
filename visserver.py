from flask import Flask, render_template, request, redirect, url_for, Blueprint
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from package.dbconsole.data import data
from package.webelements import table
from package.webelements import chart

dbengine = sqlalchemy.create_engine('mysql+pymysql://root:9999@localhost:3306/sketches')#, echo=True)
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
	if not attrid or int(attrid) > len(Data.attrid()):
		attrid = 1
	else:
		attrid = min(int(attrid), 10)
	chart1 = chart.trafficchart(Data, attrid)
	chart2 = chart.sidebarchart(Data, attrid)
	return render_template('show1.html', args=request.args.get('id'), chart1=chart1, chart2=chart2)

@app.route('/show/2')
def show2():
	attrid = request.args.get('id')
	if not attrid or int(attrid) > len(Data.attrid()):
		attrid = 1
	else:
		attrid = min(int(attrid), 10)
	chart1 = chart.distrchart(Data, attrid)
	chart2 = chart.sidebarchart(Data, attrid)
	return render_template('show2.html', args=request.args.get('id'), chart1=chart1, chart2=chart2)

@app.route('/show/3')
def show3():
	attrid = request.args.get('id')
	if not attrid or int(attrid) > len(Data.attrid()):
		attrid = 1
	else:
		attrid = min(int(attrid), 10)
	chart1 = chart.elephantchart(Data, attrid)
	chart2 = chart.sidebarchart(Data, attrid)
	return render_template('show3.html', args=request.args.get('id'), chart1=chart1, chart2=chart2)

@app.route('/show/4')
def show4():
	attrid = request.args.get('id')
	if not attrid or int(attrid) > len(Data.attrid()):
		attrid = 1
	else:
		attrid = min(int(attrid), 10)
	table1 = table.flowtable(Data, attrid)
	chart2 = chart.sidebarchart(Data, attrid)
	return render_template('show4.html', args=request.args.get('id'), table1=table1, chart2=chart2)

@app.route('/reflesh', methods=['GET', 'POST'])
def reflesh():
	Data.reflesh()
	url = request.args.get('url')
	return redirect(url)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
