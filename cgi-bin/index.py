#!/usr/bin/python
import cgi, cgitb, os, sys
from lxml import etree
import inflect

def search_name(bio_term_tree,bio_term):
	try:
		for thing in bio_term_tree.xpath("/obo/term/name"):
			if thing.text == bio_term:
				thing_parent = thing.getparent()

		child1 =  list(thing_parent)

		for element in child1:
			if element.tag == 'id' or element.tag == 'name' or element.tag == 'namespace':
				print element.tag + ':' + element.text +'<br>'

			elif element.tag == 'def':
				child2 = list(element)
				print element.tag + ':\"' + child2[0].text + '\"' ,
				print '[',
				for i in range(1,len(child2),1):
					print child2[i][1].text + ':' + child2[i][0].text + ',',
				print ']' +'<br>'


			elif element.tag == 'synonym':
				print element.tag + ':' + '\"' + element[0].text + '\"' + element.get('scope') +'[]' +'<br>'

			elif element.tag == 'is_a':
				for isa_id in bio_term_tree.xpath("/obo/term/id"):
					if element.text == isa_id.text:
						isa_id_parent = isa_id.getparent()
						print element.tag + ':' + element.text + ' ! ' + isa_id_parent[1].text +'<br>'
			

	except:
		return False

def search_synonyms(bio_term_tree,bio_term):
	try:
		for thing in bio_term_tree.xpath("/obo/term/synonym/synonym_text"):
			if thing.text == bio_term:
				thing_grandparent = thing.getparent().getparent()

		child1 =  list(thing_grandparent)

		for element in child1:
			if element.tag == 'id' or element.tag == 'name' or element.tag == 'namespace':
				print element.tag + ':' + element.text +'<br>'
			elif element.tag == 'def':
				child2 = list(element)
				print element.tag + ':\"' + child2[0].text + '\"' ,
				print '[',
				for i in range(1,len(child2),1):
					print child2[i][1].text + ':' + child2[i][0].text + ',',
				print ']' +'<br>'


			elif element.tag == 'synonym':
				print element.tag + ':' + '\"' + element[0].text + '\"' + element.get('scope') +'[]' +'<br>'


	except:
		return False

def display_all(bio_term_tree):
	for thing in bio_term_tree.xpath("/obo/term"):
		print thing[0].tag + ':' + thing[0].text + '\t' + thing[1].tag + ':' + thing[1].text +'<br>'


def article_search(bio_term_tree,bio_article):
	artilce_list = bio_article.split()
	p = inflect.engine()
	dealed_list =[]
	for word in artilce_list:
		if not word[0].isalpha():
			word = word[1:]
		if not word[-1].isalpha():
			word = word[:-1]	
		if p.singular_noun(word) :
			word = p.singular_noun(word)
		dealed_list.append(word)

	for element in dealed_list:
		search_name(bio_term_tree,element)
		search_synonyms(bio_term_tree,element)




tree = etree.parse('go_daily-termdb.xml')


cgitb.enable(); # formats errors in HTML

sys.stderr = sys.stdout
print "Content-type: text/html"
print
print """<html>
<head><title>Gene Ontology Search Engine</title></head>
<body>
<p>"""

form = cgi.FieldStorage()

if not form.has_key("value") and not form.has_key("display_submit"):
	print "<b>Error</b>: request did not provide the proper query string."

elif not form.has_key("value") and form.has_key("display_submit"):
	display_all(tree)

else:
	# This illustrates alternative ways of extracting field
	# parameters. The getfirst method is safer.
	v = str(form["value"].value)
	if form.has_key("search_submit"):

		search_name(tree,v)
	
	if form.has_key("display_submit"):
		display_all(tree)

	if form.has_key("article_submit"):
		article_search(tree,v)


print "</body></html>"
