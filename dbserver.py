import json
import traceback
import time

from flask import Flask, render_template, request, redirect, url_for, Blueprint

from package.dbconsole import dbdata

db = dbdata.DBData('mysql+pymysql://root:9999@localhost:3306/test2')
app = Flask(__name__)

@app.route('/post', methods=['GET', 'POST'])
def post():
	if request.method != 'POST':
		return 'access denied'
	print('posting!')
	print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	rawdata = request.get_data(as_text=True)
	# f = open('/cache/' + str(time.time()).replace('.', '_'), 'x')
	# f.write(rawdata)
	db.set_sys_info(1, request.environ['REMOTE_ADDR'], request.environ['REMOTE_PORT'], request.environ['HTTP_USER_AGENT'])

	try:
		rawdata = json.loads(rawdata)
	except:
		traceback.print_exc()
		return 'json syntax error'

	# print(rawdata)

	db.save_data(rawdata)
	print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	return 'data saved'

@app.route('/clean')
def clean():
	db.clean()
	return 'clean finished'

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5001, debug=True)
