#!/usr/bin/env python

# author: pharesim@nhzcrypto.org

import json
import urllib
import urllib2
import sqlite3
import sys
import math

# edit those
nhzhost     = 'http://127.0.0.1:7776'
database    = './pool.db' # best to use full path
poolstart   = 11371711 # timestamp in blockchain when your pool started
poolaccount = '123456789'
poolphrase  = "A-B_C\\D$E;F\"G'1.2;3/" # escape " and \ with \
payoutlimit = 100
feePercent  = 1
# done

conn = sqlite3.connect(database)
c = conn.cursor()

def main():
    startForging()
    getNew(json.loads(urllib2.urlopen(nhzhost+"/nhz?requestType=getAccountBlockIds&account="+poolaccount+"&timestamp="+getTimestamp()).read()))
    payout()
    return True


def startForging():
    payload = {
        'requestType': 'getForging',
        'secretPhrase': poolphrase
    }
    opener = urllib2.build_opener(urllib2.HTTPHandler())
    data = urllib.urlencode(payload)
    forging = json.loads(opener.open(nhzhost+'/nhz', data=data).read())
    if 'errorCode' in forging.keys():
        if forging['errorCode'] == 5:
            payload['requestType'] = 'startForging'
            data = urllib.urlencode(payload)
            forging = json.loads(opener.open(nhzhost+'/nhz', data=data).read())
            print "Started forging"

    return True


def getNew(newBlocks):
    shares = getShares()
    for block in newBlocks['blockIds']:
        blockData = json.loads(urllib2.urlopen(nhzhost+"/nhz?requestType=getBlock&block="+block).read())

        c.execute(
            "INSERT OR IGNORE INTO blocks (timestamp, block, totalfee) VALUES (?,?,?);",
            (blockData['timestamp'],block,blockData['totalFeeNQT'])
        )
        
        blockFee = float(blockData['totalFeeNQT'])
        if blockFee > 0:
            for (account, amount) in shares.items():
                if account is not poolaccount:
                    payout = math.floor(blockFee * (amount['percentage']/100))
                    c.execute(
                        "INSERT OR IGNORE INTO accounts (blocktime, account, percentage, amount, paid) VALUES (?,?,?,?,?);",
                        (blockData['timestamp'],account,amount['percentage'],payout,False)
                    )

    conn.commit()
    return True


def getTimestamp():
    timestamp = poolstart

    c.execute("SELECT timestamp FROM blocks ORDER BY timestamp DESC LIMIT 1;")
    blocks = c.fetchall()

    if len(blocks) > 0 and blocks[0][0] > poolstart:
        timestamp = blocks[0][0]

    return str(timestamp+1)


def getShares():  
    poolAccount  = json.loads(urllib2.urlopen(nhzhost+"/nhz?requestType=getAccount&account="+poolaccount).read())
    totalAmount  = float(poolAccount['guaranteedBalanceNQT'])
    leasedAmount = { poolaccount: { 'amount': totalAmount } }

    if 'lessors' in poolAccount:
        for lessor in poolAccount['lessors']:
            lessorAccount = json.loads(urllib2.urlopen(nhzhost+"/nhz?requestType=getAccount&account="+lessor).read())
            leasedAmount[lessor] = { 'amount': float(lessorAccount['guaranteedBalanceNQT']) }
            totalAmount += float(lessorAccount['guaranteedBalanceNQT'])

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
            fee     = ((amount*feePercent)/100)
            payment = str((amount-fee)-100000000)
            account = str(account)
            fee     = str(fee)
            print "Pay out "+payment+" to "+account+" (keep fee: "+fee+")"
            payload = {
                'requestType': 'sendMoney',
                'secretPhrase': poolphrase,
                'recipient': account,
                'amountNQT': payment,
                'feeNQT': 100000000,
                'deadline': 60
            }
            opener = urllib2.build_opener(urllib2.HTTPHandler())
            data = urllib.urlencode(payload)
            content = json.loads(opener.open(nhzhost+'/nhz', data=data).read())
            if 'transaction' in content.keys():
                c.execute("UPDATE accounts SET paid=? WHERE account=?;",(content['transaction'],str(account)))

    conn.commit()
    return True


def getLimit():
    return payoutlimit*100000000;


if __name__ == "__main__":
    main()
    sys.exit()
