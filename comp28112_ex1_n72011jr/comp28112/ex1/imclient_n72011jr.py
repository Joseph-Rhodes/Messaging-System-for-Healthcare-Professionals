import time 
import im  
import sys  

class Client:
    
    def __init__(self):
        # Initialize status attribute
        self.status = None
        # Initialize message attribute 
        self.message = ''  
        # Initialize client attribute with the 'IMServerProxy' instance
        self.client = im.IMServerProxy('https://web.cs.manchester.ac.uk/n72011jr/comp28112_ex1/IMserver.php') 
    
    
    def connection(self):
        try:
            if len(self.client.keys()) == 1:
                self.client['connection'] = '0'  # Sets connection to '0' so no one is connected
            elif self.client['connection'].decode().strip() == 'terminate':
                self.client.clear()  
                self.client['connection'] = '0'  # Sets connection to '0' meaning no one is connected
            if self.client['connection'].decode().strip() == '0':
                self.status = True  # Sets the client to the sending status
                self.client['connection'] = b'1'  # Set connection to b'1' menaing one client is connected
            elif self.client['connection'].decode().strip() == '1':
                self.status = False  # Sets the client to the waiting status
                self.client['connection'] = b'2'  # Sets connection to b'2' meaning that a connection is established
            elif self.client['connection'].decode().strip() == '2':
                print("Server is full")  
                sys.exit()  
            else:
                self.terminate("Error",1)  

            count = 0  
            printed_message = False  
            # Loop until connection is '2'
            while self.client['connection'].decode().strip() != '2':
                
                if not printed_message:
                    print(" ")
                    print("Searching for another client...")
                    printed_message = True
                count += 1 
                # Waits 15 seconds for second client to connect if not then first client is kicked 
                if count >= 15:  
                    self.terminate("Second client not found.",1)  
                time.sleep(1) 

            print("  ")  
            self.client['received'] = b'0' 
            self.client['message'] = b''  

        except KeyboardInterrupt:
            self.terminate(1)  


    def messageSystem(self):
        try:
            while self.check_connection():
                # If client status is in the sending status
                if self.status:
                    # Takes the input from the sending status client
                    myMessage = input("Enter your message: ")  
                    # While the connection is active
                    if self.check_connection():
                        if myMessage == '\n' or myMessage == '':  
                            print('Start again and please try to input something')  
                            return
                        self.client['message'] = str(myMessage) 
                        # loading = ""  
                        # Wait until message is received
                        while self.client['received'].decode().strip() == '0':
                            time.sleep(1)
                        print("\nSent")  
                        print(" ")  
                        self.client['received'] = b'0'  
                        self.status = False  # Changes client from sending to waiting status
                    else:
                        self.terminate("Connection has been terminated",1)  
                else:
                    # Waiting for a message
                    while self.client['message'].decode().strip() == '':
                        if self.check_connection():
                            print("Wait for a message", end='\r')  
                    if self.check_connection():
                        # Prints the received message
                        print(f"You have received a message: {self.client['message'].decode().strip()}")  
                        self.client['received'] = b'1'  
                        self.client['message'] = b''  
                        self.status = True  # Changes client from waiting to sending status
                        time.sleep(1) 
                    print("\n")  

            if self.client['connection'].decode().strip() == 'closed':
                self.terminate("Other client has left.",1)  
            time.sleep(1)  

        except KeyboardInterrupt:
            self.terminate("Connection Terminated",1)  


    def check_connection(self):
        # Check if connection is active
        return self.client['connection'].decode().strip() == '2'

        
    def terminate(self,m, e=0):
        # If connection is closed
        if self.client['connection'].decode().strip() == '2':
            self.client.clear()  
            self.client['connection'] = b'closed'  
            sys.exit()  
        if self.client['connection'].decode().strip() == 'closed':
            self.client.clear()  
            self.client['connection'] = b'0'  
            sys.exit()  
        else:
            print()  
            self.client.clear()  
            self.client['connection'] = b'0'  
            sys.exit(e)  

# Below creates an instance of the client class and establish a connection to the server
client = Client()
client.connection()  
client.messageSystem() 
