'''Poll a directory for new files'''

import os
import time


class NewFiles:
    '''Keep track of new files, remove when successfully processed'''
    __new = []
    __run = False
    __folder_name = ''
    __poll_frequency = 1e12
    __previously_processed = []

    def stop(self):
        '''Get list of new files'''
        self.__run = False

    def get_new(self):
        '''Get list of new files'''
        return self.__new

    def get_folder_name(self):
        '''Get name of folder being watched'''
        return self.__folder_name

    def get_poll_frequence(self):
        '''Get the frequency of the polling'''
        return self.__poll_frequency

    def get_previously_processed(self):
        '''Get the frequency of the polling'''
        return self.__previously_processed

    def remove_new(self, filename):
        '''Remove a file with the matching filename'''
        return self.__new.remove(filename)

    def watch_folder(self, folder_name, poll_frequency, previously_processed):
        '''Persistent task for watching the target folder'''
        self.__run = True;
        self.__folder_name = folder_name;
        self.__poll_frequence = poll_frequency;
        self.__previously_processed = previously_processed;
        before = {f: None for f in previously_processed}
        while self.__run:
            time.sleep(poll_frequency)
            after = {f: None for f in os.listdir(folder_name)}
            self.__new = self.__new + [f for f in after if f not in before]
            print(self.__new)
            before = after

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
