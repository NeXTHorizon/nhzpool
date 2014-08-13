#!/usr/bin/env python

# author: brendan@shellshockcomputer.com.au

import ConfigParser
from bottle import route, install, run, template, static_file, response, PasteServer
from bottle_sqlite import SQLitePlugin
import json
import urllib
import urllib2
import datetime

config = ConfigParser.RawConfigParser()
config.read('config.ini')

install(SQLitePlugin(dbfile=(config.get("pool", "database"))))

def blocktime():
    payload = {
        'requestType': 'getForging',
        'secretPhrase': config.get("pool", "poolphrase")
    }
    opener = urllib2.build_opener(urllib2.HTTPHandler())
    data = urllib.urlencode(payload)
    forging = json.loads(opener.open(config.get("pool", "nhzhost")+'/nhz', data=data).read())
    getdl = forging["deadline"]
    return getdl
    
@route('/')
def default():
    response.headers['Cache-Control'] = 'public, max-age=600'
    output = template('default')
    return output

@route('/static/:path#.+#', name='static')
def static(path):
    response.headers['Cache-Control'] = 'public, max-age=2592000'
    return static_file(path, root='static')

@route('/favicon.ico')
def get_favicon():
    response.headers['Cache-Control'] = 'public, max-age=2592000'
    return static('favicon.ico')

@route('/accounts')
def accounts():
    response.headers['Cache-Control'] = 'public, max-age=86400'
    poolAccount = json.loads(urllib2.urlopen(config.get("pool", "nhzhost")+"/nhz?requestType=getAccount&account="+config.get("pool", "poolaccount")).read())
    clean = poolAccount["lessors"] 
    output = template('accounts', leased=clean)
    return output

@route('/blocks')
def blocks(db):
    deadline = blocktime()
    response.headers['Cache-Control'] = "public, max-age=%d" % deadline
    dl = str(datetime.timedelta(seconds=deadline))
    c = db.execute("SELECT timestamp, block, totalfee FROM blocks WHERE totalfee > 0")
    result = c.fetchall()
    c.close()   
    output = template('blocks', rows=result, fg=dl)
    return output

@route('/payouts')
def payouts(db):
    response.headers['Cache-Control'] = 'public, max-age=7200'
    c = db.execute("SELECT account, percentage, amount, paid, blocktime FROM accounts")
    result = c.fetchall()   
    output = template('payouts', rows=result)
    return output

run(server=PasteServer, port=8888, host='0.0.0.0')
