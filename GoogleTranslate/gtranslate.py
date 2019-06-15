### Github Page
### https://github.com/mahirozdin/GTranslate-strings-xml
### Running by Mahir Özdin forked on Ra-Na/GTranslate-strings-xml

### Settings 

# -*- coding: utf-8 -*-

import html
import requests
import os
import xml.etree.ElementTree as ET
from io import BytesIO
 
print("Enter the original file language code en etc.")
INPUTLANGUAGE = input()
 
print("Enter the output language code tr etc.")
OUTPUTLANGUAGE  = input()

words = OUTPUTLANGUAGE.split(",")
for current_word in words:
	path = "values-"+current_word;
	INFILE = "strings.xml"
	OUTFILE = path+"/strings.xml"
	
	
	try:  
		os.mkdir(path)
	except OSError:  
		print ("Creation of the directory %s failed" % path)
	else:  
		print ("Successfully created the directory %s " % path)
	
	def translate(to_translate, to_language="auto", language="auto"):
	 r = requests.get("http://translate.google.com/m?hl=%s&sl=%s&q=%s"% (to_language, language, to_translate.replace(" ", "+")))
	 beforecharset='charset='
	 aftercharset='" http-equiv'
	 parsed1=r.text[r.text.find(beforecharset)+len(beforecharset):]

	



	 text=html.unescape(r.text)    
	 before_trans = 'class="t0">'
	 after_trans='</div><form'
	 parsed1=r.text[r.text.find(before_trans)+len(before_trans):]
	 parsed2=parsed1[:parsed1.find(after_trans)]
	 print(parsed2) 
	 return html.unescape(parsed2).replace("'", r"\'")
 

	tree = ET.parse(INFILE)
	root = tree.getroot()
	for i in range(len(root)):
		isTranslatable=root[i].get('translatable')
		print((str(i)+" ========================="))
		if(isTranslatable=='false'):
			print("Not translatable")
		if(root[i].tag=='string') & (isTranslatable!='false'):
			totranslate=root[i].text
			print(totranslate)
			print("-->")
			if(totranslate!=None):
				print(current_word)
				root[i].text=translate(totranslate,current_word,INPUTLANGUAGE)
				print(root[i].text)
		if(root[i].tag=='string-array'):
			print("Entering string array...")
			for j in range(len(root[i])):
				isTranslatable=root[i][j].get('translatable')
				print((str(i)+" "+str(j)+" ========================="))
				if(isTranslatable=='false'):
					print("Not translatable")
				if(root[i][j].tag=='item') & (isTranslatable!='false'):
				
					print(totranslate)
					if(totranslate!=None):
						root[i][j].text=translate(totranslate,current_word,INPUTLANGUAGE)
						print(root[i][j].text)
     
	tree.write(OUTFILE, encoding='utf-8')

