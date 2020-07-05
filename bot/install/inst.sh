echo "Please enter your password to download PRIZM ;]"
sudo echo "Thanks!"
echo
echo -e "\e[1;34m#] NOTICE\e[0m"
echo -e "\e[96mThis will take a while, go do something else\e[0m"
echo
sleep 3


# Package installers

cd ./sh
{
    apt > /dev/null 2>&1
    echo -e "\e[1;92mInstalling with APT\e[0m"
    name="./inst-apt.sh"
} || {
    dnf > /dev/null 2>&1
    echo -e "\e[1;92mInstalling with DNF\e[0m"
    name="./inst-dnf.sh"
} || {
    yum > /dev/null 2>&1
    echo -e "\e[1;92mInstalling with YUM\e[0m"
    name="./inst-yum.sh"
} || {
    rpm > /dev/null 2>&1
    echo -e "\e[1;92mInstalling with RPM\e[0m"
    name="./inst-rpm.sh"
} || {
    zypper > /dev/null 2>&1
    echo -e "\e[1;92mInstalling with ZYPPER\e[0m"
    name="./inst-zyp.sh"
} || {
    pacman > /dev/null 2>&1
    echo -e "\e[1;92mInstalling with PACMAN\e[0m"
    name="./inst-pac.sh"
} || {
    emerge > /dev/null 2>&1
    echo -e "\e[1;92mInstalling with PORTAGE\e[0m"
    name="./inst-port.sh"
} || {
    snap > /dev/null 2>&1
    echo -e "\e[1;92mInstalling with SNAP\e[0m"
    name="./inst-snap.sh"
} || {
    echo -e "\e[1;91m#] ERROR\e[0m"
    echo -e "\e[31mYour system doesn't have any supported package managers.\e[0m"
    echo -e "\e[31mPRIZM cannot be installed ;[\e[0m"
    cd ..
    exit 1
}

chmod +x $name
$name
sudo sensors-detect --auto
echo -e "\e[1;92mDone installing apps\e[0m"

#Python things

cd ../py

echo -e "\e[1;34m#] INFO\e[0m"
echo -e "\e[96mInstalling python dependencies\e[0m"
python3.7 -m pip install -r req.txt

echo -e "\e[1;34m#] INFO\e[0m"
echo -e "\e[96mUpdating PRIZM to suit your computer...\e[0m"
python3.7 change_dir.py

echo -e "\e[1;34m#] INFO\e[0m"
echo -e "\e[96mAdding styles for graphing...\e[0m"
python3.7 mpl_style.py

echo
echo -e "\e[1;96mNow we need some input\e[0m"
python3.7 get_info.py
cd ..

#Ending screen

echo
echo -e "\e[1;34m#] CONGRATS ;]\e[0m"
echo -e "\e[96mPRIZM has successfully been installed!\e[0m"
echo
echo -e "\e[1;91m#] NOTICE\e[0m"
echo -e "\e[31mPlease note that any GIT integrations such as the shortlink service\e[0m"
echo -e "\e[31mor the converter file uploader will NOT work unless you set those up\e[0m"
echo -e "\e[31myourself. They require a username and password for my GitHub account,\e[0m"
echo -e "\e[31mand you aren't going to get them any time soon.\e[0m"
