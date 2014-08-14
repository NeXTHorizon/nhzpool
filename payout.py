import json
import urllib
import urllib2
import sqlite3
import ConfigParser
import sys

config = ConfigParser.RawConfigParser()
config.read('config.ini')

conn = sqlite3.connect(config.get("pool", "database"))
c = conn.cursor()

def main():
    payout()
    return True
 
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
            fee     = ((amount*float(config.get("pool", "feePercent")))/100)
            payment = str((amount-fee)-100000000)
            account = str(account)
            fee     = str(fee)
            print "Pay out "+payment+" to "+account+" (keep fee: "+fee+")"
            c.execute("INSERT INTO payouts (account, fee, payment) VALUES (?,?,?);",(account, fee, payment))
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

    conn.commit()
    return True


def getLimit():
    return float(config.get("pool", "payoutlimit"))*100000000;

if __name__ == "__main__":
    main()
    sys.exit()