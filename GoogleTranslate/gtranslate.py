### Github Page
### https://github.com/mahirozdin/GTranslate-strings-xml
### Running by Mahir Özdin forked on Ra-Na/GTranslate-strings-xml

### Settings 



import html
import requests
import os
import xml.etree.ElementTree as ET
from io import BytesIO
 
print("Enter the original file language code en etc.")
INPUTLANGUAGE = input()
 
print("Enter the output language code tr etc.")
OUTPUTLANGUAGE  = input()

print ("Enter the in filename strings.xml etc.")
INFILE = input()
print("Enter the out filename strings_new_translated.xml etc.")
OUTFILE = input()

def translate(to_translate, to_language="auto", language="auto"):
 r = requests.get("http://translate.google.com/m?hl=%s&sl=%s&q=%s"% (to_language, language, to_translate.replace(" ", "+")))
 beforecharset='charset='
 aftercharset='" http-equiv'
 parsed1=r.text[r.text.find(beforecharset)+len(beforecharset):]
 parsed2=parsed1[:parsed1.find(aftercharset)]

 
 if(parsed2!=r.encoding):
     print('\x1b[1;31;40m' + 'Warning: Potential Charset conflict' )
     print(" Encoding as extracted by SELF    : "+parsed2)
     print(" Encoding as detected by REQUESTS : "+r.encoding+ '\x1b[0m')


 if(r.encoding=='windows-874' and os.name=='posix'):
     print('\x1b[1;31;40m' + "Alert: Working around age old Python bug (https://bugs.python.org/issue854511)\nOn Linux, charset windows-874 must be labeled as charset cp874"+'\x1b[0m')
     r.encoding='cp874'


 text=html.unescape(r.text)    
 before_trans = 'class="t0">'
 after_trans='</div><form'
 parsed1=r.text[r.text.find(before_trans)+len(before_trans):]
 parsed2=parsed1[:parsed1.find(after_trans)]
 print(parsed2) 
 return html.unescape(parsed2)
 

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
            root[i].text=translate(totranslate,OUTPUTLANGUAGE,INPUTLANGUAGE)
            print(root[i].text)
    if(root[i].tag=='string-array'):
        print("Entering string array...")
        for j in range(len(root[i])):
            isTranslatable=root[i][j].get('translatable')
            print((str(i)+" "+str(j)+" ========================="))
            if(isTranslatable=='false'):
                print("Not translatable")
            if(root[i][j].tag=='item') & (isTranslatable!='false'):
                totranslate=root[i][j].text
                print(totranslate)
                if(totranslate!=None):
                    root[i][j].text=translate(totranslate,OUTPUTLANGUAGE,INPUTLANGUAGE)
                    print(root[i][j].text)
     
tree.write(OUTFILE, encoding='utf-8')

