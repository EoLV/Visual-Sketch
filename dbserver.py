import json
import traceback
import time
from flask import Flask, render_template, request, redirect, url_for, Blueprint
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from package.dbconsole import models, sessions

dbengine = sqlalchemy.create_engine('mysql+pymysql://root:9999@localhost:3306/sketchestest') #, echo=True)
DBSession = scoped_session(sessionmaker(bind=dbengine))
Base = declarative_base()
Attribute = models.make_attribute(Base)

app = Flask(__name__)

def save_elastic(data):
	try:
		Heavypart = models.make_heavypart(Base, data['ID'])
		Distribution = models.make_distribution(Base, data['ID'])
		Base.metadata.create_all(bind=dbengine)
	except:
		traceback.print_exc()
		return 'create failed'
	ret = sessions.save_elastic_session(DBSession(), data, Attribute, Heavypart, Distribution)
	return ret

@app.route('/post', methods=['GET', 'POST'])
def post():
	if request.method != 'POST':
		return 'access denied'
	print('posting!')
	print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	rawdata = request.get_data(as_text=True)
	f = open(str(time.time()).replace('.', '_'), 'x')
	f.write(rawdata)
	try:
		data = json.loads(rawdata)
	except:
		traceback.print_exc()
		return 'json syntax error'
	# f = open(data['Time'].replace(':', '_'), 'x')
	# f.write(rawdata)

	if data['Algorithm'] == 'elastic':
		return save_elastic(data);
	return 'unknown algorithm'

@app.route('/clean')
def clean():
	global Base
	global Attribute
	Base.metadata.drop_all(bind=dbengine)
	Base = declarative_base()
	Attribute = models.make_attribute(Base)
	return 'clean finished'

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5001, debug=True)
