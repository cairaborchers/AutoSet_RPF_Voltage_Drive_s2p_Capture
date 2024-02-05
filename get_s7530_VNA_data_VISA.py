import pyvisa
from time import sleep 

class get_s7530_VNA_data_VISA:
    
    def __init__(self):

        rm = pyvisa.ResourceManager('C:/WINDOWS/system32/visa64.dll')

        #connect to the socket server
        try:
            self.s7530 = rm.open_resource('TCPIP0::127.0.0.1::5025::SOCKET')
        except:
            print("Failure to connect to VNA!")
            print("Check network settings")

        #the VNA ends each line with \n
        self.s7530.read_termination='\n'

        self.s7530.write("*ESR?")
        self.esr_response = self.s7530.read()

        #Get cylce time
        self.s7530.write("SYSTem:CYCLe:TIME:MEASurement?")
        cycle_time = self.s7530.read()

        #change to computer triggering
        self.s7530.write("TRIG:SOUR BUS")

        #end with an *OPC? to make sure the setups are complete (blocks)
        self.s7530.write("*OPC?")
        self.opc_response = self.s7530.read()

    def check_s7530_ok(self):
        
        check_s7530_ok = True
        self.s7530.write("*CLS")
        
        self.s7530.write("SYST:ERR?")
        reply = self.s7530.read()
        if reply.find('0') < -1:
            check_s7530_ok = False

        self.s7530.write("*STB?")
        status_byte = self.s7530.read()
        if status_byte.find('0') < -1:
            check_s7530_ok = False

        return check_s7530_ok
        
    
    def sweep(self, name):
        
        if self.check_s7530_ok() == True:

            #trigger a single sweep
            self.s7530.write("TRIG:SING")

            while self.esr_response == 0:
                
                sleep(20)
                #self.s7530.write("*ESR?")
                self.s7530.write("*ESR?")
                self.esr_response = self.s7530.read()

            self.s7530.write('MMEM:STOR:SNP:DATA C:\\s2p_save_remote\\' + name + '.s2p')
        
    def single_Sweep(self, name):
        
        if self.check_s7530_ok() == True:

            #trigger a single sweep
            self.s7530.write("TRIG:SING")

            self.opc_response = 0
            
            while self.opc_response == 0:
                
                sleep(5)
                self.s7530.write("*OPC?")
                self.opc_response = self.s7530.read()

            sleep(2)

            self.s7530.write('MMEM:STOR:SNP:DATA C:\\s2p_save_remote\\' + name + '.s2p')

            sleep(2)