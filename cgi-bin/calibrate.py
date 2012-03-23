#!/usr/bin/python

import cgi, os
import cgitb; cgitb.enable()


form = cgi.FieldStorage()


measurd_dir = 'measured'
ideals_dir = 'ideals'

n_stds = int(form.getvalue('output'))

message = ''
for k in range(n_stds):
	if not(form['measure%i'%(k)].filename and form['ideal%i'%(k)].filename):
		message ='<script type="text/javascript">alert(\'enter more data\')</script>'

for k in range(n_stds):
fn = os.path.basename(fileitem.filename).replace('_','-')
    open(touchstone_dir + fn, 'wb').write(fileitem.file.read())
print """\
Content-Type: text/html\n
<html>
<body>
   <p>%s</p>
</body>
</html>
""" % message

