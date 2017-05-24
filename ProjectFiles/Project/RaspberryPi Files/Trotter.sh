#!/bin/bash
# Make script executable: chmod +x Trotter.sh
# Run script & use options below: ./Trotter.sh
# 't' Launch full Trotter services
# 'v' Voice Interface & GUI
# 'g' Gesture Interface
# 'p' Projection Globe
# 'q' Terminate all Trotter services
# 'e' Exit Trotter launcher
# 'n' ngrok: Secure tunnels to localhost


function banner {
	clear
	echo -e "\n "
	echo "_/_/_/_/_/  _/_/_/      _/_/    _/_/_/_/_/  _/_/_/_/_/  _/_/_/_/  _/_/_/    "
	echo "   _/      _/    _/  _/    _/      _/          _/      _/        _/    _/   "
	echo "  _/      _/_/_/    _/    _/      _/          _/      _/_/_/    _/_/_/  "
	echo " _/      _/    _/  _/    _/      _/          _/      _/        _/    _/  "
	echo "_/      _/    _/    _/_/        _/          _/      _/_/_/_/  _/    _/  "
}


function terminate {
	kill $(ps aux | grep '[c]hromium-browser' | awk '{print $2}')
	#kill $(ps aux | grep '[f]irefox-esr' | awk '{print $2}')
	kill $(ps aux | grep '[p]ython GlobeVUI/GlobeVUI.py' | awk '{print $2}')
	kill $(ps aux | grep '[p]ython Gesture/UserDetection.py' | awk '{print $2}')
	kill $(ps aux | grep '[G]esture/GestInput' | awk '{print $2}')
	kill $(ps aux | grep '[p]ython Rotation/rotation.py' | awk '{print $2}')
	kill $(ps aux | grep '[p]ython Rotation/server.py' | awk '{print $2}')
	echo -e "\n ** Terminated all Trotter processes **"
}


function trotter {
	terminate
	# Chrome in fullscreen
	#/usr/bin/chromium-browser --kiosk 127.0.0.1&
	/usr/bin/chromium-browser 127.0.0.1&
	python GlobeVUI/GlobeVUI.py&
	python Gesture/UserDetection.py&
	Gesture/GestInput&
	python Rotation/rotation.py&
	python Rotation/server.py&
	banner
	echo -e "\n ** Launching full Trotter service **"
}

# unused
function netset {
	net = ""
	read net < /globe/net.txt
	echo -e "$net"
}


function init {
	banner
	lxterminal --command "/home/pi/globe/ngrok start --all"&
	sleep 5s
	/home/pi/globe/Sendip.sh
	echo -e "\n ngrok launched \n Network configuration emailed"
}



# Startup code. Uncomment this block of code in final product
# Set working Dir to that of this script
cd "${0%/*}"
init
#trotter
echo -e "\n\n For help enter 'h'"



while true
do
	read -n 1 option
	if [[ "$option" == "t" ]]
	then
		terminate
		trotter
		echo -e "\n ** Launching full Trotter service **"
	elif [[ "$option" == "v" ]]
	then
		kill $(ps aux | grep '[c]hromium-browser' | awk '{print $2}')
		#kill $(ps aux | grep '[f]irefox-esr' | awk '{print $2}')
		kill $(ps aux | grep '[p]ython GlobeVUI/GlobeVUI.py' | awk '{print $2}')
		python GlobeVUI/GlobeVUI.py&
		/usr/bin/chromium-browser 127.0.0.1/map.html&
		#firefox-esr&
		banner
		echo -e "\n ** Starting Voice Interface & GUI **"
	elif [[ "$option" == "g" ]]
	then
		kill $(ps aux | grep '[p]ython Gesture/UserDetection.py' | awk '{print $2}')
		kill $(ps aux | grep '[G]esture/GestInput' | awk '{print $2}')
		python Gesture/UserDetection.py&
		Gesture/GestInput&
		banner
		echo -e "\n ** Starting Gesture Interface **"
	elif [[ "$option" == "p" ]]
	then
		kill $(ps aux | grep '[p]ython Rotation/rotation.py' | awk '{print $2}')
		kill $(ps aux | grep '[p]ython Rotation/server.py' | awk '{print $2}')
		python Rotation/rotation.py&
		python Rotation/server.py&
		banner
		echo -e "\n ** Starting Projection Globe **"
	elif [[ "$option" == "n" ]]
	then
		init
	elif [[ "$option" == "q" ]]
	then
		terminate
		banner
	elif [[ "$option" == "e" ]]
	then
		terminate
		banner
		echo -e "\n ** Exiting Trotter service **"
		exit 0
	elif [[ "$option" == "h" ]]
	then
		banner
		echo -e "\n ** Trotter Help **"
		echo "To launch/reset a feature enter the corresponding letter:"
		echo "'n' ngrok: Secure tunnels to localhost"
		echo "'t' Launch full Trotter services"
		echo "'v' Voice Interface & GUI"
		echo "'g' Gesture Interface"
		echo "'p' Projection Globe"
		echo "'q' Terminate all Trotter services"
		echo "'e' Exit Trotter launcher"
	fi
done




		











