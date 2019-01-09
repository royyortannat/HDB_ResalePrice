def genResaleFlatPriceGraph(p_yearEnter, p_monthEnter, p_leaseEnter, p_flatType, p_labels):
        import numpy as np
        import matplotlib.pyplot as plt
        #from datetime import datetime
        from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons
        from datetime import datetime, timedelta

        global txt, flatType, checkBoxLines
        txt = None
        yearEnter = p_yearEnter
        monthEnter = p_monthEnter
        monthNum = "0" + monthEnter
        labels = p_labels
        flatType = p_flatType

        init_sLease = 50
        init_sYear = 2018
        date11halfMonthAgo = datetime.today() - timedelta(days=350)
        if init_sYear > 2000:
                init_sYear = date11halfMonthAgo.strftime('%Y')
        #print(init_sYear)

        def mainTheme():
                global axcolor
                axcolor = 'lightgoldenrodyellow'
                title = "HDB Resale Flat Price"
                titlelen = len(title)
                ax.set_title(title,fontsize=30)
                ax.set_ylabel('Resale Price',fontsize=25)


        def onclick(event):
                global txt
                nearestPrice = round(event.ydata,-3)
                #mouse click on the graph and y-axis indicate the resale price and range within 5K (upper and lower 5K)
                if nearestPrice > 0:
                        minPrice = nearestPrice - 5000
                        maxPrice = nearestPrice + 5000
                        townDet = townSelect[int(round(event.xdata,0)-1)]
                        pointSel = townDet[(townDet['resale_price'] >= minPrice) & (townDet['resale_price'] < maxPrice)]
                        if str(pointSel) != "[]":
                                txt = ax.text(event.xdata, event.ydata, str(pointSel), horizontalalignment='center', verticalalignment='center', bbox=dict(facecolor='red', alpha=0.5))
                fig.canvas.draw()

        def offclick(event):
                nearestPrice = round(event.ydata,-3)
                if nearestPrice > 0:
                        txt.remove()
                fig.canvas.draw()

        def get_status():
                return [checkBoxLines[index].get_visible() for index in checkBoxLines]

        def genCombineResalePrices(yearEnter, monthNum, p_leaseEnter, flatType):
                import numpy as np
                from datetime import datetime
                from matplotlib.widgets import CheckButtons
                global townSelect, towndata
                ## To get data within the Period from parameter pass of p_yearEnter p_monthEnter to current date
                dateStart = yearEnter + monthNum[-2:]
                firstStartDate = yearEnter + "-" + monthNum[-2:]
                dateEnd = datetime.now().strftime('%Y%m')
                dataPeriod = data[data['month'] == firstStartDate]
                for i in range(int(dateStart)+1, int(dateEnd)+1):
                        strDate = str(i)
                        last2digit = int(strDate[-2:])
                        if last2digit < 13:
                                iStrDate = str(i)
                                iDate = iStrDate[0:4] + "-" + iStrDate[-2:]
                                idata = data[data['month'] == iDate]
                                dataPeriod = np.append(dataPeriod,idata)
                ## To get data within the Flat lease period (Flat Lease > parameter p_leaseEnter)
                leaseStart = int(p_leaseEnter)+1
                leaseData = dataPeriod[dataPeriod['remaining_lease'] > leaseStart]
                flatTypeData = leaseData[leaseData['flat_type']  == flatType]
                towndata = flatTypeData

                ## To get data within the Selected Checkbox Town Line
                line_labels = [str(line.get_label()) for line in checkBoxLines]
                line_visibility = [line.get_visible() for line in checkBoxLines]
                check = CheckButtons(rax, line_labels, line_visibility)
                checkButtonThemes(check)

                status = check.get_status()

                #index = line_labels.index(label)
                #checkBoxLines[index].set_visible(not checkBoxLines[index].get_visible())
                statusIndex = np.arange(0,len(status))
                resale_prices = flatTypeData['resale_price']
                town_resale_prices = np.zeros(len(townList), object)
                for t in townIndex:
                        town_resale_prices[t] = resale_prices[towndata['town'] == townList[t]]
                townSelect = np.zeros(len(townList), object)
                townName = []
                resale_prices_combined = []
                labelIndex = -1
                for s in statusIndex:
                        if status[s]:
                                labelIndex += 1
                                townSelect[labelIndex] = towndata[towndata['town'] == townList[s]]
                                #townSelect = np.append(townSelect,sdata)
                                townName.append(line_labels[s])
                                resale_prices_combined.append(town_resale_prices[s]) 
                return resale_prices_combined, townName

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
                statusIndex = np.arange(0,len(status))
                resale_prices = towndata['resale_price']
                town_resale_prices = np.zeros(len(townList), object)
                for t in townIndex:
                        town_resale_prices[t] = resale_prices[towndata['town'] == townList[t]]
                townName = []
                resale_prices_combined = []
                labelIndex = -1
                for s in statusIndex:
                        if status[s]:
                                labelIndex += 1
                                townSelect[labelIndex] = towndata[towndata['town'] == townList[s]]
                                townName.append(line_labels[s])
                                resale_prices_combined.append(town_resale_prices[s]) 
                #ax.boxplot.clear()
                ax.clear()
                mainTheme()
                if str(resale_prices_combined) != '[]':
                        bp_dict = ax.boxplot(resale_prices_combined,labels=townName,patch_artist=True)
                        boxplotTheme(bp_dict)
                print(status)
                plt.draw()

        def update(val):
                uYear = str(sYear.val)
                uLease = sLease.val
                monthNum = "01"
                resale_prices_combined, labels = genCombineResalePrices(uYear[0:4], monthNum, uLease, flatType)
                #ax.boxplot.clear()
                ax.clear()
                mainTheme()
                if str(resale_prices_combined) != '[]':
                        bp_dict = ax.boxplot(resale_prices_combined,labels=labels,patch_artist=True)
                        boxplotTheme(bp_dict)
                fig.canvas.draw_idle()

        def checkButtonThemes(check):
                for r in check.rectangles:
                        r.set_alpha(0.8)
                        r.set_width(0.025)
                        r.set_edgecolor("k")

	##############            Main Process Start Here			###############
        title = "HDB Resale Flat Price"
        titlelen = len(title)
        #print("{:*^{titlelen}}".format(title, titlelen=titlelen+6))
        #print()
        data = np.genfromtxt('data/resale-flat-prices.csv', 
                skip_header=1, 
                dtype=[('month','U7'), ('town','U30'), ('flat_type','U20'), ('block','U4'), ('street_name','U50'), 
                        ('storey_range','U15'), ('floor_area_sqm','U3'), ('flat_model','U25'),
                        ('lease_commence_date','U4'), ('remaining_lease','i2'), ('resale_price','f8')], 
                        delimiter=",", missing_values=['na','-'],filling_values=[0])
        null_rows = np.isnan(data['resale_price'])
        nonnull_resale_prices = data[null_rows==False]
        townList = list(set(data['town']))
        townList.sort()
        townIndex = np.arange(0,len(townList))

        yearmonthList = list(set(data['month']))

        minsYear = int(yearmonthList[0][0:4])
        maxsYear = int(yearmonthList[0][0:4])
        for yearmonthRec in yearmonthList:
                if int(yearmonthRec[0:4]) < minsYear:
                        minsYear = int(yearmonthRec[0:4])
                if int(yearmonthRec[0:4]) > maxsYear:
                        maxsYear = int(yearmonthRec[0:4])

        #print(minYear)
        #print(maxYear)

        date11halfMonthAgo = datetime.today() - timedelta(days=350)
        init_sYear = date11halfMonthAgo.strftime('%Y')


        #print("Filtered data: " + str(nonnull_resale_prices.shape))

        fig, ax = plt.subplots(figsize=(19,15))
        plt.subplots_adjust(left=0.25, bottom=0.25)
        mainTheme()
	
        #Create a dummy ax plot line to capture the status of visible or non visible town 
        #so later can be use in boxplot
        checkBoxLines = np.zeros(len(townList), object)
        for l in townIndex:
                checkBoxLines[l], = ax.plot(0, 0, visible=False, lw=2, label=townList[l])
        #Ploting checkbox button
        # Make checkbuttons with all plotted lines with correct visibility
        rax = plt.axes([0.05, 0.2, 0.13, 0.7], facecolor=axcolor)

        line_labels = [str(line.get_label()) for line in checkBoxLines]
        line_visibility = [line.get_visible() for line in checkBoxLines]
        check = CheckButtons(rax, line_labels, line_visibility)
        checkButtonThemes(check)

        check.on_clicked(func)
        status = check.get_status()
        print(status)

        axYear = plt.axes([0.5, 0.15, 0.4, 0.03], facecolor=axcolor)
        axLease = plt.axes([0.5, 0.1, 0.4, 0.03], facecolor=axcolor)

        sYear = Slider(axYear, 'Year From', minsYear, maxsYear, valinit=int(init_sYear), valstep=1)
        sLease = Slider(axLease, 'Min Remain Lease Year', 1, 99, valinit=int(init_sLease), valstep=1)

        radioax = plt.axes([0.25, 0.08, 0.11, 0.12], facecolor=axcolor)
        radio = RadioButtons(radioax, ('1 ROOM', '2 ROOM', '3 ROOM','4 ROOM','5 ROOM','EXECUTIVE','MULTI-GENE'), active=3)

        sYear.on_changed(update)
        sLease.on_changed(update)

        def flatTypefunc(label):
                global flatType
                uYear = str(sYear.val)
                uLease = sLease.val
                monthNum = "01"
                flatType = label
                resale_prices_combined, labels = genCombineResalePrices(uYear[0:4], monthNum, uLease, flatType)
                ax.clear()
                mainTheme()
                if str(resale_prices_combined) != '[]':
                        bp_dict = ax.boxplot(resale_prices_combined,labels=labels,patch_artist=True)
                        boxplotTheme(bp_dict)
                fig.canvas.draw_idle()
        radio.on_clicked(flatTypefunc)

        fig.canvas.mpl_connect('button_press_event', onclick)
        fig.canvas.mpl_connect('button_release_event', offclick) 

        resale_prices_combined, labels = genCombineResalePrices(yearEnter, monthNum, p_leaseEnter, flatType)

        if str(resale_prices_combined) != '[]':
                bp_dict = ax.boxplot(resale_prices_combined,labels=labels,patch_artist=True)
                #labels = ['']
                #resale_prices_combined = ['0']
                boxplotTheme(bp_dict)

        def boxplotTheme(bp_dict):
                #global bp_dict
                ## change outline color, fill color and linewidth of the boxes
                for box in bp_dict['boxes']:
                        # change outline color
                        box.set( color='#7570b3', linewidth=2)
                        # change fill color
                        box.set( facecolor = '#1b9e77' )

                ## change color and linewidth of the whiskers
                for whisker in bp_dict['whiskers']:
                        whisker.set(color='#7570b3', linewidth=2)

                ## change color and linewidth of the caps
                for cap in bp_dict['caps']:
                        cap.set(color='#7570b3', linewidth=2)

                ## change color and linewidth of the medians
                for median in bp_dict['medians']:
                        median.set(color='#b2df8a', linewidth=2)

                ## change the style of fliers and their fill
                for flier in bp_dict['fliers']:
                        flier.set(marker='D', color='#e7298a', alpha=0.5)

                print(bp_dict.keys())

                for line in bp_dict['medians']:
                        # get position data for median line
                        x, y = line.get_xydata()[1] # top of median line
                        # overlay median resale_price
                        #ax[0].plt.text(x, y, '%.1f' % y,
                        ax.text(x, y, '%.1f' % y,
                                horizontalalignment='center',fontsize=15) # draw above, centered

                fliers = []
                for line in bp_dict['fliers']:
                        ndarray = line.get_xydata()
                        if (len(ndarray)>0):
                                max_flier = ndarray[:,1].max()
                                max_flier_index = ndarray[:,1].argmax()
                                x = ndarray[max_flier_index,0]
                                print("Flier: " + str(x) + "," + str(max_flier))
                                ax.text(x,max_flier,'%.1f' % max_flier,horizontalalignment='center',fontsize=15,color='green') 
                                

        plt.show()

p_yearEnter = "2017"
p_monthEnter = "01"
p_leaseEnter = "50"
p_flatType = "4 ROOM"
#p_labels = ['ANG MO KIO', 'BISHAN', 'KALLANG/WHAMPOA', 'SERANGOON', 'TOA PAYOH']
p_labels = []

List_Town = ['ANG MO KIO', 'BEDOK', 'BISHAN', 'BUKIT BATOK', 'BUKIT MERAH', 'BUKIT PANJANG', 'BUKIT TIMAH', 'CENTRAL AREA', 'CHOA CHU KANG', 'CLEMENTI', 'GEYLANG', 
        'HOUGANG', 'JURONG EAST', 'JURONG WEST', 'KALLANG/WHAMPOA', 'MARINE PARADE', 'PASIR RIS', 'PUNGGOL', 'QUEENSTOWN', 'SEMBAWANG', 'SENGKANG', 'SERANGOON', 
        'TAMPINES', 'TOA PAYOH', 'WOODLANDS', 'YISHUN']
List_FlatType = ['1 ROOM', '2 ROOM', '3 ROOM', '4 ROOM', '5 ROOM', 'EXECUTIVE', 'MULTI-GENE']

#genResaleFlatPriceGraph(p_yearEnter, p_monthEnter, p_leaseEnter, p_flatType, p_labels)
