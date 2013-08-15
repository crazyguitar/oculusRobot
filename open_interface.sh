#!/bin/bash
# open csitool interface
cd ~/linux-80211n-csitool-supplementary/injection
./setup_monitor_csi.sh 64 HT20
startOrNot=`service network-manager status| grep stop`
if [ ${#startOrNot} == 0 ];then
	sudo service network-manager stop
fi
sudo ifconfig wlan0 down

# open oculus server
cd /var/www/Oculus
sudo ./oculus_start.sh
