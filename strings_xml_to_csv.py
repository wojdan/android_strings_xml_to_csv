# Copyright 2016 Bartłomiej Wojdan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from itertools import izip
from bs4 import BeautifulSoup as BS, Comment, Tag
import csv

xml = 'strings.xml'

def get_fieldnames(filename):
    soup = BS(open(filename), 'html.parser')
    resources = soup.resources
    s = set()
    for desc in resources.descendants:
        if isinstance(desc, Tag):
            s.update(desc.attrs.keys())
    fieldnames = ['value','translation','comment']
    fieldnames[len(fieldnames):] = list(s)
    return fieldnames

def parse(filename):
    soup = BS(open(filename), 'html.parser')
    resources = soup.resources
    def get_strings():
        item = {}
        for c in resources.children:
            try:
                if isinstance(c, Comment):
                    item['comment'] = c.strip()
                if isinstance(c, Tag):
                    item.update(c.attrs)
                    arr_name = c.attrs['name']
                    if c.name == 'string':
                        item['value'] = c.string
                        yield item
                    elif c.name == 'string-array':
                        for i, arr_item in enumerate(c.find_all('item')):   
                            item['name'] = '[{}]{}'.format(i, arr_name)
                            try:
                                item['value'] = arr_item.string.encode('utf-8')
                                yield item
                            except Exception as inst:
                                print item['value']
                                print inst
                    item = {}        
            except Exception as inst:
                print inst.args

    return get_strings()

f = open('outputs/android_strings.csv', 'w+')
try:
    writer = csv.DictWriter(f, fieldnames=get_fieldnames(xml))
    writer.writeheader()
    for i in parse(xml):
        writer.writerow(i)
finally:
    f.close()
