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

def lastblock(db):
    
    lastblock = d.fetchone()
    print lastblock
    blockData = json.loads(urllib2.urlopen(config.get("pool", "nhzhost")+"/nhz?requestType=getBlock&block=", data=lastblock).read())
    payload = {
        'requestType': 'getBlock',
        'block': lastblock
    }
    opener = urllib2.build_opener(urllib2.HTTPHandler())
    data = urllib.urlencode(payload)
    api = json.loads(opener.open(config.get("pool", "nhzhost")+'/nhz', data=data).read())
    getheight = api["height"]
    return getheight
    
@route('/')
def default():
    response.headers['Cache-Control'] = 'public, max-age=172800'
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
def accounts(db):
    response.headers['Cache-Control'] = 'public, max-age=3600'
    db.text_factory = str
    d = db.execute("SELECT height FROM blocks ORDER BY timestamp DESC")
    getlastheight = d.fetchone()
    lastheight = getlastheight[0]
    print lastheight
    c = db.execute("SELECT account, heightfrom, heightto, amount FROM leased WHERE heightto > %s" % (lastheight))
    result = c.fetchall()   
    output = template('accounts', rows=result)
    return output

@route('/blocks')
def blocks(db):
    response.headers['Cache-Control'] = 'public, max-age=120'
    deadline = blocktime()
    dl = str(datetime.timedelta(seconds=deadline))
    c = db.execute("SELECT timestamp, block, totalfee FROM blocks WHERE totalfee > 0")
    result = c.fetchall()
    c.close()   
    output = template('blocks', rows=result, fg=dl)
    return output

@route('/payouts')
def payouts(db):
    response.headers['Cache-Control'] = 'public, max-age=86400'
    c = db.execute("SELECT account, fee, payment FROM payouts")
    result = c.fetchall()   
    output = template('payouts', rows=result)
    return output

@route('/unpaid')
def unpaid(db):
    response.headers['Cache-Control'] = 'public, max-age=1200'
    c = db.execute("SELECT blocktime, account, percentage, amount FROM accounts WHERE paid=0")
    result = c.fetchall()   
    output = template('transactions', rows=result)
    return output
	
run(server=PasteServer, port=8888, host='0.0.0.0')
