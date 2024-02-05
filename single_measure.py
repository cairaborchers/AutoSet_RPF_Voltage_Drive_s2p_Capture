import ComCommand
import get_s7530_VNA_data_VISA
import pandas as pd
import time

#Program sturcture:
    #Open port
    #Set up VNA

    #Read voltages from file

    #for Loop for drive voltages
        #for loop for upper vs lower eq
            #call comdata with upper or lower eq
            #call comdata 3 times with commands for 3 voltages
            #call get s7530 vna data
    
    #close port 

#Open Port

portCom = ComCommand.ComCommand()

#Set up vna
vna = get_s7530_VNA_data_VISA.get_s7530_VNA_data_VISA()
vna.check_s7530_ok()

#Read Voltages From File
#85 RPF
df = pd.read_excel("85_RPF_Voltages_1_26_24.xlsx")

#396 RPF
#df = pd.read_excel("396_RPF_voltages_1_17_24_v3.xlsx")

#492 RPF
#df = pd.read_excel("492_RPF_voltages_1_15_24.xlsx")

#index, starting at tilt0 = 0
index = 8

i = index + 1
#send voltages to RPF + Get s2p files from NA
for i in range(i-1, index + 1): 
    
    drv1 = str(df.iloc[i,1]*100)
    drv2 = str(df.iloc[i,2]*100)
    drv3 = str(df.iloc[i,3]*100)
    
    #send voltages to RPF
    portCom.sendCommand("ble rpf drv1 " + drv1 + "\r")
    portCom.sendCommand("ble rpf drv2 " + drv2 + "\r")
    portCom.sendCommand("ble rpf drv3 " + drv3 + "\r")
    
    j = 0
    for j in range(2):

        if j == 0:
            #set switched eq to lower
            portCom.sendCommand("ble switch rpfsw" + " " + "0" + "\r")
            filename = "real_" + str(i)
            time.sleep(.5)
        else:
            #set switched eq to higher
            portCom.sendCommand("ble switch rpfsw" + " " + "1" + "\r")
            filename = "real_U_" + str(i)
            time.sleep(.5)
        
        #Get s2p files from NA
        vna.single_Sweep(filename)

portCom.closePort()