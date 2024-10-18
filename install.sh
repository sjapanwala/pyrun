#!/bin/bash
TARGET_PATH="/usr/local/bin/py"
PYTHON_SCRIPT_URL="https://raw.githubusercontent.com/sjapanwala/pyrun/refs/heads/main/pyrun.py"

if [ -e "$TARGET_PATH" ]; then
    echo -e "\033[91mPyrun is already installed.\033[0m"
    read -p "Do you want to Remove Installation? (y/n): " answer
    if [[ "$answer" =~ ^[Yy]$ ]]; then
        sudo rm "$TARGET_PATH"
        if [ $? -eq 0 ]; then
            echo -e "\033[32mInstallation Removed\033[0m"
            exit
        else
            echo -e "\033[91mRemoval Failed\033[0m"
            exit 1
        fi
    else
        echo -e "\033[91mInstallation Aborted\033[0m"
        exit 1
    fi
fi

# Checking for python installation
if ! command -v python3 &> /dev/null; then
    echo -e "\033[31mPython3 is not installed.\033[0m"
    echo -e "\033[90mC'mon, didn't you read that Python was part of the app?\033[0m"
    echo -e "\nWindows: winget install python3\nHomeBrew: brew install python3\nAPT: sudo apt install python3\nPacman: sudo pacman -S python3\nYum: sudo yum install python3\nZypper: sudo zypper install python3\nApk: sudo apk add python3\n"
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo -e "\033[31mpip3 is not installed.\033[0m"
    echo -e "\033[90mHow do you have Python but not pip3?...\033[0m"
    exit 1
fi

package="pygments"
# Use python to check if the package can be imported
python3 -c "import $package" 2>/dev/null

# Check if the command was successful
if [ $? -eq 0 ]; then
    echo -e "Welcome To Pyrun Installer, Please Read Through The Installation Process\n\n1. Download The App\n2. Add It To /usr/local/bin/py (this will make it usable)\n3. Install Dependencies\n4. Done!\n\033[90mSudo Access Is Required\033[0m\n"
    read -p "Do you want to continue? (y/n): " answer
    # Checking the user's input
    if ! [[ "$answer" =~ ^[Yy]$ ]]; then
        echo -e "\033[91mInstallation Aborted\033[0m"
        exit 1
    else
        sudo curl -s -o "$TARGET_PATH" "$PYTHON_SCRIPT_URL"
        sudo chmod +x "$TARGET_PATH"
        if [[ -f "$TARGET_PATH" ]]; then
            echo -e "\033[32mInstallation successful! You can now run your script using 'py' from anywhere.\033[0m"
            echo -e "\033[37mTo Run Update, Run \033[92m'py --new'\033[0m"
            echo -e "\033[37mTo Run Help, Run \033[92m'py --help'\033[0m"
            echo -e "\033[37mTo Uninstall, Run This Script Again\033[0m"
        else
            echo -e "\033[91mInstallation failed.\033[0m"
            exit 1
        fi
    fi
else
    counter=0
    echo -e "\033[37mInstalling Dependencies...\033[0m"
    pip3 install pygments 2>/dev/null
    python3 -c "import pygments" 2>/dev/null 
    if ! [ $? -eq 0 ]; then
        counter=$((counter + 1))
    else
        echo -e "\033[31mError Occurred!\033[0m"
        echo -e "\033[33mForce Install?\033[0m"
        read -p "Do you want to continue? (force installing can possibly break the script and your Python installation) (y/n): " answer
        if [[ "$answer" =~ ^[Yy]$ ]]; then
            pip3 install pygments --break-system-packages
            python3 -c "import pygments" 2>/dev/null 
            if [ $? -eq 0 ]; then
                counter=$((counter + 1))
                echo -e "\033[32m$counter Dependencies Installed\033[0m"
            else
                echo -e "\033[91mError Occurred!... This time IDK what happened\033[0m"
                exit 1
            fi
        else
            echo -e "\033[91mInstallation Aborted\033[0m"
            exit 1
        fi
    fi
    # Add more dependencies here
    echo -e "\033[32m$counter Dependencies Installed\033[0m"
fi
# cleanup
echo -e "\033[35mScript Finished\033[0m"
sudo rm install.sh