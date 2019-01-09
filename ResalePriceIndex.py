def genResalePriceIndex():
    import numpy as np
    import matplotlib.pyplot as plt
    from datetime import datetime
    title = "HDB Resale Flat Index Price Line Chart"
    titlelen = len(title)
    print("{:*^{titlelen}}".format(title, titlelen=titlelen+6))
    print()

    data = np.genfromtxt('data/housing-and-development-board-resale-price-index-1q2009-100-quarterly.csv',  
                                skip_header=1, 
                                dtype=[('quarter','U7'), ('index','f8')], delimiter=",",
                                missing_values=['na','-'],filling_values=[0])

    yearEnter = '2007'
    startYear = int(yearEnter)
    quarterNum = '1'
    dateStart = yearEnter + quarterNum[-1:]
    firstStartDate = yearEnter + "-Q" + quarterNum[-1:]
    endYearDate = datetime.now().strftime('%Y')
    endYear = int(endYearDate)
    dataPeriod = data[data['quarter'] == firstStartDate]
    for i in range(startYear, endYear + 1):
        for j in range(1, 5):
            if not(i == startYear and j == 1):
                iDate = str(i) + "-Q" + str(j)
                idata = data[data['quarter'] == iDate]
                dataPeriod = np.append(dataPeriod,idata)
                #print(iDate)

    dataSelect = dataPeriod

    x_unit = dataSelect['quarter']
    y_unit = dataSelect['index']

    fig = plt.figure(figsize=(19,15))
    plt.subplots_adjust(bottom=0.25)
    ax1 = fig.add_subplot(111)
    ax1.set_title(title,fontsize=30)

    ax1.plot(x_unit, y_unit, c='b',  label='2009 Q1 as 100')
    plt.ylabel('Index', fontsize = 20)

    plt.xticks(rotation=45)

    plt.legend(loc='upper left')

    plt.show()

