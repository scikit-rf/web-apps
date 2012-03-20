#!/usr/bin/python

import cgi, os
import cgitb; cgitb.enable()


form = cgi.FieldStorage()

# Get filename here.
fileitem = form['filename']

plot_dir = '../touchstone_plotter/plots/'
plot_fmts = ['pdf','png','eps']
touchstone_dir = '../touchstone_plotter/touchstones/'
# Test if the file was uploaded
if fileitem.filename:
    # strip leading path from file name to avoid 
    # directory traversal attacks
    fn = os.path.basename(fileitem.filename).replace('_','-')
    open(touchstone_dir + fn, 'wb').write(fileitem.file.read())
    
    
    # Get data from fields
    if form.getvalue('component'):
        component = form.getvalue('component')
    else:
        component = 's_db'
    
    latex_on = form.getvalue('latex_on')
    if form.getvalue('legend_on'):
        legend_off = False
    else: 
        legend_off = True
    
    if form.getvalue('grid_on') and component != 's_smith':
        show_grid = True
    else:
        show_grid = False
    
    title = form.getvalue('title')
    
    import ast
    plot_args = ast.literal_eval(form.getvalue('args'))
    plot_kwargs = ast.literal_eval(form.getvalue('kwargs'))
    
    
    
    
    import matplotlib
    import numpy
    matplotlib.use('Agg')
    import pylab
    import sys
    sys.path.append('/home/alex/code/scikit-rf/')
    import skrf as rf
    if latex_on:
        pylab.rcParams['text.usetex'] = True
    else:
        pylab.rcParams['text.usetex'] = False
    ntwk = rf.Network(touchstone_dir+ fn)
    if form.getvalue('f_unit') != 'auto':
        ntwk.frequency.unit = form.getvalue('f_unit')
    ntwk.__getattribute__('plot_%s'%component)(*plot_args,**plot_kwargs)
    if show_grid:
        pylab.grid(1)
    if legend_off:
        rf.legend_off()
    pylab.title(title)
    try:
        [pylab.savefig(plot_dir+fn[:-4]+'.'+fmt, format=fmt) for fmt in plot_fmts]
        message = '''
        <center>
            <img width=\'825\' src=\'%s\'></img>
            <br>
            <a href='%s'>png</a>
            <a href='%s'>pdf</a>
            <a href='%s'>eps</a>
        </center>'''\
        %(plot_dir+fn[:-4]+'.png',
            plot_dir+fn[:-4]+'.'+ 'pdf',
            plot_dir+fn[:-4]+'.'+ 'png',
            plot_dir+fn[:-4]+'.'+ 'eps',)
    except(RuntimeError):
        message = '''
        <center>
            <h2>Error saving figure, try turning off \'latex\' option.</h2>
        </center>'''
        
    
   
else:
    message = 'No file was uploaded'
   
print """\
Content-Type: text/html\n
<html>
<body>
   <p>%s</p>
</body>
</html>
""" % (message,)
