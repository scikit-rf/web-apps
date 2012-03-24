#!/usr/bin/python

import cgi, os
import cgitb; cgitb.enable()
import matplotlib
import numpy
matplotlib.use('Agg')
import pylab
import sys
sys.path.append('/home/alex/code/scikit-rf/')
import skrf as rf



form = cgi.FieldStorage()


measured_dir = '../calibration/measured/'
ideals_dir = '../calibration/ideals/'
duts_dir = '../calibration/duts/'
caled_dir = '../calibration/caled/'
output_dir = '../calibration/output/'
plot_dir = output_dir + 'plots/'
plot_fmts = ['png','pdf']

component_to_name ={
	's_db':'Magnitude',
	's_deg':'Phase',
	's_smith':'Smith Chart',
	}


n_stds = int(form.getvalue('stdCounter'))
n_duts = int(form.getvalue('dutCounter'))


measured =[]
ideals = []
duts = []
message = ''

for k in range(n_stds):
	if not(form['measure%i'%(k)].filename and form['ideal%i'%(k)].filename):
		message ='<script type="text/javascript">alert(\'enter more data\')</script>'

for k in range(n_stds):
	fileitem = form['measure%i'%(k)]
	fn = os.path.basename(fileitem.filename).replace('_','-')
	open(measured_dir + fn, 'wb').write(fileitem.file.read())
	measured.append(rf.Network(measured_dir + fn))
	fileitem = form['ideal%i'%(k)]
	fn = os.path.basename(fileitem.filename).replace('_','-')
	open(ideals_dir + fn, 'wb').write(fileitem.file.read())
	ideals.append(rf.Network(ideals_dir + fn))
for k in range(n_duts):
	fileitem = form['dut%i'%(k)]
	fn = os.path.basename(fileitem.filename).replace('_','-')
	open(duts_dir + fn, 'wb').write(fileitem.file.read())
	duts.append(rf.Network(duts_dir + fn))



cal = rf.Calibration(
	measured = measured, 
	ideals = ideals,
	)
	
caled = [cal.apply_cal(k) for k in duts]

message='''
<div>
<h2>
Touchstone Files
</h2>
</div>'''

for ntwk in caled:
	fn = ntwk.name+'.s'+str(ntwk.number_of_ports)+'p'
	message+='''
	<a href=\'%s\'>%s</a> <br>
	'''%(caled_dir+fn,fn)

message +='''
<div>
<h2>
Plots 
</h2>
</div>'''


for component in ['s_db', 's_deg','s_smith']:
	plot_name = component_to_name[component]
	message+='''
	<div>
	<h3>
	%s
	</h3>
	</div>'''%(plot_name)
	
	pylab.figure()
	pylab.title(plot_name)
	for ntwk in caled:
		ntwk.__getattribute__('plot_%s'%component)()
	
	 
	message += '''
			<div class = "unit">
			<img width=\'825\' src=\'%s\'></img><br>
			'''%(plot_dir+plot_name+'.png')
	
	for fmt in plot_fmts:
		fn = plot_dir+plot_name+'.'+fmt
		pylab.savefig(fn, format=fmt)
		message += '''<a href = \'%s\'>%s</a>
		'''%(fn,fmt)
	message+='''
		</div>
		<div text-align="center">
		'''
message += '''
</div>
'''

print '''\
Content-Type: text/html\n
<html>

<head>
<style>
	div.unit{
	text-align:center;
	padding: 10px;
	border: 0px solid black;	
	}
</style>
</head>
<body>
%s
</body>
</html>
''' % message

