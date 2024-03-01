import time
import im
import sys

class Client:
    
    def __init__(self):
        self.status = None
        self.message = ''
        self.server = im.IMServerProxy('https://web.cs.manchester.ac.uk/n72011jr/comp28112_ex1/IMserver.php') 
    
    
    def connection(self):
        try:
            if len(self.server.keys()) == 1:
                self.server['conn'] = '0'
            elif self.server['conn'].decode().strip() == 'closing':
                self.server.clear()
                self.server['conn'] = '0'
            if self.server['conn'].decode().strip() == '0':
                self.status = True
                self.server['conn'] = b'1'
            elif self.server['conn'].decode().strip() == '1':
                self.status = False
                self.server['conn'] = b'connected'
            elif self.server['conn'].decode().strip() == 'connected':
                print("Server is full")
                self.server['conn'] = b'full'
                sys.exit()
            else:
                self.terminate("Error")

            loading = ""
            printed_message = False
            while self.server['conn'].decode().strip() != 'connected':
                if printed_message == False:
                    print("Searching for another user...")
                    printed_message = True
                loading += '.'
                if loading.count('.') >= 15:
                    self.terminate("Second user not found.")
                time.sleep(1)

            print("  ")
            self.server['received'] = b'0'
            self.server['message'] = b''

        except KeyboardInterrupt:
            self.terminate(1)


    def messageSystem(self):
        try:
            while self.check_connection():
# Start of Sending Status Below
                if self.status:
                    myMessage = input("Enter your message: ")
                    if self.check_connection():
                        if myMessage == '\n' or myMessage == '':
                            print('Start again and please try to input something')
                            return
                        self.server['message'] = str(myMessage)
                        loading = ""
                        while self.server['received'].decode().strip() == '0':
                            time.sleep(1)
                        print("\nSent")
                        print(" ")
                        self.server['received'] = b'0'
                        self.status = False
                    else:
                        self.terminate("Connection with user ended. Closing connection to server.")
# End here
                
# Start of Waiting Status Below
                else:
                    while self.server['message'].decode().strip() == '':
                        if self.check_connection():
                            print("Wait for a message", end='\r')
                    if self.check_connection():
                        print(f"You have received a message: {self.server['message'].decode().strip()}")
                        self.server['received'] = b'1'
                        self.server['message'] = b''
                        self.status = True
                        time.sleep(1)
                    print("\n")
# End here            
            if self.server['conn'].decode().strip() == 'closing':
                self.terminate("Other user left the conversation.")
            time.sleep(1)

        except KeyboardInterrupt:
            self.terminate(1)


    def check_connection(self):
        return self.server['conn'].decode().strip() == 'connected'

        
    def terminate(self, e=0):
        if self.server['conn'].decode().strip() == 'connected':
            self.server.clear()
            self.server['conn'] = b'closing'
            sys.exit()

        if self.server['conn'].decode().strip() == 'closing':
            self.server.clear()
            self.server['conn'] = b'0'
            sys.exit()

        else:
            print()
            self.server.clear()
            self.server['conn'] = b'0'
            sys.exit(e)

client = Client()
client.connection()
client.messageSystem()
