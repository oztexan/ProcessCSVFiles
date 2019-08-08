'''Poll a directory for new files and process'''
import os
import time
import csv
import datetime

from process_files.models import ProcessedFiles, TradeActivityReport
from .reporttypes import process_filename

# This is overkill but I wanted to work with Python classes


class NewFiles:
    '''Keep track of new files, remove when successfully processed'''
    __new = []
    __run = False
    __folder_name = ''
    __poll_frequency = 1e12
    __before = []

    def stop(self):
        '''Get list of new files'''
        self.__run = False

    def get_new(self):
        '''Get list of new files'''
        return self.__new

    def get_processed_files(self):
        '''Get list of processed files'''
        str_list = []
        for pf in ProcessedFiles.objects.all():
            str_list.append(str(pf))
        return str_list

    def get_active_trades(self):
        '''Get list of active (non deprecated) trades'''
        str_list = []
        for tr in TradeActivityReport.objects.filter(
                source_file__status='Processed'):
            str_list.append(str(tr))
        return str_list

    def get_folder_name(self):
        '''Get name of folder being watched'''
        return self.__folder_name

    def get_poll_frequency(self):
        '''Get the frequency of the polling'''
        return self.__poll_frequency

    def remove_new(self, filename):
        '''Remove a file with the matching filename'''
        return self.__new.remove(filename)

    def process_trade_activity_file(self,filename,source_file):
        with open(self.__folder_name + '/' + filename) as csv_file:
            headers = None
            lookup = {}
            trades = []
            for line in csv.reader(
                    csv_file, skipinitialspace=True):
                # Allow blank rows
                if headers and len(line) > 0:
                    print('Line = ', line)
                    # This mapping probably not always clean?
                    # More time, ensure column name match
                    if len(lookup) != len(line):
                        raise Exception(
                            'Mismatch count in header and file row.  File %s ignored.' % filename)
                    tar_dict = {}
                    i = 0
                    for v in line:
                        tar_dict[lookup[headers[i]]] = v
                        i += 1
                    tar = TradeActivityReport(**tar_dict)
                    trades.append(tar)
                elif len(line) > 0:
                    headers = line
                    # FIXME Don't do this here everytime
                    for i in TradeActivityReport._meta.get_fields():
                        if i.db_column is not None:
                            lookup[i.db_column] = i.name
                    for h in headers:
                        if not lookup[h]:
                            raise Exception('Unrecognised column name %s' % h)

        source_file.status = 'Processed'
        source_file.save()

        for t in trades:
            t.source_file = source_file
            print(t)
            t.save()

    def process_new_files(self):
        after = {f: None for f in os.listdir(self.__folder_name)}
        self.__before = []
        for pf in ProcessedFiles.objects.all():
            self.__before.append(pf.filename)

        # Assume filenames are reliably alphanumerically sequenced
        # If first run on the folder includes revisions, we want to ensure
        # we process in order
        self.__new = sorted([f for f in after if f not in self.__before])
        remove = []
        for filename in self.__new:
            # Put DB transaction stuff here
            print('FILE=', filename)
            try:
                details = process_filename(filename)
                replace_candidates = []
                # Revised reports that deprecate previous will match all but generation_time?
                # We don't know about unknowns so can't recognise revised
                # versions
                if(details['report_type'] != 'Unknown'):
                    deprecate = ProcessedFiles.objects.filter(
                        report_type=details['report_type'],
                        trade_date=details['trade_date'],
                        account=details['account'])
                    # Django IDIOM, queries are lazy, force DB query now
                    for d in deprecate:
                        replace_candidates.append(d)

                details['status'] = 'Arrived'
                details['modification_time'] = datetime.datetime.now()
                source_file = ProcessedFiles(**details)

                if source_file.report_type == 'TradeActivityReport':
                    self.process_trade_activity_file(filename, source_file)
                else:
                    source_file.save()

                for rc in replace_candidates:
                    print("Replace", rc)
                    rc.status = "Deprecated"
                    rc.save()

            except Exception as inst:
                source_file.status = 'Failed: '+str(inst)
                source_file.save()
                print(inst)

    def watch_folder(self, folder_name, poll_frequency):
        '''Persistent task for watching the target folder'''
        self.__run = True
        self.__folder_name = folder_name
        self.__poll_frequence = poll_frequency
        while self.__run:
            time.sleep(poll_frequency)
            self.process_new_files()


# Alternative approach to testing, run the file directly
if __name__ == "__main__":
    # Setup to run in a directory that has a 'file_bucket' subdirectory
    # Touch a file 'fixture1'
    # Run
    # File 'fixture1' is ignored
    # Subsequent touched files are reported
    PF = NewFiles()
    PF.watch_folder(
        'file_bucket',
        1,
        ['TradeActivityReport-LIFETRADING-20181004-0500561.csv'])
else:
    print("Importing poll.py")
