#!/usr/bin/env python

# author: pharesim@nhzcrypto.org

import json
import urllib
import urllib2
import sqlite3
import sys
import math
import ConfigParser
import time

config = ConfigParser.RawConfigParser()
config.read('config.ini')

conn = sqlite3.connect(config.get("pool", "database"))
c = conn.cursor()


def main():
    while True:
        #startForging()
        #getleased()
        getNew(json.loads(urllib2.urlopen(config.get("pool", "nhzhost")+"/nhz?requestType=getAccountBlockIds&account="+config.get("pool", "poolaccount")+"&timestamp="+getTimestamp()).read()))
        #time.sleep(100)
        print "done"
        sys.exit()
        
def startForging():
    payload = {
        'requestType': 'getForging',
        'secretPhrase': config.get("pool", "poolphrase")
    }
    opener = urllib2.build_opener(urllib2.HTTPHandler())
    data = urllib.urlencode(payload)
    forging = json.loads(opener.open(config.get("pool", "nhzhost")+'/nhz', data=data).read())
    if 'errorCode' in forging.keys():
        if forging['errorCode'] == 5:
            payload['requestType'] = 'startForging'
            data = urllib.urlencode(payload)
            forging = json.loads(opener.open(config.get("pool", "nhzhost")+'/nhz', data=data).read())
            print "Started forging"

    return True

def getleased():
    leasedaccounts = json.loads(urllib2.urlopen(config.get("pool", "nhzhost")+"/nhz?requestType=getAccount&account="+config.get("pool", "poolaccount")).read())
    for lessor in leasedaccounts['lessors']:
        lessorAccount = json.loads(urllib2.urlopen(config.get("pool", "nhzhost")+"/nhz?requestType=getAccount&account="+lessor).read())
        balance = lessorAccount['guaranteedBalanceNQT']
        accountadd = lessorAccount['account']
        heightfrom = lessorAccount['currentLeasingHeightFrom']
        heightto = lessorAccount['currentLeasingHeightTo']
        c.execute("INSERT OR REPLACE INTO leased (account, heightfrom, heightto, amount) VALUES (?,?,?,?);",(accountadd, heightfrom, heightto, balance))
    
    conn.commit()
    return True                    
    
        
def getNew(newBlocks):
    shares = getShares()
    if 'blockIds' in newBlocks:
        for block in newBlocks['blockIds']:
            blockData = json.loads(urllib2.urlopen(config.get("pool", "nhzhost")+"/nhz?requestType=getBlock&block="+block).read())

            c.execute(
                "INSERT OR IGNORE INTO blocks (timestamp, block, totalfee, height) VALUES (?,?,?,?);",
                (blockData['timestamp'],block,blockData['totalFeeNQT'],blockData['height'])
            )
            
            blockFee = float(blockData['totalFeeNQT'])
            blockheight = float(blockData['height'])
            if blockFee > 0:
                for (account, amount) in shares.items():
                    if account is not config.get("pool", "poolaccount"):
                        lessorAccount = json.loads(urllib2.urlopen(config.get("pool", "nhzhost")+"/nhz?requestType=getAccount&account="+account).read())
                        heightfrom = lessorAccount['currentLeasingHeightFrom']
                        if heightfrom < blockheight:                                           
                            payout = math.floor(blockFee * (amount['percentage']/100))                     
                            
                            c.execute(
                                    "INSERT OR IGNORE INTO accounts (blocktime, account, percentage, amount, paid) VALUES (?,?,?,?,?);",
                            (blockData['timestamp'],account,amount['percentage'],payout,False)
                        )

    conn.commit()
    return True


def getTimestamp():
    timestamp = config.get("pool", "poolstart")

    c.execute("SELECT timestamp FROM blocks ORDER BY timestamp DESC LIMIT 1;")
    blocks = c.fetchall()

    if len(blocks) > 0 and blocks[0][0] > config.get("pool", "poolstart"):
        timestamp = blocks[0][0]

    return str(int(timestamp)+1)


def getShares():
    poolAccount = json.loads(urllib2.urlopen(config.get("pool", "nhzhost")+"/nhz?requestType=getAccount&account="+config.get("pool", "poolaccount")).read())
    totalAmount = 0
    if 'guaranteedBalanceNQT' in poolAccount:
        totalAmount  = float(poolAccount['guaranteedBalanceNQT'])

    leasedAmount = { config.get("pool", "poolaccount"): { 'amount': totalAmount } }

    if 'lessors' in poolAccount:
        for lessor in poolAccount['lessors']:
            lessorAccount = json.loads(urllib2.urlopen(config.get("pool", "nhzhost")+"/nhz?requestType=getAccount&account="+lessor).read())
            leasedAmount[lessor] = { 'amount': float(lessorAccount['guaranteedBalanceNQT']) }
            totalAmount += float(lessorAccount['guaranteedBalanceNQT'])

    if totalAmount > 0:
        for (account, amount) in leasedAmount.items():
            leasedAmount[account]['percentage'] = amount['amount'] / (totalAmount/100)

    return leasedAmount

if __name__ == "__main__":
    main()
