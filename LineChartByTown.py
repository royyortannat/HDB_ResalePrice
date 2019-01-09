def genLineChartByTown(p_yearEnter, p_quarterEnter, p_flatType):
        import numpy as np
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        from matplotlib.widgets import RadioButtons, CheckButtons
        from datetime import datetime
        from matplotlib import cm

        global txt, flatType, checkBoxLines
        txt = None
        yearEnter = p_yearEnter
        quarterEnter = p_quarterEnter
        quarterNum = quarterEnter
        flatType = p_flatType

        def mainTheme():
                global axcolor
                axcolor = 'lightgoldenrodyellow'
                title = "HDB Resale Flat Price Line Chart"
                ax.set_title(title,fontsize=30)
                ax.set_ylabel('Resale Price',fontsize=25)

        def get_status():
                return [checkBoxLines[index].get_visible() for index in checkBoxLines]

        def genCombineResalePrices(yearEnter, quarterNum, flatType):
                import numpy as np
                from datetime import datetime
                from matplotlib.widgets import CheckButtons
                global townSelect, towndata
                ## To get data within the Period from parameter pass of p_yearEnter p_quarterEnter to current date
                startYear = int(yearEnter)
                quarterNum = '2'
                dateEnd = datetime.now().strftime('%Y')
                endYear = int(dateEnd)
                dataPeriod = data[data['quarter'] == '2007-02']
                tdata = data[data['quarter'] == '2007-03']
                dataPeriod = np.append(dataPeriod,tdata)
                tdata = data[data['quarter'] == '2007-04']
                dataPeriod = np.append(dataPeriod,tdata)
                for i in range(startYear+1, endYear + 1):
                    for j in range(1, 5):
                        if not(i == startYear and j == 2):
                            iDate = str(i) + "-Q" + str(j)
                            idata = data[data['quarter'] == iDate]
                            dataPeriod = np.append(dataPeriod,idata)
                towndata = dataPeriod[dataPeriod['flat_type'] == flatType]

                ## To get data within the Selected Checkbox Town Line
                line_labels = [str(line.get_label()) for line in checkBoxLines]
                line_visibility = [line.get_visible() for line in checkBoxLines]
                check = CheckButtons(rax, line_labels, line_visibility)
                checkButtonThemes(check)
                status = check.get_status()
                prices = towndata['price']
                quarter = towndata['quarter']
                town_prices = np.zeros(len(townList), object)
                town_quarter = np.zeros(len(townList), object)
                for t in townIndex:
                        town_prices[t] = prices[towndata['town'] == townList[t]]
                        town_quarter[t] = quarter[towndata['town'] == townList[t]]
                return town_prices, town_quarter

        def updateCheckBox(line_labels, line_visibility, check):
                rax.clear()
                line_labels = [str(line.get_label()) for line in checkBoxLines]
                line_visibility = [line.get_visible() for line in checkBoxLines]
                check = CheckButtons(rax, line_labels, line_visibility)
                checkButtonThemes(check)

        def func(label):
                global index, towndata, checkBoxLines
                status = check.get_status()
                index = line_labels.index(label)
                checkBoxLines[index].set_visible(not checkBoxLines[index].get_visible())
                updateCheckBox(line_labels, line_visibility, check)
                towndata = towndata[towndata['flat_type'] == flatType]
                prices = towndata['price']
                quarter = towndata['quarter']
                town_prices = np.zeros(len(townList), object)
                town_quarter = np.zeros(len(townList), object)
                for t in townIndex:
                        town_prices[t] = prices[towndata['town'] == townList[t]]
                        town_quarter[t] = quarter[towndata['town'] == townList[t]]
                mainTheme()
                print(status)
                plt.draw()

        def checkButtonThemes(check):
                for r in check.rectangles:
                        r.set_alpha(0.8)
                        r.set_width(0.025)
                        r.set_edgecolor("k")

	##############            Main Process Start Here			###############
        title = "HDB Resale Flat Price Line Chart"

        data = np.genfromtxt('data/median-resale-prices-for-registered-applications-by-town-and-flat-type.csv',  
                skip_header=1, 
                dtype=[('quarter','U7'),  ('town','U30'), ('flat_type','U20'), ('price','i8')], delimiter=",",
                missing_values=['na','-'],filling_values=[0])

        null_rows = np.isnan(data['price'])
        #nonnull_prices = data[null_rows==False]
        townList = list(set(data['town']))
        townList.sort()
        townIndex = np.arange(0,len(townList))
        colorList = cm.hsv(townIndex / float(max(townIndex+10)))
        yearquarterList = list(set(data['quarter']))
        yearquarterList.sort()
        town_prices = np.zeros(len(townList), object)

        startYear = int(yearEnter)
        quarterNum = '2'
        dateEnd = datetime.now().strftime('%Y')
        endYear = int(dateEnd)
        dataPeriod = data[data['quarter'] == '2007-02']
        tdata = data[data['quarter'] == '2007-03']
        dataPeriod = np.append(dataPeriod,tdata)
        tdata = data[data['quarter'] == '2007-04']
        dataPeriod = np.append(dataPeriod,tdata)
        for i in range(startYear+1, endYear + 1):
                for j in range(1, 5):
                        if not(i == startYear and j == 2):
                                iDate = str(i) + "-Q" + str(j)
                                idata = data[data['quarter'] == iDate]
                                dataPeriod = np.append(dataPeriod,idata)
        towndata = dataPeriod[dataPeriod['flat_type'] == flatType]

        prices = towndata['price']
        quarter = towndata['quarter']
        town_prices = np.zeros(len(townList), object)
        town_quarter = np.zeros(len(townList), object)
        for t in townIndex:
                town_prices[t] = prices[towndata['town'] == townList[t]]
                town_quarter[t] = quarter[towndata['town'] == townList[t]]

        fig, ax = plt.subplots(figsize=(19,15))
        plt.subplots_adjust(left=0.25, bottom=0.25)
        mainTheme()
	
        checkBoxLines = np.zeros(len(townList), object)
        print(town_prices[0])
        for l in townIndex:
                checkBoxLines[l], = ax.plot(town_quarter[l], town_prices[l], visible=False, c=colorList[l], label=townList[l])
                ax.set_xticklabels(town_quarter[l], rotation=90)

        patches = [mpatches.Patch(color=color, label=label) for label, color in zip(townList, colorList)]
        #fig.legend(patches, townList, loc='top right', frameon=True)
        fig.legend(patches, townList,  loc='top right')
        
        #Ploting checkbox button
        # Make checkbuttons with all plotted lines with correct visibility
        rax = plt.axes([0.05, 0.25, 0.13, 0.7], facecolor=axcolor)

        line_labels = [str(line.get_label()) for line in checkBoxLines]
        line_visibility = [line.get_visible() for line in checkBoxLines]
        check = CheckButtons(rax, line_labels, line_visibility)
        checkButtonThemes(check)
      
        check.on_clicked(func)
        status = check.get_status()
        print(status)

        radioax = plt.axes([0.05, 0.08, 0.11, 0.12], facecolor=axcolor)
        radio = RadioButtons(radioax, ('1-room', '2-room', '3-room', '4-room', '5-room', 'Executive'), active=3)


        def flatTypefunc(label):
                global flatType
                quarterNum = "2"
                flatType = label
                town_prices, town_quarter = genCombineResalePrices(yearEnter, quarterNum, flatType)
                ax.clear()
                mainTheme()
                status = check.get_status()
                for l in townIndex:
                        if status[l]:
                                checkBoxLines[l], = ax.plot(town_quarter[l], town_prices[l], visible=True, c=colorList[l], label=townList[l])
                                ax.set_xticklabels(town_quarter[l], rotation=90)
                        else:
                                checkBoxLines[l], = ax.plot(town_quarter[l], town_prices[l], visible=False, c=colorList[l], label=townList[l])
                                ax.set_xticklabels(town_quarter[l], rotation=90)
                fig.canvas.draw_idle()
        radio.on_clicked(flatTypefunc)
        #ax.legend(checkBoxLines)
        #ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        town_prices, town_quarter = genCombineResalePrices(yearEnter, quarterNum, flatType)
        plt.show()

p_yearEnter = "2007"
p_quarterEnter = "2"
p_flatType = "4-room"

List_Town = ['ANG MO KIO', 'BEDOK', 'BISHAN', 'BUKIT BATOK', 'BUKIT MERAH', 'BUKIT PANJANG', 'BUKIT TIMAH', 'CENTRAL AREA', 'CHOA CHU KANG', 'CLEMENTI', 'GEYLANG', 
        'HOUGANG', 'JURONG EAST', 'JURONG WEST', 'KALLANG/WHAMPOA', 'MARINE PARADE', 'PASIR RIS', 'PUNGGOL', 'QUEENSTOWN', 'SEMBAWANG', 'SENGKANG', 'SERANGOON', 
        'TAMPINES', 'TOA PAYOH', 'WOODLANDS', 'YISHUN']
List_FlatType = ['1 ROOM', '2 ROOM', '3 ROOM', '4 ROOM', '5 ROOM', 'EXECUTIVE', 'MULTI-GENE']

#genLineChartByTown(p_yearEnter, p_quarterEnter, p_flatType)
#genLineChartByTown("2007", "2", "4-room")
