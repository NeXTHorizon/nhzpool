#!/usr/bin/env python

# author: brendan@shellshockcomputer.com.au

import ConfigParser
from bottle import route, install, run, template, static_file, PasteServer
from bottle_sqlite import SQLitePlugin
import json
import urllib
import urllib2
import datetime

config = ConfigParser.RawConfigParser()
config.read('config.ini')

install(SQLitePlugin(dbfile=(config.get("pool", "database"))))

@route('/')
def default():
    output = template('default')
    return output

@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')

@route('/favicon.ico')
def get_favicon():
    return static('favicon.ico')

@route('/accounts')
def accounts():
    poolAccount = json.loads(urllib2.urlopen(config.get("pool", "nhzhost")+"/nhz?requestType=getAccount&account="+config.get("pool", "poolaccount")).read())
    clean = poolAccount["lessors"] 
    output = template('accounts', leased=clean)
    return output

@route('/blocks')
def blocks(db):
    c = db.execute("SELECT timestamp, block, totalfee FROM blocks WHERE totalfee > 0")
    result = c.fetchall()
    c.close()
    payload = {
        'requestType': 'getForging',
        'secretPhrase': config.get("pool", "poolphrase")
    }
    opener = urllib2.build_opener(urllib2.HTTPHandler())
    data = urllib.urlencode(payload)
    forging = json.loads(opener.open(config.get("pool", "nhzhost")+'/nhz', data=data).read())
    getdl = forging["deadline"]
    deadline = str(datetime.timedelta(seconds=getdl))   
    output = template('blocks', rows=result, fg=deadline)
    return output

@route('/payouts')
def payouts(db):
    c = db.execute("SELECT account, percentage, amount, paid, blocktime FROM accounts")
    result = c.fetchall()   
    output = template('payouts', rows=result)
    return output

run(server=PasteServer, port=8888, host='0.0.0.0')
