#!/bin/sh
# Sends Trotter network & ngrok settings to email

SUBJ="Trotter"
EMAIL="trotters490@gmail.com"


#Pub = $(wget -qO- ifconfig.me/ip)
#Lan = $(ifconfig wlan0 | grep 'inet addr' | awk '{ print $2 }')
#ngrokSSH = $(curl http://localhost:4040/api/tunnels | jq '.tunnels[0].public_url')
#ngrokWeb = $(curl http://localhost:4040/api/tunnels | jq '.tunnels[2].public_url')

# Email network settings
sudo echo -e " Public IP:\n $(curl -s https://api.ipify.org) \n\n LAN IP: \n $(ifconfig wlan0 | grep 'inet addr' | awk '{ print $2 }') \n\n NGROK: \n SSH: $(curl http://localhost:4040/api/tunnels | jq '.tunnels[0].public_url') \n Web: $(curl http://localhost:4040/api/tunnels | jq '.tunnels[2].public_url')" | mail -s $SUBJ $EMAIL &

sleep 5s
# Print network settings
# \e[15A moves cursor up 15 lines.  \r\e[0K   clears the
sudo echo -en "\e[12A \r\e[0K\n\r\e[0K\n\r\e[0K Public IP: \n\r\e[0K $(curl -s https://api.ipify.org) \n\r\e[0K\n\r\e[0K LAN IP: \n\r\e[0K $(ifconfig wlan0 | grep 'inet addr' | awk '{ print $2 }') \n\r\e[0K\n\r\e[0K NGROK: \n\r\e[0K SSH: $(curl http://localhost:4040/api/tunnels | jq '.tunnels[0].public_url') \n\r\e[0K Web: $(curl http://localhost:4040/api/tunnels | jq '.tunnels[2].public_url')"
# clear 5 past terminal lines and move cursor back up 6 lines
sudo echo -en "\n\r\e[0K\n\r\e[0K\n\r\e[0K\n\r\e[0K\n\r\e[0K\n\r\e[0K \e[5A"



exit

