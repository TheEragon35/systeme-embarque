#!/bin/bash
#on enleve les mdp pour sudo
sudo echo -e "\n********** Cancel sudo **********\n" > .setup_log.txt
sudo echo -e "tim ALL=(ALL) NOPASSWD: ALL" | sudo EDITOR='tee -a' visudo >> .setup_log.txt

#on affiche l'esapce dispo avant suppression
taille=$(df -h /dev/mmcblk0p1) >> .setup_log.txt
echo -e "Espace disponible avant suppresion : $taille\n" >> .setup_log.txt


#on supprime les appils qui servent à rien
echo -e "\n********** Suppression des applications inutiles **********\n" >> .setup_log.txt
sudo apt-get purge libreoffice-* -y >> .setup_log.txt
sudo apt-get purge thunderbird* -y >> .setup_log.txt
sudo apt-get purge docker* -y >> .setup_log.txt

echo -e "\n*********** Suppression des paquets inutilisés **********\n" >> .setup_log.txt
#on supprime les paquets pas utilise
sudo apt-get autoremove -y >> .setup_log.txt

#On affiche l'esapce dispo apres suppression
echo "\nEspace disponible apres suppresion : $taille\n" >> .setup_log.txt 

#on maj les paquets et l'os
echo -e "\n*********** MAJ de l'os et des paquets **********\n" >> .setup_log.txt
sudo apt-get update -y && apt-get upgrade -y >> .setup_log.txt

#on installe les python build dependencies
echo -e "\n*********** Installation des paquets essentiels pour python **********\n" >> .setup_log.txt
sudo apt install build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev -y >> .setup_log.txt

#on installe git
echo -e "\n*********** Installation de Git **********\n" >> .setup_log.txt
sudo apt-get install git -y >> .setup_log.txt

#on installe pyenv
echo -e "\n*********** Installation de pyenv et du plugin virtualenv **********\n" >> .setup_log.txt
git clone https://github.com/pyenv/pyenv.git ~/.pyenv >> .setup_log.txt
cd ~/.pyenv && src/configure && make -C src >> .setup_log.txt

#on rajoute des commande necessaire au fonctionnement de pyenv dans le bashrc
echo -e "\n*********** Ajout des commandes au .bashrc **********\n" >> .setup_log.txt

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc

#idem pour profile
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
echo 'eval "$(pyenv init -)"' >> ~/.profile
source ~/.profile

#on installe le plugin pour les virtualenv de pyenv 
git clone https://github.com/pyenv/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv >> .setup_log.txt
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
source ~/.bashrc

#installation de codium
echo -e "\n*********** Installation de Codium **********\n" >> .setup_log.txt
wget -qO - https://gitlab.com/paulcarroty/vscodium-deb-rpm-repo/raw/master/pub.gpg \
    | gpg --dearmor \
    | sudo dd of=/usr/share/keyrings/vscodium-archive-keyring.gpg >> .setup_log.txt
echo 'deb [ signed-by=/usr/share/keyrings/vscodium-archive-keyring.gpg ] https://download.vscodium.com/debs vscodium main' \
    | sudo tee /etc/apt/sources.list.d/vscodium.list >> .setup_log.txt
sudo apt update && sudo apt install codium >> .setup_log.txt

#on met python 3.9.12
echo -e "\n*********** Installation de python 3.9.12 **********\n" >> .setup_log.txt
pyenv install 3.9.12 >> .setup_log.txt
pyenv global 3.9.12 >> .setup_log.txt

#maj du pip
echo -e "\n*********** MAJ du pip **********\n" >> .setup_log.txt
pip install --upgrade pip setuptools wheel

exec "$SHELL"

