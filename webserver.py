#!/usr/bin/env python

# author: brendan@shellshockcomputer.com.au

import sqlite3
import ConfigParser
from bottle import route, run, template, static_file, PasteServer, debug
import json
import urllib
import urllib2


config = ConfigParser.RawConfigParser()
config.read('config.ini')

@route('/')
def default():
    output = template('default')
    return output

@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')

@route('/accounts')
def accounts():
    conn = sqlite3.connect(config.get("pool", "database"))
    c = conn.cursor()
    c.execute("SELECT account, percentage, amount, paid, blocktime FROM accounts")
    result = c.fetchall()
    c.close()   
    output = template('accounts', rows=result)
    return output

@route('/blocks')
def blocks():
    conn = sqlite3.connect(config.get("pool", "database"))
    c = conn.cursor()
    c.execute("SELECT timestamp, block, totalfee FROM blocks")
    result = c.fetchall()
    c.close()
    payload = {
        'requestType': 'getForging',
        'secretPhrase': config.get("pool", "poolphrase")
    }
    opener = urllib2.build_opener(urllib2.HTTPHandler())
    data = urllib.urlencode(payload)
    forging = json.loads(opener.open(config.get("pool", "nhzhost")+'/nhz', data=data).read())   
    output = template('blocks', rows=result, fg=forging)
    return output

   
debug(True)
run(server=PasteServer, port=8888, host='0.0.0.0')