def genHDBdwelling():
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.widgets import RadioButtons

    title = "Total HDB Dwellings"
    titlelen = len(title)
    print("{:*^{titlelen}}".format(title, titlelen=titlelen+6))
    print()

    data = np.genfromtxt('data/resident-households-by-type-of-dwelling-hdb-ethnic-grp-of-head-of-household-tenancy.csv',
                                skip_header=1, 
                                dtype=[('year','U10'), ('level_1','U50'), ('level_2','U50'), ('level_3','U50'), ('level_4','U50'), 
                                ('value','f8')], delimiter=",",
                                missing_values=['na','-'],filling_values=[0])

    #print("Original data: " + str(data.shape))

    null_rows = np.isnan(data['value'])
    nonnull_values = data[null_rows==False]
    #print("Filtered data: " + str(nonnull_values.shape))

    #Get only Total value of each categories
    dataTotal = data[data['level_2'] == 'Total']

    flatType = '4-Room Flats'
    dataSelect = dataTotal[dataTotal['level_4'] == flatType]
    #print(dataSelect)
    fig, ax = plt.subplots(figsize=(19, 15), subplot_kw=dict(aspect="equal"))
    plt.subplots_adjust(bottom=0.25)

    def plotPieChart(dataSelect):
        labels = list(set(dataSelect['level_1']))
        labels = ['Chinese','Malays','Indians','Others']
        levels = np.arange(0,len(labels))
        levels_values = dataSelect[['level_1','value']]

        values = levels_values['value']
        values_TotalHDBDwellings = values[levels_values ['level_1'] == 'Total']
        values_Chinese = values[levels_values['level_1'] == 'Chinese']
        values_Malays = values[levels_values['level_1'] == 'Malays']
        values_Indians = values[levels_values ['level_1'] == 'Indians']
        values_Others = values[levels_values ['level_1'] == 'Others']

        values_combined =[values_Chinese, values_Malays, values_Indians, values_Others]
        racesList = np.concatenate(values_combined).ravel().tolist()
        #print(racesList)
        ax.clear()

        def func(pct, allvals):
            absolute = int(pct/100.*np.sum(allvals))
            return "{:.1f}%\n({:d} g)".format(pct, absolute)

        wedges, texts, autotexts = ax.pie(racesList, autopct=lambda pct: func(pct, racesList), textprops=dict(color="w"))

        ax.legend(wedges, labels,
            title="HDB Dwelling By Ethnic Group",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(autotexts, size=8, weight="bold")

        ax.set_title("HDB Dwelling By Ethnic Group and Flat Type")


    plotPieChart(dataSelect)

    ###### ['1- and 2-Room Flats', '3-Room Flats', '4-Room Flats', '5-Room and Executive Flats']
    axcolor = 'lightgoldenrodyellow'
    radioax = plt.axes([0.25, 0.08, 0.15, 0.12], facecolor=axcolor)
    radio = RadioButtons(radioax, ('1- and 2-Room Flats', '3-Room Flats', '4-Room Flats','5-Room and Executive Flats'), active=2)

    def flatTypefunc(label):
        global flatType
        flatType = label
        dataSelect = dataTotal[dataTotal['level_4'] == flatType]
        plotPieChart(dataSelect)
        #fig.canvas.draw_idle()
        plt.draw()
    radio.on_clicked(flatTypefunc)

    plt.show()

