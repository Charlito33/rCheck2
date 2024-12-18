#!/bin/bash
sudo rm -f /tmp/rcheck2.zip
sudo rm -rf /tmp/rcheck2
sudo rm -rf /usr/share/rcheck2
sudo wget -O /tmp/rcheck2.zip https://github.com/Charlito33/rCheck2/archive/refs/heads/master.zip
sudo unzip /tmp/rcheck2.zip -d /tmp/rcheck2
sudo mv /tmp/rcheck2/rCheck2-master /usr/share/rcheck2
sudo rm -rf /tmp/rcheck2
echo "#!/bin/bash" | sudo tee /usr/bin/rcheck
echo "/usr/share/rcheck2/rcheck2 \"\$@\"" | sudo tee -a /usr/bin/rcheck
sudo chmod 755 /usr/bin/rcheck
echo -e "\e[92mrCheck2 installed in /usr/bin/rcheck.\e[0m"
echo -e "\e[92mUse it with : rcheck <program path> (rules path).\e[0m"
