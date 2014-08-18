nhzpool
=======

Forging pool for NHZ

Set up database:
cat db.txt | sqlite3 pool.db

Edit variables in config.ini

Dependencies:
pip install bottle bottle-sqlite paste

Start Pool Backend and Web Server:

./start.sh

Cron:
\* * * * * /path/to/payout.py >> /path/to/log
( Set time you want payouts to run at )

Goto:
http://localhost:8810/



