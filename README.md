# Intro to Embedded Linux Development and Edge AI
A workshop to teach student embedded developers how to set up a SBC with linux, the basics of the command line and running OpenCV.

      ____     .--.               _____ 
     | !? |   |o_o |             < OOM >
      `--'    |:_/ |              ----- 
        \    //   \ \                 \   ^__^
            (|     | )                 \  (oo)\_______
           /'\_   _/` \                   (__)\       )\/\
           \___)=(___/                        ||----w |
                                              ||     ||

## Part 1: Booting Up the Edge

### What is a Raspberry Pi and Edge AI?
A Raspberry Pi is a Single Board Computer (SBC)—an entire, fully functioning computer packed onto a board the size of a credit card. It runs an embedded Linux operating system. Embedded Linux is the hidden engine of the modern world, powering everything from smart thermostats to the entertainment screens on airplanes.

Traditionally, AI requires massive, centralized servers in giant data centers. But what if a drone needs to navigate a forest without internet access? That's where **Edge AI** comes in. By running AI models directly on the "edge" of the network (on the device itself), we reduce latency, increase privacy, and save bandwidth. 

**Learning Objectives:**
1. Provision and remotely access a headless embedded Linux system.
2. Learn fundamental command-line interface (CLI) navigation and scripting.
3. Establish a modern Python virtual environment to run an OpenCV computer vision pipeline.

### Step 1: Create a Raspberry Pi Connect Account
Later on, we will need to see the graphical output of our computer vision scripts. Go to [connect.raspberrypi.com](https://connect.raspberrypi.com/) and create a free account. Keep your login details handy.

### Step 2: Flashing the OS
1. Insert your micro SD card into your computer.
2. Open the **Raspberry Pi Imager**.
3. Select the recommended **Raspberry Pi OS (64-bit)** (Full desktop version).
4. Select your SD card as the storage.
5. **CRUCIAL STEP:** Before clicking write, edit the OS Customization settings!
   * Set a hostname.
   * Set a username and password (write these down!).
   * Configure your Wi-Fi (if not using ethernet).
   * Go to the Services tab and **Enable SSH** (use password authentication).
   * Go to the Options tab and enable Raspberry Pi Connect.
6. Write the image to the SD card.

### Step 3: Finding Your Pi on the Network
Before GUIs (Graphical User Interfaces) with mice and windows existed, humans interacted with computers using a **terminal**—a text-based interface where you type commands directly to the operating system. We are going to use a terminal to find our Pi.

1. Open **Command Prompt** (Windows) or **Terminal** (Mac).
2. Run this command to see a list of all IP addresses currently on your local network:
   `arp -a`
3. Physically put the micro SD card into the Raspberry Pi. Plug in the Ethernet cable, and finally, plug in the power. 
4. Wait about 2-3 minutes for the Pi to boot up.
5. Run `arp -a` again. Compare the new list to the old list. The new IP address that appeared is your Raspberry Pi!
   * *Fallback:* If this doesn't work, log into Raspberry Pi Connect in your browser, open the remote terminal, and type `ifconfig` to find the `inet` IP address under your network adapter.

### Step 4: Connecting via SSH
We need that IP address to **SSH** into the Pi. Secure Shell (SSH) is a network protocol that gives you a secure, encrypted way to access a computer over an unsecured network. It drops you into a **shell**—a program that takes your keyboard commands and passes them to the operating system to execute.

Run this command, replacing `username` with your chosen username and `ip_address` with the IP you found:
`ssh username@ip_address`

Type `yes` to accept the fingerprint, and enter your password.

### Step 5: The First Command
You are now inside your Raspberry Pi! You are currently sitting in your **home directory** (`~`), your personal workspace. Let's update the system. Run:
`sudo apt-get update && sudo apt-get upgrade -y`

* **`apt-get`**: This is the Advanced Package Tool, Linux's built-in app store/package manager.
* **`sudo`**: "Superuser Do". It temporarily gives you administrative (root) privileges to install things safely.

---

## Part 2: Taming the Command Line

### Step 1: Installing a Superpower (Vim)
Before we start making files, let's install a better text editor. We will use `apt-get` to install programs in Debian-based Linux operating systems like Raspberry Pi OS. 

Run this command:
`sudo apt-get install vim -y`

*What is Vim?* It is an upgraded version of `vi`, one of the oldest text editors which, along with `nano`, comes preinstalled on almost all Linux distributions. Vim is notoriously a bit esoteric and relies heavily on keyboard commands instead of a mouse. However, once you get the hang of it, it becomes an absolute superpower for swiftly editing files on headless servers. Today will give you a small taste of that!

### Step 2: Setting up the Workspace
Create a development folder and clone our workshop repository:
`mkdir dev`
`cd dev`
`git clone https://github.com/bevis-hp/Intro-to-Embedded-Linux-Development-and-Edge-AI`

Go back to your home folder (`cd ~`) and create a folder for binary executables:
`cd ~`
`mkdir bin`

### Step 3: The Mystery Script
Move the bash script from the workshop folder into your new `bin` folder (`cp` copies files):
`cp ~/dev/Intro-to-Embedded-Linux-Development-and-Edge-AI/mystery_script.sh ~/bin/`

Right now, it's just a text file. We need to make it an executable program using **`chmod`** (Change Mode):
`cd ~/bin`
`chmod +x mystery_script.sh`

Run it! Notice we use `./` to tell the computer "run the file in *this exact folder*":
`./mystery_script.sh`

It prints an ASCII cat and asks for a text file. Let's rename the script using **`mv`** (Move/Rename):
`mv mystery_script.sh devcat`

### Step 4: Modifying the PATH
We want `devcat` to run from anywhere, without needing the `./`. We do this by adding our `bin` folder to the system's `$PATH`.
1. Open your bash configuration file with the **`vim`** text editor:
   `vim ~/.bashrc`
2. Press `G` (capital G) to jump to the bottom of the file.
3. Press `o` (lowercase o) to open a new line and enter "Insert Mode".
4. Type exactly: `export PATH="$HOME/bin:$PATH"`
5. Press `Esc` to exit Insert Mode.
6. Type `:wq` and hit `Enter` to write the file and quit.

Reload the configuration using **`source`** and verify it with **`echo`**:
`source ~/.bashrc`
`echo $PATH`
You should see `home/<your-username>/bin` in the list displayed if you have done this correctly.

### Step 5: Testing DevCat
Go to your home directory (`cd ~`). Let's create an empty text file using **`touch`**:
`touch test.txt`

Open it with `vim test.txt`, press `i` to insert text, write a sentence, press `Esc`, and type `:wq` to save. 

Now, run your command from anywhere!
`devcat test.txt`

Check the file again with `cat test.txt`. The original text is gone, replaced entirely by cat language!

*(Finished early? Check out [The Command Line Murders](https://github.com/veltman/clmystery) to practice your new detective CLI skills!)*

---

## Part 3: Edge AI with OpenCV

Now we transition from text to images. Because we are working with visual media, we need a desktop environment. 

1. Go back to [connect.raspberrypi.com](https://connect.raspberrypi.com/).
2. Connect to your Raspberry Pi using the **Screen Sharing** (Desktop) option.
3. Open the Terminal app inside the desktop GUI.

### Step 1: Python and Virtual Environments
When developing in Python, it's best practice to use **Virtual Environments**. This creates an isolated bubble for your project, preventing different Python projects from messing up each other's libraries. We will use a lightning-fast modern tool called `uv`.

Install `uv` using **`curl`** (a command that downloads data from a server and pipes it to an execution shell):
`curl -LsSf https://astral.sh/uv/install.sh | sh`
`source $HOME/.local/bin/env`

### Step 2: Setting up OpenCV
Navigate to your dev folder, create a project folder, and create the virtual environment:
`cd ~/dev`
`mkdir opencv_testing`
`cd opencv_testing`
`uv venv`

Activate the environment and install OpenCV:
`source .venv/bin/activate`
`uv pip install opencv-python numpy`

### Step 3: Preparing the Assets
Copy the Python script from the workshop repo to your current folder:
`cp ~/dev/workshop_repo/sobel_edge.py .`

Now, let's download an image from the internet using `curl` and output (`-o`) it as `test_image.jpg`:
`curl -o test_image.jpg https://raw.githubusercontent.com/opencv/opencv/master/samples/data/ml.png`

Open the Python script with `vim sobel_edge.py` and ensure the `target_image` variable matches the file you just downloaded (`test_image.jpg`).

### Step 4: Run the Filter
Run your python script:
`python sobel_edge.py`

A window should pop up showing the original image alongside a mathematically transformed image highlighting all the edges! This Sobel filter is foundational to how computers "see" shapes.

**Next Steps:** With this environment set up, you are ready to plug in a USB camera, capture a live video feed, and pass those frames into an object recognition neural network like YOLO (You Only Look Once) to track real-world items in real-time!
