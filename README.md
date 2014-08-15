nhzpool
=======

Forging pool for NHZ

Set up database:
cat db.txt | sqlite3 pool.db

Edit variables in config.ini

Pool backend:

screen -d -m -S nhzpool ./pool.py

Cron:
\* * * * * /path/to/payout.py >> /path/to/log
( Set time you want payouts to run at )

Webserver:

Dependencies:
pip install bottle bottle-sqlite paste

Run:
screen -d -m -S poolserver ./webserver.py

Goto:
http://localhost:8888/



