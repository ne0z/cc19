#!/usr/bin/env python
from __future__ import print_function, division, absolute_import

import os
import yaml
from json import dumps as js


def _process_writeup_list(writeups, label):
    if type(writeups) != list:
        writeups = [writeups]
    writeup_html = ''
    for i, w in enumerate(writeups, 1):
        writeup_html += '<a href="{}">{}{}</a> '.format(w, label, (' '+str(i)) if i!=1 else '')
    return writeup_html


def _add_challenges(pathname, outfile):
    with open(pathname, 'r') as ymlfile:
        chall_metadata = yaml.safe_load(ymlfile)
    if type(chall_metadata) != list:
        chall_metadata = [chall_metadata]
    js_category = js(pathname.split(os.sep)[1])
    path = os.path.split(pathname)[0]
    n = 0
    for c in chall_metadata:
        name = js('<a href="{}">{}</a>'.format(path, c['name']))
        ctf = js(c.get('ctf', ''))
        author = js(c.get('author', ''))
        difficulty = js(c.get('difficulty', ''))
        tags = js(c.get('tags', ''))
        notes = js(c.get('notes', ''))
        original_writeup_html = _process_writeup_list(c['original_writeups'], 'Original')
        backup_writeups = c['backup_writeups']
        if type(backup_writeups) != list:
            backup_writeups = [backup_writeups]
        backup_writeup_html = _process_writeup_list([os.path.join(path, bw) for bw in backup_writeups], 'Backup')
        writeup_html = original_writeup_html + backup_writeup_html
        print("{{name: {}, ctf: {}, author: {}, category: {}, tags: {}, difficulty: {}, writeup: '{}', notes: {}}},".format(name, ctf, author, js_category, tags, difficulty, writeup_html, notes), file=outfile)
        n +=1
    return n


def main():
    with open('challenge-list.html', 'w') as f:
        print(
'''<html>
<head>
<link href="tabulator.min.css" rel="stylesheet">
<script type="text/javascript" src="tabulator.min.js"></script>
</head>
<body>
<h1>Training challenges for CyberChallenge.IT 2019</h1>
<p>
Each folder contains:
<ul>
            <li>a <i>description(s).txt</i> file that describe the challenge(s) and how to run them
            <li>a <i>chall-metadata.yml</i> with metadata that is used to automagically create the following list
</ul>
</p>
<div id="challenge-table"></div>
<script>
var tableData = [
''', file=f)
        n_challs = 0
        for root, dirs, files in os.walk('.', topdown=False):
            for name in files:
                if name == 'chall-metadata.yml':
                    n_challs += _add_challenges(os.path.join(root, name), f)
        print(
        '''
        ]
        var table = new Tabulator("#challenge-table", {
            data: tableData,
            layout: 'fitDataFill',
            selectable: false,
            columns: [
                {title: 'name', field:'name', formatter: 'html'},
                {title: 'ctf', field:'ctf'},
                {title: 'author', field:'author'},
                {title: 'category', field: 'category'},
                {title: 'tags', field: 'tags'},
                {title: 'difficulty', field: 'difficulty'},
                {title: 'writeup', field: 'writeup', formatter: 'html'},
                {title: 'notes', field: 'notes'},
            ],
        });''', file=f)
        print('</script><p>Total challenges: {}; note: you can sort the list by clicking on column names</body></html>'.format(n_challs), file=f)


if __name__ == '__main__':
    main()

