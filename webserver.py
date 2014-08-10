#!/usr/bin/env python

# author: brendan@shellshockcomputer.com.au

import sqlite3
import ConfigParser
from bottle import route, run, template, static_file, PasteServer, debug
import json
import urllib
import urllib2
from pool import getShares


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
    poolAccount = json.loads(urllib2.urlopen(config.get("pool", "nhzhost")+"/nhz?requestType=getAccount&account="+config.get("pool", "poolaccount")).read())
    clean = poolAccount["lessors"] 
    output = template('accounts', leased=clean)
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
    deadline = forging["deadline"]   
    output = template('blocks', rows=result, fg=deadline)
    return output

@route('/payouts')
def payouts():
    conn = sqlite3.connect(config.get("pool", "database"))
    c = conn.cursor()
    c.execute("SELECT account, percentage, amount, paid, blocktime FROM accounts")
    result = c.fetchall()
    c.close()   
    output = template('payouts', rows=result)
    return output

   
debug(True)
run(server=PasteServer, port=8888, host='0.0.0.0')