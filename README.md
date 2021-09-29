# a simple script to display information on the rpi

This script displays the following infos:
1. external IP
2. private IP
3. date and time
4. CPU temperature
5. CPU load


For the external IP, the python script reads the data from a file. This file has been created by a simple bash script:
''' curl https://ip.me > externalIP.txt'''

That's it. 


