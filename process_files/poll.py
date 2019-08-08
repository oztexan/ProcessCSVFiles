'''Poll a directory for new files and process'''
import os
import time
import csv

from process_files.models import ProcessedFiles, TradeActivityReport
from .reporttypes import process_filename
import process_files


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

    def get_folder_name(self):
        '''Get name of folder being watched'''
        return self.__folder_name

    def get_poll_frequency(self):
        '''Get the frequency of the polling'''
        return self.__poll_frequency

    def get_previously_processed(self):
        '''Get the frequency of the polling'''
        return self.__previously_processed

    def remove_new(self, filename):
        '''Remove a file with the matching filename'''
        return self.__new.remove(filename)

    def process_new_files(self):
        # Need to sort this by generation_time?
        after = {f: None for f in os.listdir(self.__folder_name)}
        self.__before = []
        for pf in ProcessedFiles.objects.all():
            self.__before.append(pf.filename)
        self.__new = [f for f in after if f not in self.__before]
        # before = after
        print("NEW = ",self.__new)
        for filename in self.__new:
            # Put DB transaction stuff here
            try:
                details = process_filename(filename)
                deprecate = []
                # Revised reports that deprecate previous will match all but generation_time?
                # We don't know about unknowns so can't recognise revised
                print('details',details)
                if(details['report_type'] != 'Unknown'):
                    deprecate = ProcessedFiles.objects.filter(
                        report_type=details['report_type'],
                        trade_date=details['trade_date'],
                        account=details['account'])

                print('deprecate',deprecate)
                details['status'] = 'A'
                source_file = ProcessedFiles.objects.create(**details)

                print('FILE',self.__folder_name)

                if source_file.report_type == 'TradeActivityReport':
                    with open(self.__folder_name+'/'+filename) as csv_file:
                        for line in csv.reader(
                                csv_file, skipinitialspace=True):
                            print('LINE =',line)
                            values = [source_file] + line
                            cols = [i.name for i in TradeActivityReport._meta.get_fields()
                                    if i.name != 'id']
                            # This mapping probably not always this clean?
                            if len(cols) != len(values):
                                raise Exception('Mismatch in tradereport CSV col count and DB col count.  File %s ignored.' % filename)
                            fields = dict(zip(cols, [source_file] + line))
                            tar = TradeActivityReport.objects.create(
                                **fields)
                            tar.save()

                    source_file.status = 'P'

                for d in deprecate:
                    d.status = "D"
                    d.save()

                source_file.save()
                self.__before.append(filename)
                self.__new.remove(filename)

            except Exception as inst:
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
