from django.test import TestCase
from process_files.models import ProcessedFiles, TradeActivityReport
from .reporttypes import process_filename
import csv
import process_files
import os
# from .poll import *

# class PollTestCase(TestCase):
#     def setUp(self):
#


class ReportTypesTestCase(TestCase):
    # def setUp(self):

    def test_report_types(self):
        filename = 'TradeActivityReport-LIFETRADING-20181004-0500561.csv'
        details = process_filename(filename)
        self.assertEqual(details['report_type'], 'TradeActivityReport')
        self.assertEqual(details['trade_date'], '20181004')
        self.assertEqual(details['generation_time'], '0500561')

        filename = 'SomethingUnknown-LIFETRADING--20181004-0500561.csv'
        details = process_filename(filename)
        self.assertEqual(details['report_type'], 'Unknown')
        self.assertEqual(details['trade_date'], '')
        self.assertEqual(details['generation_time'], '')


class ProcessedFilesTestCase(TestCase):
    def setUp(self):
        tar = {
            'filename': 'TradeActivityReport-LIFETRADING-20181004-0500561.csv',
            'status': 'Arrived',
            'report_type': 'TradeActivityReport',
            'account': '',
            'trade_date': '20181004',
            'generation_time': '0500561',
        }
        pr = {
            'filename': 'PositionReport-20181004-LIFETRADING-18345-0615929.csv',
            'status': 'Arrived',
            'report_type': 'PositionReport',
            'account': '1835',
            'trade_date': '20181004',
            'generation_time': '0615929',
        }
        cr = {'filename': 'CollateralReport-LIFETRADING-20181004-0711836.csv',
              'status': 'Arrived',
              'report_type': 'CollateralReport',
              'account': '',
              'trade_date': '20181004',
              'generation_time': '0711836',
              }
        ProcessedFiles.objects.create(**tar)
        ProcessedFiles.objects.create(**pr)
        ProcessedFiles.objects.create(**cr)

    def test_processed_files(self):
        print(ProcessedFiles.objects.all())
        """Processed Files are correctly identified"""
        tar = ProcessedFiles.objects.get(report_type="PositionReport")
        self.assertEqual(tar.account, '1835')
        cr = ProcessedFiles.objects.get(report_type="CollateralReport")
        self.assertEqual(cr.generation_time, '0711836')
        pr = ProcessedFiles.objects.get(report_type="TradeActivityReport")
        self.assertEqual(pr.trade_date, '20181004')


class TradeActivityReportTestCase(TestCase):
    def setUp(self):
        tar = {
            'filename': 'TradeActivityReport-LIFETRADING-20181004-0500561.csv',
            'status': 'Arrived',
            'report_type': 'TradeActivityReport',
            'account': '',
            'trade_date': '20181004',
            'generation_time': '0500561',
        }
        source_file = ProcessedFiles.objects.create(**tar)

        cols = [i.name for i in TradeActivityReport._meta.get_fields()
                if i.name != 'id']
        with open(os.path.dirname(process_files.__file__) + '/fixtures/TradeActivityReport-LIFETRADING-20181004-0500561.csv') as csv_file:
            for line in csv.reader(csv_file, skipinitialspace=True):
                fields = dict(zip(cols, [source_file] + line))
                tar = TradeActivityReport.objects.create(**fields)

    def test_processed_files(self):
        # print(TradeActivityReport.objects.all())
        tar = TradeActivityReport.objects.get(TradeID='20181003-00238')
        self.assertEqual(tar.CCYUnderlying, 'AUD')
        self.assertEqual(tar.Venue, 'XXXX')
        self.assertEqual(tar.ISIN, 'AU000000CYB7')
        print(tar.source_file)
