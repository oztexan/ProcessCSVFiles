import re

MATCHFILENAME = {
    'TradeActivityReport': r'TradeActivityReport-LIFETRADING-(\d+)-(\d+).csv',
    'PositionReport': r'PositionReport-(\d+)-LIFETRADING-(\d+)-(\d+).csv',
    'CollateralReport': r'CollateralReport-LIFETRADING-(\d+)-(\d+).csv'
}

PARSEFILENAME = {
    'TradeActivityReport': {
        'groups': 2,
        'trade_date': 1,
        'generation_time': 2,
        'account': -1},
    'PositionReport': {
        'groups': 3,
        'trade_date': 1,
        'generation_time': 3,
        'account': 2},
    'CollateralReport': {
        'groups': 2,
        'trade_date': 1,
        'generation_time': 2,
        'account': -1}}


def process_filename(filename):
    '''Extact attributes from filename'''
    # for each parsefilename, do regex test
    for report_type, regex in MATCHFILENAME.items():
        pattern = re.compile(regex, re.IGNORECASE)
        if pattern.match(filename):
            capture = pattern.search(filename)
            match = PARSEFILENAME[report_type]
            return {
                'filename': filename,
                'report_type': report_type,
                'trade_date': capture.group(match['trade_date'])
                              if match['generation_time'] > 0
                              and match['groups'] >= match['trade_date']
                              else '',
                'generation_time': capture.group(match['generation_time'])
                                   if match['generation_time'] > 0
                                   and match['groups'] >= match['generation_time']
                                   else '',
                'account': capture.group(match['account'])
                           if match['account'] > 0
                           and match['groups'] >= match['account']
                           else ''}

    return {
        'filename': filename,
        'report_type': 'Unknown',
        'trade_date': '',
        'generation_time': '',
        'account': ''
    }


if __name__ == "__main__":
    print("Running reporttypes.py")
else:
    print("Importing reporttypes.py")
