![1](/esp32-esp8266/bcd%20clock/project%20images/20241222_091254.jpg)

# BCD-Clock <br>
Code for a Binary Coded Decimal Clock that gets TimeData via DCF OR NTP for an ESP32 (should also work with an ESP8266). <br>
## Hardware used: <br>
1 - ESP32 <br>
1 - DCF1 Receiver <br>
20 - WS2812 compatible LEDs <br>
7 - Standard LEDs<br> <br>
<br>
Note: While it works with an USB-Cable plugged into a computer/raspberry/laptop keep in mind: more LED = more power needed <br>
### notes on main.py <br>
Don't use this one if you want a pure NTP or a pure DCF solution. Until i can fix my local problem with the receiving of the DCF signal it uses 
NTP a a method of getting the current time. It still contains code for DCF-Receving. It's a garbled mess at the moment but still works nonetheless. <br>
### content of this repo
\- DCF-Version folder
\-- DCF_BCD.py
\-- dcf2rtc.py
\-- boot.py
\- NTP-Version folder
\-- NTP_BCD.py
\-- boot.py
\- Test-Version
\- main.py
\- boot.py
\- dcf2rtc.py
<br>
### Usage: <br>
**WLAN:** <br>
IF you are using NTP edit the NTP_BCD.py to contain your WIFI SSID and Password! <br>
Those can be found on line 9 and line 10 in the file. <br>
<br> <br>
**Upload** ALL the contents from your chosen folder. <br>
<br>
**Finally:** <br>
Reconnect your Clock to the power source of your liking.<br>

**Notes:** <br>
It should be noted that receiving a valid DCF77 Signal is an arduous task at best. It does not magicall work better if you put the recevier near a window. There is a reason why i wrote and included the NTP Version.
