# Fritz-Discord-Bot
Using Fritz's API to read traffic information from AVM FritzBOX Routers and connect this with a Discord bot posting and updating the the message.

<br> 
Tested on a Fritz.Box 7590
Fritz!OS: 7.57

In order to access the API you need to activate UPnP and Allow App Access TR-064.


Documentation Fritz API

https://fritzconnection.readthedocs.io/en/1.4.2/sources/api.html

## Configure
<br>

Create a Discord bot: https://discord.com/developers/applications
<br>
Insert your Router Password.
<br>
Copy the Bot-Token and paste it at Token = 'CHANGE_ME'
<br>
Change the presence status to whatever you want

## Run

Open Terminal

python3 fritzapi.py


Command to activate the bot /bandwidth


<div align="center">
<a href="https://i.gyazo.com/49daf60f36fae1d7307c7d8f9656facb.png">
<img src="https://i.gyazo.com/49daf60f36fae1d7307c7d8f9656facb.png" />
</a>
</div>

## Pterodactyl Egg

Import the pterodactyl Egg
Upload requirements.txt and the skript to the main folder
