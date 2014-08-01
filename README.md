nhzpool
=======

Forging pool for NHZ

Set up database:
cat db.txt | sqlite3 pool.db

Edit variables in pool.py

Cron:
#* * * * * /path/to/pool.py >> /path/to/log
