'''Models required for app process_files'''


from django.db import models

# class ThreadTask(models.Model):
#     task = models.CharField(max_length=30, blank=True, null=True)
#     is_done = models.BooleanField(blank=False, default=False)


class ProcessedFiles(models.Model):
    '''Keeps record of all files discovered and tracks relevant metadata.'''
    STATUS_TYPES = (
        ('A', 'Arrived'),
        ('P', 'Processed'),
        ('D', 'Deprecated'),
    )
    filename = models.CharField(max_length=120, blank=True, null=True)
    # Enum ['Arrived', 'Processed', 'Deprecated']
    status = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        choices=STATUS_TYPES)
    report_type = models.CharField(max_length=120, blank=True, null=True)
    account = models.CharField(max_length=120, blank=True, null=True)
    trade_date = models.CharField(max_length=120, blank=True, null=True)
    generation_time = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return """%s,
        status = %s,
        report_type = %s,
        account = %s,
        trade_date = %s,
        generation_time = %s""" % (
            self.filename,
            self.status,
            self.report_type,
            self.account,
            self.trade_date,
            self.generation_time)


class TradeActivityReport(models.Model):
    '''All trade activity captured through history tagged with source file.'''
    source_file = models.ForeignKey(ProcessedFiles, on_delete=models.CASCADE)
    CounterpartyShor = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        db_column='CounterpartyShor')
    TradeID = models.CharField(max_length=30,
                               blank=True,
                               null=True,
                               db_column='TradeID')
    TradeDate = models.CharField(max_length=30,
                                 blank=True,
                                 null=True,
                                 db_column='TradeDate')
    SettlementDate = models.CharField(max_length=30,
                                      blank=True,
                                      null=True,
                                      db_column='SettlementDate')
    Ticker = models.CharField(max_length=30,
                              blank=True,
                              null=True,
                              db_column='Ticker')
    ISIN = models.CharField(max_length=30,
                            blank=True,
                            null=True,
                            db_column='ISIN')
    Name = models.CharField(max_length=30,
                            blank=True,
                            null=True,
                            db_column='Name')
    ProductShortName = models.CharField(max_length=30,
                                        blank=True,
                                        null=True,
                                        db_column='ProductShortName')
    StrategyExternalID = models.CharField(max_length=30,
                                          blank=True,
                                          null=True,
                                          db_column='Strategy(ExternalID)')
    Qty = models.CharField(max_length=30,
                           blank=True,
                           null=True,
                           db_column='Qty')
    Type = models.CharField(max_length=30,
                            blank=True,
                            null=True,
                            db_column='Type')
    CCYUnderlying = models.CharField(max_length=30,
                                     blank=True,
                                     null=True,
                                     db_column='CCYUnderlying')
    GrossPriceLocal = models.CharField(max_length=30,
                                       blank=True,
                                       null=True,
                                       db_column='GrossPrice(Local)')
    FXRate = models.CharField(max_length=30,
                              blank=True,
                              null=True,
                              db_column='FXRate')
    GrossPriceSwap = models.CharField(max_length=30,
                                      blank=True,
                                      null=True,
                                      db_column='GrossPriceSwap')
    Comms = models.CharField(max_length=30,
                             blank=True,
                             null=True,
                             db_column='Comms')
    MarketCharges = models.CharField(max_length=30,
                                     blank=True,
                                     null=True,
                                     db_column='MarketCharges')
    NetPriceSwap = models.CharField(max_length=30,
                                    blank=True,
                                    null=True,
                                    db_column='NetPriceSwap')
    SwapCCY = models.CharField(max_length=30,
                               blank=True,
                               null=True,
                               db_column='SwapCCY')
    TradedNotionalAmt = models.CharField(max_length=30,
                                         blank=True,
                                         null=True,
                                         db_column='TradedNotionalAmt')
    FundingRate = models.CharField(max_length=30,
                                   blank=True,
                                   null=True,
                                   db_column='FundingRate')
    Spread = models.CharField(max_length=30,
                              blank=True,
                              null=True,
                              db_column='Spread')
    Performance = models.CharField(max_length=30,
                                   blank=True,
                                   null=True,
                                   db_column='Performance')
    FundingReset = models.CharField(max_length=30,
                                    blank=True,
                                    null=True,
                                    db_column='FundingReset')
    DividendEntitlement = models.CharField(max_length=30,
                                           blank=True,
                                           null=True,
                                           db_column='DividendEntitlement')
    InitialMargin = models.CharField(max_length=30,
                                     blank=True,
                                     null=True,
                                     db_column='InitialMargin')
    ProductType = models.CharField(max_length=30,
                                   blank=True,
                                   null=True,
                                   db_column='ProductType')
    RemainingNotionalAmt = models.CharField(max_length=30,
                                            blank=True,
                                            null=True,
                                            db_column='RemainingNotionalAmt')
    UniqueTransactionID = models.CharField(max_length=30,
                                           blank=True,
                                           null=True,
                                           db_column='Unique Transaction ID')
    TradeTime = models.CharField(max_length=30,
                                 blank=True,
                                 null=True,
                                 db_column='TradeTime')
    TotalComm = models.CharField(max_length=30,
                                 blank=True,
                                 null=True,
                                 db_column='TotalComm')
    TotalMarket = models.CharField(max_length=30,
                                   blank=True,
                                   null=True,
                                   db_column='TotalMarket')
    OrderIns = models.CharField(max_length=30,
                                blank=True,
                                null=True,
                                db_column='OrderIns')
    InstrumentIdentifier = models.CharField(max_length=30,
                                            blank=True,
                                            null=True,
                                            db_column='InstrumentIdentifier')
    Venue = models.CharField(max_length=30,
                             blank=True,
                             null=True,
                             db_column='Venue')

    def __str__(self):
        return "%s %s %s %s" % (self.Qty, self.Ticker,
                                self.TradeDate, self.CounterpartyShor)
