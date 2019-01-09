def genResaleApplication():
        import numpy as np
        import matplotlib.pyplot as plt
        from matplotlib.widgets import RadioButtons

        title = "Total HDB Dwellings"
        titlelen = len(title)
        print("{:*^{titlelen}}".format(title, titlelen=titlelen+6))
        print()

        data = np.genfromtxt('data/number-of-resale-applications-registered-by-flat-type.csv',
                                skip_header=1, 
                                dtype=[('quarter','U7'), ('flat_type','U10'), 
                                ('no_of_resale_applications','f8')], delimiter=",",
                                missing_values=['na','-'],filling_values=[0])

        #print("Original data: " + str(data.shape))

        null_rows = np.isnan(data['no_of_resale_applications'])
        nonnull_values = data[null_rows==False]
        #print("Filtered data: " + str(nonnull_values.shape))

        #flatType = '4-room'
        #dataSelect = data[data['flat_type'] == flatType]
        dataSelect = data
        #print(dataSelect)


        def plotHistogram(dataSelect):
                labels = list(set(dataSelect['flat_type']))
                labels = ['1 & 2-room','3-room','4-room','5-room','Executive']
                levels = np.arange(0,len(labels))
                flat_type_no_of_resale = dataSelect[['flat_type','no_of_resale_applications']]

                no_of_resale = flat_type_no_of_resale['no_of_resale_applications']
                no_of_resale_1_2_room = no_of_resale[(flat_type_no_of_resale ['flat_type'] == '1-room') | (flat_type_no_of_resale['flat_type'] == '2-room')]
                no_of_resale_3_room = no_of_resale[flat_type_no_of_resale['flat_type'] == '3-room']
                no_of_resale_4_room = no_of_resale[flat_type_no_of_resale ['flat_type'] == '4-room']
                no_of_resale_5_room = no_of_resale[flat_type_no_of_resale ['flat_type'] == '5-room']
                no_of_resale_Executive = no_of_resale[flat_type_no_of_resale ['flat_type'] == 'Executive']
                print(no_of_resale_1_2_room)

                no_of_resale_combined =[no_of_resale_1_2_room,
                                                no_of_resale_3_room,
                                                no_of_resale_4_room,
                                                no_of_resale_5_room,
                                                no_of_resale_Executive]
                # Create bins of 2000 each
                #bins = np.arange(data1.min(), data2.max(), 2000) # fixed bin size

                # row and column sharing
                f, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, sharex='col', sharey='row', figsize=(19,15))
                #plt.subplots_adjust(bottom=0.25)

                #axes 1 # first figure
                hist_all = ax1.hist(no_of_resale_combined,
                        alpha=0.5, 
                        color=['red','green','blue','cyan','magenta'],
                        label=labels)
                ax1.set_title("All Room Resale Applications",fontsize=20)
                ax1.set_ylabel('No. of Quarters',fontsize=10)
                ax1.legend()

                #axes 2.figure(2) # second figure
                ax2.hist(no_of_resale_1_2_room,  
                        alpha=0.5, 
                        color=['red'])
                ax2.set_title("1 & 2 Room Resale",fontsize=20)
                ax2.set_ylabel('No. of Quarters',fontsize=10)

                #plt.figure(3) # third figure
                ax3.hist(no_of_resale_Executive,  
                        alpha=0.5, 
                        color=['magenta'])
                ax3.set_title("Executive Room Resale",fontsize=20)
                ax3.set_ylabel('No. of Quarters',fontsize=10)

                #plt.figure(4) # fourth figure
                ax4.hist(no_of_resale_3_room,  
                        alpha=0.5, 
                        color=['green'])
                ax4.set_title("3 Room Resale",fontsize=20)
                ax4.set_ylabel('No. of Quarters',fontsize=10)

                #plt.figure(5) # fifth figure
                ax5.hist(no_of_resale_4_room,  
                        alpha=0.5, 
                        color=['blue'])
                ax5.set_title("4 Room Resale",fontsize=20)
                ax5.set_ylabel('No. of Quarters',fontsize=10)

                #plt.figure(6) # sixth figure
                ax6.hist(no_of_resale_5_room,  
                        alpha=0.5, 
                        color=['cyan'])
                ax6.set_title("5 Room Resale",fontsize=20)
                ax6.set_ylabel('No. of Quarters',fontsize=10)

        plotHistogram(dataSelect)


        plt.show()

