#!/usr/bin/python
import cgi, cgitb, os, sys
cgitb.enable(); # formats errors in HTML

sys.stderr = sys.stdout
print "Content-type: text/html"
print
print """<html>
<head><title>Gene Ontology Search Engine</title></head>
<body>
<p>"""

form = cgi.FieldStorage()

if not form.has_key("value") :
    print "<b>Error</b>: request did not provide the proper query string."
else:
    # This illustrates alternative ways of extracting field
    # parameters. The getfirst method is safer.
    v = str(form["value"].value)

    print "Get : ", v
print "</body></html>"
