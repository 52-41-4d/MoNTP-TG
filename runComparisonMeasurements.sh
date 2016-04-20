# sudo python realTimeWiFiMonitor.py & python realTimeNTPMonitor.py

name="run1_7385-6"
sudo python realTimeWiFiMonitor.py > wifiOutput_${name}.txt & python realTimeNTPMonitor.py > ntpOutput_${name}.txt
join -t , -1 1 -2 1 -a 1 wifiOutput_${name}.txt ntpOutput_${name}.txt > runOutput_${name}.txt
python plotOutput.py ${name}
