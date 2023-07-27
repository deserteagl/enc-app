'''from ctypes import *

s = CDLL('/root/PycharmProjects/FaiCrypto/Marca.so')
s.prep.argtype = c_void_p
s.prep(b'\x00'*32,b'\x00'*16,b'\x00'*8)

mydata = b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'

i = create_string_buffer(mydata,len(mydata))


e = create_string_buffer(len(mydata))
#s.encrypt_block(i)

#print(i.raw)
#s.decrypt_block(i)
s.MarcaCipher.argtypes = c_void_p ,c_void_p,c_size_t
s.MarcaCipher(i,e,c_size_t(len(mydata)))
print(e.raw)

from xml.dom.minidom import parse
parser = parse('./data/conf.xml')
dirs = parser.documentElement
for dir in dirs.getElementsByTagName("dir"):
    print(dir.getElementsByTagName('status')[0].childNodes[0].data)
    <Directory title="Secured">
   <dir name="/root/PycharmProjects/FaiCrypto/Secured">
      <path>/root/PycharmProjects/FaiCrypto/Secured</path>
      <currentName>/root/PycharmProjects/FaiCrypto/Secured</currentName>
      <status>open</status>
   </dir>
</Directory>
'''
'''
from xml.etree import ElementTree
tree = ElementTree.ElementTree()
root = ElementTree.Element('Directory')
root.attrib={'title':'Secured'}
subelement = ElementTree.Element('dir')
item = ElementTree.Element('path')
item.text = '/root'
item1 = ElementTree.Element("currentname")
item2 = ElementTree.Element("status")
item1.text = "/root"
item2.text = "open"
subelement.append(item1)
subelement.append(item2)
subelement.append(item)
root.append(subelement)
tree._setroot(root)
tree.write("./data/conf.xml")
'''
import xml.etree.ElementTree as elt
tree = elt.parse('./data/conf.xml')
root = tree.getroot()
for i in root:
   # for n in i:
    #if i.tag == '/root':
    i[2].text = 'hidden'
#tree = elt.ElementTree()
#tree._setroot(root)
tree.write('./data/conf.xml')