import sqlite3
import sys
import ConfigParser


config = ConfigParser.RawConfigParser()
config.read('config.ini')

conn = sqlite3.connect(config.get("pool", "database"))
c = conn.cursor()


def main():
    transaction = "10642581256253220471"
    account = "12357392056317066768"
    fee =
    payment =

    c.execute("UPDATE accounts SET paid=? WHERE account=?;",(str(transaction),str(account)))
#    c.execute("INSERT INTO payouts (account, fee, payment) VALUES (?,?,?);",(account, fee, payment)


if __name__ == "__main__":
    main()
    sys.exit()