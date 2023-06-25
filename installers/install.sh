mkdir betterlectio_temp
cd betterlectio_temp

sudo rm -rf /usr/share/betterlectio/
wget https://github.com/BetterLectio/desktop/releases/download/0.0.1/betterlectio-linux.zip
sudo unzip betterlectio-linux.zip -d /usr/share/betterlectio/

sudo mkdir /usr/share/app-logos/
wget https://raw.githubusercontent.com/BetterLectio/betterLectio/main/static/favicon.png --output-document=betterlectio.png
sudo mv betterlectio.png /usr/share/app-logos/

wget https://raw.githubusercontent.com/BetterLectio/desktop/main/installers/betterlectio.desktop
sudo mv betterlectio.desktop /usr/share/applications/

cd ..
sudo rm -rf betterlectio_temp
