sudo rm -rf /usr/share/betterlectio/
sudo unzip betterlectio-linux.zip -d /usr/share/betterlectio/

sudo mkdir /usr/share/app-logos/
wget https://raw.githubusercontent.com/BetterLectio/betterLectio/main/static/favicon.png --output-document=betterlectio.png
sudo mv betterlectio.png /usr/share/app-logos/

#wget https://raw.githubusercontent.com/BetterLectio/betterLectio/dev/buildData/betterlectio.desktop
sudo mv betterlectio.desktop /usr/share/applications/