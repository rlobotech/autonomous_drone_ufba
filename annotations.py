## Conect to raspberry
ssh pi@192.168.1.2
## Password
raspberry 

## Check gps satelittes
cgps -s

##### ETC
*Note: Each time the files are changed the application restarts automatically*

## Contribution guidelines ##

**Variables, functions and files-> all in lowercase and/or separated by underline:**

* drone
* drone_new()
* drone_edit.html

**Classes -> Initial capital letter for each word:**

* Drone()
* DroneEdit()

*Note: Everything in English*


# Usar o GitKraken como software de versionamento e o sublime 3 como IDE, baixando o plugin do flask.

##### End ETC

#This example runs a few commands on a remote server and prints the result. 

#First we import the modules that we need. (pxssh and getpass)

#We import the getpass module, which will prompt the user for a password,
#without echoing what they type to the console.

import pxssh
import getpass
try:                                                            
    s = pxssh.pxssh()
    hostname = raw_input('hostname: ')
    username = raw_input('username: ')
    password = getpass.getpass('password: ')
    s.login (hostname, username, password)
    s.sendline ('uptime')   # run a command
    s.prompt()             # match the prompt
    print s.before          # print everything before the prompt.
    s.sendline ('ls -l')
    s.prompt()
    print s.before
    s.sendline ('df')
    s.prompt()
    print s.before
    s.logout()
except pxssh.ExceptionPxssh, e:
    print "pxssh failed on login."
    print str(e)

#Run a command on a remote SSH server
#Let's show one more example. To run a command ('uptime') and to print the output, 
#you need to do something like that :

import pxssh
s = pxssh.pxssh()
if not s.login ('localhost', 'myusername', 'mypassword'):
    print "SSH session failed on login."
    print str(s)
else:
    print "SSH session login successful"
    s.sendline ('uptime')
    s.prompt()         # match the prompt
    print s.before     # print everything before the prompt.
    s.logout()
    
#We can also execute multiple command like this:
s.sendline ('uptime;df -h')
