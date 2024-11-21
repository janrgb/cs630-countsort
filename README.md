# Parallel Vs. Threaded Countsort Tool

## Authors
- Harshita Gupta
- Janhavi Tatkare
- Janish Suneja

## Setup
- Ensure you have Python **v3.12.X** installed. Linux distributions usually come with it by default, so use `python --version` or `python3 --version` to check your Python version on command line. If on a Windows or Mac, you will need to download it.

- If you don't have the correct version, download it for Windows/Mac from [here](https://www.python.org/downloads/)

- For Debian-based Linux distributions, use:

    ```
    sudo apt update
    sudo apt upgrade python3
    python3 --version
    ```

- For RHEL-based Linux distributions, use:

    ```
    sudo dnf install python3
    ```

- Examine the `requirements.txt` file for all dependencies.

- If using Windows or Mac, use:

    ```
    pip3 install <package>
    ``` 
    or 
    
    ```
    pip install <package>
    ``` 
    to get any dependencies you do not have.

- If using Linux, `pip` may not work depending on distribution. If it does not, use the system package manager instead. For Ubuntu, this would be:
    ```
    sudo apt install python3-<package>
    ```
    
    or 
    
    ```
    sudo apt install python-<package>
    ```

## Running

- Once every dependency is met, running the program is as easy as doing `python countsortgui.py` in the directory where `countsortgui.py` is located.