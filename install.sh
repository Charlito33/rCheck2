#!/bin/bash
sudo rm -f /tmp/rcheck2.zip
sudo rm -rf /tmp/rcheck2
if [ -d /usr/share/rcheck2 ]
then
  read -n 1 -p "A previous version of rCheck2 is installed on this system, do you want to remove it? [Y/n] " -r
  if [[ "$REPLY" != "" ]]
  then
    echo ""
  fi
  if [[ "$REPLY" != "" ]] && [[ ! "$REPLY" =~ ^[Yy]$ ]]
  then
    echo "Terminating installer."
    exit
  fi
  sudo rm -rf /usr/share/rcheck2
  echo "Removed installed rCheck."
fi
echo "Downloading rCheck2 from GitHub..."
sudo wget -q -O /tmp/rcheck2.zip https://github.com/Charlito33/rCheck2/archive/refs/heads/master.zip
sudo unzip /tmp/rcheck2.zip -d /tmp/rcheck2 >> /dev/null
sudo mv /tmp/rcheck2/rCheck2-master /usr/share/rcheck2
sudo rm -rf /tmp/rcheck2
echo "#!/bin/bash" | sudo tee /usr/bin/rcheck >> /dev/null
echo "/usr/share/rcheck2/rcheck2 \"\$@\"" | sudo tee -a /usr/bin/rcheck >> /dev/null
sudo chmod 755 /usr/bin/rcheck
echo ""
echo -e "\e[92mrCheck2 installed in /usr/bin/rcheck.\e[0m"
echo -e "\e[92mUse it with : rcheck [target path] [configuration path].\e[0m"
