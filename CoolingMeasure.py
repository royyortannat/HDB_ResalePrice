def genCoolingMeasure():
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from datetime import datetime

    def convQuarter(qDate):
        syear = qDate[0:4]
        quart = qDate[-1]
        if quart == "1":
            mmdd = "-03-31"
        elif quart == "2":
            mmdd = "-06-30"
        elif quart == "3":
            mmdd = "-09-30"
        else:
            mmdd = "-12-31"
        sdate = syear + mmdd
        return sdate

    # Converter to convert quarter to datetime objects
    func = lambda s: datetime.strptime(convQuarter(s.decode("utf-8")), "%Y-%m-%d")

    # Converter to convert date strings to datetime objects
    conv = lambda s: datetime.strptime(s.decode("utf-8"), "%Y-%m-%d")

    converters = {0: func}

    cooldata = np.genfromtxt('data/cooling-measure.csv',
        skip_header=1,
        dtype=[('cooldate','datetime64[s]'),  ('cooldesc','U20'), ('coolcolor','U20')], delimiter=",",
        converters={0: conv}, missing_values=['na','-'],filling_values=[0])

    coolList = list(set(cooldata['cooldate']))
    coolList.sort()
    coolIndex = np.arange(0,len(coolList))

    data = np.genfromtxt('data/median-resale-prices-for-registered-applications-by-town-and-flat-type.csv',
        skip_header=1,
        dtype=[('quarter','datetime64[s]'),  ('town','U30'), ('flat_type','U20'), ('price','i8')], delimiter=",",
        converters={0: func}, missing_values=['na','-'],filling_values=[0])

    dataSelect = data[data['price']>0]

    x_quarter_4room = dataSelect[dataSelect['flat_type']=='4-room']['quarter']
    y_price_4room = dataSelect[dataSelect['flat_type']=='4-room']['price']

    x_quarter_5room = dataSelect[dataSelect['flat_type']=='5-room']['quarter']
    y_price_5room = dataSelect[dataSelect['flat_type']=='5-room']['price']

    fig = plt.figure(figsize=(19,15))
    plt.subplots_adjust(bottom=0.25)
    ax1 = fig.add_subplot(111)

    ax1.scatter(x_quarter_4room , y_price_4room , s=30, c='red', marker="*", label='4 Room')
    ax1.scatter(x_quarter_5room , y_price_5room , s=10, c='blue', marker="x", label='5 Room')

    ax1.legend(loc = 0)

    title = "Major Cooling Measures Affecting HDB Resale Flat Price"
    ax1.set_title(title,fontsize=30)
    ax1.set_ylabel('Resale Price',fontsize=25)

    ### Ploting vertical line stating the cooling measure's date ####
    for i in coolIndex:
        ax1.axvline(cooldata['cooldate'][i], color=cooldata['coolcolor'][i], zorder=0, linestyle='--')
        ax1.text(cooldata['cooldate'][i], 250000, cooldata['cooldesc'][i], color=cooldata['coolcolor'][i], rotation=90)

    ax1.set_xlabel('Date')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    plt.gcf().autofmt_xdate()

    #plt.legend(loc='upper left')
    plt.show()

