# Django File Processor

This Django application processes incoming CSV files and records the file arrivals and mock trade position data into a database.

The database includes two tables
- ProcessedFiles
- TradeActivityReport

There is a 1-M relationship between ProcessedFiles and the TradeActivityReport

ProcessedFiles are recorded with the following information:
- filename
- status (enum [A for Arrived, P for Processed, D for Deprecated])
- report_type
- account (can be null)
- trade_date
- generation_date

Any files that do not match one of the following patterns will include only a filename & status
```
'TradeActivityReport': r'TradeActivityReport-LIFETRADING-(\d+)-(\d+).csv',
'PositionReport': r'PositionReport-(\d+)-LIFETRADING-(\d+)-(\d+).csv',
'CollateralReport': r'CollateralReport-LIFETRADING-(\d+)-(\d+).csv'
```

Files with a filename that match the pattern TradeActivityReport pattern are further processed into rows in the TradeActivityReport. The status on these files will typically be "P".

- Enhancement: if a file arrives that has a matching name of a file already processed, it will replace the matching files data.

Files that are present in the directory at startup are ignored as historical.
  - Enhancement to load this from the database table

## Utility Modules
- poll.py, long run server side process to monitor a folder for new files.  Implemented using threads, maybe overkill and not robust but was an interesting exercise.  I didn't just want to poll client side
- reporttypes.py, defines the file patterns and parsing rules for 3 different file types to be recognised
-

## Requirements

 - Python3
 - Django2.1
 - sqlite3

## Setup

 ```
 git clone TBD
 cd django-file-processor
 python3 -m venv env
 source env/bin/activate
 pip3 install -r requirements.txt
 python3 manage.py migrate
 python3 manage.py runserver
 ```
 In browser go to `http://localhost:8000`.

## Assumptions & Limitations
 - Files assumed to always be added, never removed from the watch folder.  If so, restart the server.
 - The front end site is single instance only, multiple browser sessions will cause failures
 - For demo purposes, server polls every 10 seconds, this can be set in the View (views.py)
 - The client polls, checks for updates independently of the server

## Testing
Testing is handled in two seperate ways.

The usual way, run unit tests that are defined in the tests file
```
python manage.py test
```

The Poll module which is a long run task can be tested by directly running the module:
```
python process_files/poll.py
```
Setup to run in a directory that has a 'file_bucket' subdirectory
- Touch a file 'fixture1'
- Run
- File 'fixture1' is ignored assuming it is old
- Subsequent touched files are reported
