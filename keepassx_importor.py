#!/usr/bin/env python
#coding: utf-8

'''
把yaml格式的条目追加到keepassX导出的XML文件中
yaml格式:
-
 title: t_name_1
 username: u_name_1
 password: pw_1
 comment: c_1
-
 title: t_name_2
 username: u_name_2
 password: pw_2
 comment: c_2


@author: jessinio@gmail.com
'''
import os
from optparse import OptionParser
import time
import traceback
import sys
from lxml import etree
import yaml

def get_option():
    parser = OptionParser()
    parser.add_option("-n", "--new", dest="new_data",
                      help="new entry file", metavar="/path/to/file")
    parser.add_option("-a", "--append", dest="append_to",
                      help="append entry to xml")
    parser.add_option("-g", "--group", dest="group_name",
                      help="group name")


    (options, args) = parser.parse_args()

    if not (options.new_data and options.append_to and options.group_name):
        parser.print_help()
        sys.exit(1)
    return options


class Txt2XML:
    def __init__(self, new_data, append_to, group_name, create_time=None):
        self.new_data = new_data
        self.append_to = append_to
        self.group_name = group_name
        self.create_time = create_time
        self.entry_template = '''<entry>
   <title>%s</title>
   <username>%s</username>
   <password>%s</password>
   <url></url>
   <comment>%s</comment>
   <icon>1</icon>
   <creation>%s</creation>
   <lastaccess>%s</lastaccess>
   <lastmod>%s</lastmod>
   <expire>Never</expire>
  </entry>'''

        self.keepassXML = None
        self.group_tag = None
    
    def _get_group_tag(self):
        # 
        for title_tag in self.keepassXML.xpath('/database/group/title'):
            if title_tag.text == self.group_name:
                self.group_tag = title_tag.getparent()
                break
        else:
            #raise Exception, "Error: can't find %s group" % self.group_name
            print >>sys.stderr, "Error: can't find '%s' group" % self.group_name
            sys.exit(1)
        
    def _load_xml(self):
        try:
            self.keepassXML = etree.parse(self.append_to)
        except Exception, e:
            #TODO:
            traceback.print_exc()
            sys.exit(1)

    def _load_txt(self):
        return yaml.load(open(self.new_data).read())
    
    def _append_entry_to_parent(self, child_node):
        self.group_tag.append(child_node)

    def save_to(self):
        self._load_xml()
        self._get_group_tag()
        t = time.strftime("%Y-%m-%dT%H:%M:%S")
        for title_name, user_name, password, comment in self._load_txt():
            child_node = self.entry_template % (title_name, user_name, password, comment, t, t, t)
            child_node = etree.XML(child_node)
            self._append_entry_to_parent(child_node)
        self.keepassXML.write(self.append_to, encoding="utf-8")

if __name__ == "__main__":
    options = get_option()
    Txt2XML(options.new_data, options.append_to, options.group_name).save_to()
