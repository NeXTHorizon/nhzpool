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
def default(db):
    response.headers['Cache-Control'] = 'public, max-age=3600'
    poolaccount = config.get("pool", "poolaccount")
    poolfee = config.get("pool", "feePercent")
    db.text_factory = str
    d = db.execute("SELECT height, timestamp, totalfee FROM blocks WHERE totalfee > 0 ORDER BY timestamp DESC limit 6")
    getlastheight = d.fetchone()
    lastheight = getlastheight[0]
    c = db.execute("SELECT account, heightto, amount FROM leased WHERE heightto > %s" % (lastheight))
    result = c.fetchall() 
    block = d.fetchall()   
    output = template('default', pa=poolaccount, fee=poolfee, rows=result, blocks=block)
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
    c = db.execute("SELECT account, heightfrom, heightto, amount FROM leased")
    result = c.fetchall()   
    output = template('accounts', rows=result)
    return output

@route('/blocks')
def blocks(db):
    response.headers['Cache-Control'] = 'public, max-age=120'
    deadline = blocktime()
    dl = str(datetime.timedelta(seconds=deadline))
    c = db.execute("SELECT height, timestamp, block, totalfee FROM blocks WHERE totalfee > 0 ORDER BY timestamp DESC")
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
    c = db.execute("SELECT blocktime, account, percentage, amount FROM accounts WHERE paid=0 ORDER BY blocktime DESC")
    result = c.fetchall()   
    output = template('unpaid', rows=result)
    return output

@route('/paid')
def paid(db):
    response.headers['Cache-Control'] = 'public, max-age=1200'
    c = db.execute("SELECT blocktime, account, percentage, amount FROM accounts WHERE paid>0 ORDER BY blocktime DESC")
    result = c.fetchall()   
    output = template('paid', rows=result)
    return output
	    
run(server=PasteServer, port=8888, host='0.0.0.0')
