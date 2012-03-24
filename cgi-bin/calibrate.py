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
output_dir = '../calibration/output/'
plot_fmts = ['pdf','png','eps']


n_stds = int(form.getvalue('stdCounter'))
measured =[]
ideals = []
message = ''
for k in range(n_stds):
	if not(form['measure%i'%(k)].filename and form['ideal%i'%(k)].filename):
		message ='<script type="text/javascript">alert(\'enter more data\')</script>'

for k in range(n_stds):
	fileitem = form['measure%i'%(k)]
	fn = os.path.basename(fileitem.filename).replace('_','-')
	open(measured_dir + fn, 'wb').write(fileitem.file.read())
	measured.append(rf.Network(measured_dir + fn, 'wb'))
	fileitem = form['ideal%i'%(k)]
	fn = os.path.basename(fileitem.filename).replace('_','-')
	open(ideals_dir + fn, 'wb').write(fileitem.file.read())
	ideals.append(rf.Network(ideals_dir + fn, 'wb'))



cal = rf.Calibration(
	measured = measured, 
	ideals = ideals,
	)
cal.error_ntwk.write_touchstone( 'ErrorNetwork',dir = output_dir)
cal.plot_coefs_db()
pylab.title('Error Coefficients')
[pylab.savefig(output_dir+'Error Coefficients'+'.'+fmt, format=fmt) for fmt in plot_fmts]

message = """
<center>
<a href = '%s'>Error Network</a>
<img width=\'825\' src=\'%s\'></img>
<br>
<a href='%s'>png</a>
<a href='%s'>pdf</a>
<a href='%s'>eps</a>
</center>"""\
%(output_dir+'ErrorNetwork.s2p',
output_dir+'Error Coefficients'+'.png',
output_dir+'Error Coefficients'+'.'+ 'pdf',
output_dir+'Error Coefficients'+'.'+ 'png',
output_dir+'Error Coefficients'+'.'+ 'eps',)

print """\
Content-Type: text/html\n
<html>
<body>
   <p>%s</p>
</body>
</html>
""" % message

