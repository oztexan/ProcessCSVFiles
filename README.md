# Django File Processor

This application processes CSV files that are dropped periodically into the local directory "file_bucket" in the root level of this project.

It fulfills the following requirements:
- New file reports are dropped into a local folder at regular times in the day

- Multiple types of reports may be dropped into this folder

- Each file should be processed, and a status recorded to the database to say they have arrived

- For specific report types, the contents of the file should also be imported into the database and the status updated to imported

- You are free to add any additional status values as appropriate

- The modification time of the file represents the download date/time, this should be recorded to the database

- Each report type has a specific filename pattern, this includes the report type but also additional information relating to that file. There will always be a trade date encoded in the filename.

- Different report types may have different filename patterns

- Each report type has a different set of columns, all columns should be imported (though only TradeActivityReports are processed)

- Each report may be revised during the day, the prior report should be considered out of date and replaced with this one.

## Approach Used to Process Files

The logic for processing the watch folder is in views.py and poll.py where the heavy app logic resides.

THe directory being monitored and the polling frequency are set in views.py
```
WATCH_FOLDER = os.path.abspath(os.path.dirname(__name__)) + '/file_bucket'
POLL_FREQUENCY = 3
```
The polling frequency is currently set to 3 seconds for rapid testing purposes.  This can be changed to 10*60 if 10 minute testing is desired.

A server side thread is launched in views.py when the frontend calls into the startThreadTask handler on the url endpoint /startThread.  

This thread runs a simple while loop with a call to sleep(POLL_FREQUENCY).  When it wakes it reviews the files in the directory with respect to the files that have already been processed in the DB.  

1. The list of new files is calculated
2. This list is iterated
3. Replacement files candidates are identified
4. A candidate entry for the ProcessedFiles tables is produced with a status of ‘Arrived’ and modification time = now
5. If the file is of type TradeActivityReport, the contents of the file are further processed
  - The file column names must match the db_colname set on the TradeActivityReport object, else the file is failed.
  - Validation on each row occurs. Each row must have the same number of columns as the header row.  If any row fails, the entire file fails
  - If all goes well, the file is saved as "processed", and trades are saved to the database
  - If any failures occur the file is recorded in the database as failing with a reason (error), no trades are saved.
6. If file processing succeeds, any files identified to be replaced are tagged as "deprecated"


The frontend polls the backend endpoint '/checkThread' at a 1000ms intervals. The endpoint returns the current processed files and trades for display.


## Database
The database includes two tables
- ProcessedFiles
- TradeActivityReport

There is a 1-M relationship between ProcessedFiles and the TradeActivityReport

ProcessedFiles are recorded with the following information to accomodate all known report types:
- filename
- status (enum [Arrived, Processed, Deprecated, Failed: Reason])
- report_type
- account (can be null)
- trade_date
- generation_date

TradeActivityReport captures all trades, tagged with their source file.

## File Matching
Any files that do not match one of the following patterns will be stored in the ProcessedFiles table with a report_type = "Unknown"
```
'TradeActivityReport': r'TradeActivityReport-LIFETRADING-(\d+)-(\d+).csv',
'PositionReport': r'PositionReport-(\d+)-LIFETRADING-(\d+)-(\d+).csv',
'CollateralReport': r'CollateralReport-LIFETRADING-(\d+)-(\d+).csv'
```

Files with a filename that match the TradeActivityReport pattern are further processed into rows in the TradeActivityReport. The status on these files be "Processed".

- Extra Credit: if a file arrives that has a matching name of a file already processed, it will replace the matching files data.  This was a little ambiguous, does the file come in with exactly the same name?  My assumption is files always come in with a different name, replacement file names match everything except the generation_date?  

Files that are present in the directory at startup will be processed as new. They are processed in file alphanumeric order.  If there are any replacement files in the directory at startup the filename with the lowest alphanumeric order will replace all others.

## Approach
- poll.py, long run server side process to monitor a folder for new files.  Implemented using threads, maybe overkill and not robust but was an interesting exercise.  I didn't just want to poll client side

- reporttypes.py, defines the file patterns and parsing rules for the 3 different file types to be recognised

## Installation Requirements

 - Python3
 - Django2.1
 - sqlite3

## Setup

 ```
 git clone git@github.com:oztexan/ProcessCSVFiles.git
 cd ProcessCSVFiles
 python3 -m venv env
 source env/bin/activate
 pip3 install -r requirements.txt
 python3 manage.py migrate
 python3 manage.py runserver
 ```

## Run
 In a browser visit `http://localhost:8000`.

 The UI is very basic.  Two buttons
 - "Start/Stop Watching"
 - "Toggle View"

 Click "Start Watching" to begin processing files in the "file_bucket" subdirectory.

 Add new files to the file_bucket to watch behaviour.

 Click "Toggle View" to switch between processed files and processed trades.

 Note: Trades associated with deprecated files are filtered out


## Assumptions & Limitations
 - Files assumed to always be added, never removed from the watch folder.  If so, restart the server
 ```
 rm db.sqlite3
 python3 manage.py migrate
 python3 manage.py runserver
 ```

 Always reload the UI after this process


 - The front end site is single instance only, multiple browser sessions may cause unexpected behaviour

 - For demo purposes, the server polls every 3 seconds, this can be set in the views.py

 - The client UI calles the server /checkThread endpoint, currently set at a 1 sec interval.  THis can be changed in the template index.html

## Unit Testing
Run unit tests (a few written in the tests.py file)
```
python manage.py test
```

## Manual Incoming File Scenario Tests (example files in fixtures directory)
Copy some example files stored in process_files/fixtures into file_bucket
Reinitialise the app
```
rm db.sqlite3
python3 manage.py migrate
python3 manage.py runserver
```
- Process all files that are in the file_bucket folder
- If two files already exist in the watch folder and one file replaces the other, ensure one is deprecated, other Processed e.g. fixtures
 - CollateralReport-LIFETRADING-20181004-0711836
 - CollateralReport-LIFETRADING-20181004-07118360
- Unknown file pattern should just store as "Arrived" with Unknown report_type e.g.
 - rubbish.csv
- TradeActivityReport files with empty rows are processed, empty rows ignored
 - TradeActivityReport-LIFETRADING-20181005-666666
- If there is a mismatch in column header and any row count, file processing should fail, trades should not be stored and a failed status recorded in database
 - TradeActivityReport-LIFETRADING-20181005-666667
- Failed files must not replace previously successful files, eg 666667 below will not replace trades processed from 666666
 - TradeActivityReport-LIFETRADING-20181005-666666
 - TradeActivityReport-LIFETRADING-20181005-666667
