def genSpecificFlat():
	import numpy as np
	import matplotlib.pyplot as plt
	from matplotlib.widgets import TextBox, RadioButtons
	from datetime import datetime, timedelta
	from matplotlib import cm


	global txt, flatType, checkBoxLines, enterStreet, enterFloor, selectFlatType
	txt = None
	init_sLease = 50
	init_sYear = 2018
	date11halfMonthAgo = datetime.today() - timedelta(days=350)
	if init_sYear > 2000:
		init_sYear = date11halfMonthAgo.strftime('%Y')

	def mainTheme():
		global axcolor
		axcolor = 'lightgoldenrodyellow'
		title = "Avg HDB Resale Flat Price for the past 20 months"
		#titlelen = len(title)
		ax.set_title(title,fontsize=30)
		ax.set_ylabel('Resale Price',fontsize=25)

	def plotBarChart(selectFlatType, enterStreet, enterFloor):
		flatTypeData = dataPeriod[dataPeriod['flat_type']==selectFlatType]
		floorData = flatTypeData[flatTypeData['storey_range']==enterFloor]
		specificData = floorData[floorData['street_name']==enterStreet]
		#specificData = dataPeriod[(dataPeriod['flat_type']==selectFlatType) & (dataPeriod['street_name']==enterStreet) & (dataPeriod['storey_range']==enterFloor)]
		resale_prices = specificData['resale_price']
		avg_resale_prices = {}

		for i in yrsmthlast20monthsList:
			resalePriceForMonth = resale_prices[specificData['month']==i]
			if str(resalePriceForMonth) == '[]':
				avg = 0
			else:
				avg = np.average(resalePriceForMonth)
			#print("Average for year-month " + i + " is {:.0f}".format(avg))
			avg_resale_prices[i] = avg

		if str(avg_resale_prices) != '{}':
			ax.clear()
			mainTheme()
			barchart = ax.bar(list(avg_resale_prices.keys()), list(avg_resale_prices.values()), color='#d62728')
			for i in range(len(barchart)):
				bar = barchart[i]
				x,y  = bar.get_xy()
				h = bar.get_height()
				ax.text(x,h,"{:.0f}".format(list(avg_resale_prices.values())[i]),fontsize=10)
			#ax.title('Avg HDB Resale Flat Price for the past 20 months',fontsize=40)
			ax.ylabel('Resale Price',fontsize=40)
			ax.yticks(fontsize=20)
			ax.xticks(yrsmthlast20monthsIndex, yrsmthlast20monthsList, fontsize=40,rotation=30)
			plt.figure(1) # first figure

	##############            Main Process Start Here			###############
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

	storeyList = list(set(data['storey_range']))
	storeyList.sort()
	storeyIndex = np.arange(0,len(storeyList))

	yearmonthList = list(set(data['month']))
	yearmonthList.sort()
	yearmonthIndex = np.arange(0,len(yearmonthList))

	last20months = yearmonthIndex[-20:]
	#copy the first months of last20months data
	dataPeriod = data[data['month'] == yearmonthList[last20months[0]]]
	#copy the remaining 19 months of data
	for eachMonth in last20months:
		if eachMonth != last20months[0]:
			idata = data[data['month'] == yearmonthList[eachMonth]]
			dataPeriod = np.append(dataPeriod,idata)

	yrsmthlast20monthsList = list(set(dataPeriod['month']))
	yrsmthlast20monthsList.sort()
	yrsmthlast20monthsIndex = np.arange(0,len(yrsmthlast20monthsList))
	avg_resale_prices = {}

	fig, ax = plt.subplots(figsize=(19,15))
	plt.subplots_adjust(bottom=0.25)
	mainTheme()
	initial_textStreet = ""
	initial_textFloor = ""

	labels = yrsmthlast20monthsList
	levels = np.arange(0,len(labels))
	selectFlatType = '4 ROOM'
	enterStreet = ''
	enterFloor = ''

	if  str(avg_resale_prices) != '{}':
		plt.figure(1) # first figure

	def submitStreet(text):
		global enterStreet
		if len(text.strip()) > 0:
			enterStreet = (text.strip()).upper()
			enterStreet = enterStreet.replace('LORONG','LOR')
			enterStreet = enterStreet.replace('AVENUE','AVE')
		if len(enterStreet) > 0 and len(enterFloor) > 0:
			plotBarChart(selectFlatType, enterStreet, enterFloor)
		plt.draw()

	def submitFloor(text):
		global enterFloor
		storeyType = ''
		if len(text.strip()) > 0:
			for s in storeyIndex:
				if int(text.strip()) >= int(storeyList[s][0:2]) and int(text.strip()) <= int(storeyList[s][-2:]):
					storeyType = storeyList[s]
			enterFloor = storeyType
		if len(enterStreet) > 0 and len(enterFloor) > 0:
			plotBarChart(selectFlatType, enterStreet, enterFloor)
		plt.draw()

	axbox_street = plt.axes([0.25, 0.1, 0.55, 0.07])
	text_box_street = TextBox(axbox_street, 'Street: ', initial=initial_textStreet)
	text_box_street.on_submit(submitStreet)

	axbox_floor = plt.axes([0.84, 0.1, 0.05, 0.07])
	text_box_floor = TextBox(axbox_floor, 'Floor: ', initial=initial_textFloor)
	text_box_floor.on_submit(submitFloor)

	radioax = plt.axes([0.09, 0.08, 0.11, 0.12], facecolor=axcolor)
	radio = RadioButtons(radioax, ('1 ROOM', '2 ROOM', '3 ROOM','4 ROOM','5 ROOM','EXECUTIVE','MULTI-GENE'), active=3)

	def flatTypefunc(typeFlat):
		global selectFlatType
		selectFlatType = typeFlat
		if len(enterStreet) > 0 and len(enterFloor) > 0:
			ax.clear()
			mainTheme()
			plotBarChart(selectFlatType, enterStreet, enterFloor)
	radio.on_clicked(flatTypefunc)

	plt.show()
