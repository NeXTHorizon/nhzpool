nhzpool
=======

Forging pool for NHZ

Prerequisites
-------------

* Python 2.7.x
* Python-pip
* SQLite 3.x
* virtualenvwrapper (for creation of a virtual Python environment for the pool)

Installation
------------

First we need to create the virtual environment that will contain the required packages.

```
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv nhzpool
```

Now to install the required packages.
```
pip install -r requirements.txt
```

Now set up the database:
```
cat db.txt | sqlite3 pool.db
```

Copy config.ini.example to config.ini and edit the settings
```
cp config.ini.example config.ini
```

nhzhost: The host and port at which to find the NHZ API server

database: The full path to the pool.db file

poolaccount: The numeric account ID for the pool

poolaccountrs: The alphanumeric account ID for the pool

poolphrase: The password for the pool's account. This is needed to send payouts. Keep the setup very secure.

payoutlimit: The minimum amount to pay out

feePercent: The percentage of forged NHZ you wish to charge users

Now you can start Pool Backend and Web Server:

```
./start.sh
```

Go to:
http://youripaddress:8810/

