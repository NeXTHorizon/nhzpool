#!/usr/bin/env python

# author: pharesim@nhzcrypto.org

import json
import urllib
import urllib2
import sqlite3
import math
import ConfigParser
import time

config = ConfigParser.RawConfigParser()
config.read('config.ini')

conn = sqlite3.connect(config.get("pool", "database"))
c = conn.cursor()


def main():
    while True:
        startForging()
        getleased()
        getNew(json.loads(urllib2.urlopen(config.get("pool", "nhzhost")+"/nhz?requestType=getAccountBlockIds&account="+config.get("pool", "poolaccount")+"&timestamp="+getTimestamp()).read()))
        time.sleep(100)
        payout()
        time.sleep(100)
        
        
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
        rs = lessorAccount['accountRS']
        c.execute("INSERT OR REPLACE INTO leased (account, heightfrom, heightto, amount, ars) VALUES (?,?,?,?,?);",(accountadd, heightfrom, heightto, balance, rs))
    
    conn.commit()
    return True                    
    
        
def getNew(newBlocks):
    shares = getShares()
    if 'blockIds' in newBlocks:
        for block in newBlocks['blockIds']:
            blockData = json.loads(urllib2.urlopen(config.get("pool", "nhzhost2")+"/nhz?requestType=getBlock&block="+block).read())
            if 'errorCode' in blockData.keys():
                if blockData['errorCode'] == 5:
                    time.sleep(120)
                    return True
                else:
                    c.execute("INSERT OR IGNORE INTO blocks (timestamp, block, totalfee, height) VALUES (?,?,?,?);", (blockData['timestamp'],block,blockData['totalFeeNQT'],blockData['height']))
                
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

def payout():
    c.execute("SELECT account, amount FROM accounts WHERE paid=0 AND amount>0;")
    unpaid = c.fetchall()
    c.execute("SELECT * FROM blocks WHERE totalfee>0;")
    blocks = c.fetchall()

    pending = {}
    for share in unpaid:
        if share[0] in pending:
            pending[share[0]] += share[1]
        else:
            pending[share[0]] = share[1]

    for (account, amount) in pending.items():
        if amount > getLimit():
            time.sleep(100)
            fee     = int(math.floor(((amount*float(config.get("pool", "feePercent")))/100)))
            payment = str((amount-fee)-100000000)
            account = str(account)
            fee     = str(fee)
            print "Pay out "+payment+" to "+account+" (keep fee: "+fee+")"
            payload = {
                'requestType': 'sendMoney',
                'secretPhrase': config.get("pool", "poolphrase"),
                'recipient': account,
                'amountNQT': payment,
                'feeNQT': 100000000,
                'deadline': 60
            }
            opener = urllib2.build_opener(urllib2.HTTPHandler())
            data = urllib.urlencode(payload)
            content = json.loads(opener.open(config.get("pool", "nhzhost")+'/nhz', data=data).read())
            if 'transaction' in content.keys():
                c.execute("UPDATE accounts SET paid=? WHERE account=?;",(content['transaction'],str(account)))
                c.execute("INSERT INTO payouts (account, fee, payment) VALUES (?,?,?);",(account, fee, payment))

    conn.commit()
    return True


def getLimit():
    return float(config.get("pool", "payoutlimit"))*100000000;

if __name__ == "__main__":
    main()
