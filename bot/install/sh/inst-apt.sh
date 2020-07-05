sudo apt-get update -y
sudo apt-get upgrade -y
dependencies=(
    "python3.7"
    "python3-pip"
    "python3.7-dev"
    "ffmpeg"
    "lm-sensors"
    "libreoffice"
    "sysstat"
    "git"
)
for dependency in "${dependencies[@]}"
do
    echo -e "\e[92mInstalling $dependency\e[0m"
    sudo apt-get install $dependency -y
done
