# Intro to Embedded Linux Development, Computer Vision and Edge AI
A workshop to teach student embedded developers how to set up a SBC with linux, the basics of the command line and running OpenCV.

      ____     .--.               _____ 
     | !? |   |o_o |             < OOM >
      `--'    |:_/ |              ----- 
        \    //   \ \                 \   ^__^
            (|     | )                 \  (oo)\_______
           /'\_   _/` \                   (__)\       )\/\
           \___)=(___/                        ||----w |
                                              ||     ||

# Edge AI on the Raspberry Pi: From Headless Setup to Computer Vision

Welcome to the workshop! Today, we are going to transform a bare circuit board into an Edge AI device capable of seeing the world. 

## Part 1: Booting Up the Edge

### What is a Raspberry Pi and Edge AI?
A Raspberry Pi is a Single Board Computer (SBC)—an entire, fully functioning computer packed onto a board the size of a credit card. It runs an embedded Linux operating system. Embedded Linux is the hidden engine of the modern world, powering everything from smart thermostats to the entertainment screens on airplanes.

Traditionally, AI requires massive, centralized servers in giant data centers. But what if a drone needs to navigate a forest without internet access? That's where **Edge AI** comes in. By running AI models directly on the "edge" of the network (on the device itself), we reduce latency, increase privacy, and save bandwidth. 

**Learning Objectives:**
1. Provision and remotely access a headless embedded Linux system.
2. Master fundamental command-line interface (CLI) navigation and scripting.
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

Let's learn how to navigate. 
* **`mkdir`** (Make Directory): Creates a new folder.
* **`cd`** (Change Directory): Moves you into a folder.
* **`ls`** (List): Shows you what is inside your current folder.

### Step 1: Installing a Superpower (Vim)
Before we start making files, let's install a better text editor. We will use `apt-get` to install programs in Debian-based Linux operating systems like Raspberry Pi OS. 

Run this command:
`sudo apt-get install vim -y`

*What is Vim?* It is an upgraded version of `vi`, one of the oldest text editors which, along with `nano`, comes preinstalled on almost all Linux distributions. Vim is notoriously a bit esoteric and relies heavily on keyboard commands instead of a mouse. However, once you get the hang of it, it becomes an absolute superpower for swiftly editing files on headless servers. Today will give you a small taste of that!

### Step 2: Setting up the Workspace
Create a development folder and clone our workshop repository:
`mkdir dev`
`cd dev`
`git clone https://github.com/bevis-hp/Intro-to-Embedded-Linux-Development-Computer-Vision-and-Edge-AI.git`

Go back to your home folder (`cd ~`) and create a folder for binary executables:
`cd ~`
`mkdir bin`

### Step 3: The Mystery Script
Move the bash script from the workshop folder into your new `bin` folder (`cp` copies files):
`cp ~/dev/Intro-to-Embedded-Linux-Development-Computer-Vision-and-Edge-AI/mystery_script.sh ~/bin/`

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

### Step 5: Testing DevCat
Go to your home directory (`cd ~`). Let's create an empty text file using **`touch`**:
`touch test.txt`

Open it with `vim test.txt`, press `i` to insert text, write a sentence, press `Esc`, and type `:wq` to save. 

Now, run your command from anywhere!
`devcat test.txt`

Check the file again with `cat test.txt`. The original text is gone, replaced entirely by cat language! *(The **`cat`** command, short for "concatenate," is most commonly used to quickly read a file and print its contents directly to your terminal screen).*

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
`cp ~/dev/Intro-to-Embedded-Linux-Development-Computer-Vision-and-Edge-AI/sobel_edge.py .`

Now, let's download an image from the internet using `curl` and output (`-o`) it as `test_image.jpg`:
`curl -o test_image.jpg https://raw.githubusercontent.com/opencv/opencv/master/samples/data/ml.png`

Open the Python script with `vim sobel_edge.py` and ensure the `target_image` variable matches the file you just downloaded (`test_image.jpg`).

### Step 4: Run the Filter
Run your python script:
`python sobel_edge.py`


A window should pop up showing the original image alongside a mathematically transformed image highlighting all the edges! This Sobel filter is foundational to how computers "see" shapes.

---

## Part 4: Live Video with a USB Camera

Now that we can process static images, let's process real-time video using a standard USB webcam. 

### Step 1: Connect and Identify the Camera
Plug your USB web camera into one of the Raspberry Pi's USB ports. 

To use our camera, we need to find its hardware device ID. We will use `apt-get` to install a small utility package that helps list connected video devices. Run:
`sudo apt-get install v4l-utils -y`

Now, list all connected video devices:
`v4l2-ctl --list-devices`

You will see your camera's name (e.g., Logitech HD Pro Webcam) listed along with several `/dev/video` endpoints beneath it. Look for the very first `/dev/video` number listed under your camera's name (usually `/dev/video0`). That number (`0`) is your camera ID.

### Step 2: Preparing the Script
Ensure you are still in your `opencv_testing` directory and your virtual environment is active:
`cd ~/dev/opencv_testing`
`source .venv/bin/activate`

Copy the camera test script from our workshop repository to your current working directory:
`cp ~/dev/Intro-to-Embedded-Linux-Development-Computer-Vision-and-Edge-AI/usb_camera_test.py .`

Let's look inside the script using our text editor to see how it works:
`vim usb_camera_test.py`

Check the `camera_id` variable near the top of the file. If your camera ID from Step 1 was anything other than `0`, press `i` to enter Insert Mode, change the number, press `Esc`, and type `:wq` to save and quit. If it was `0`, you can just type `:q` to quit without saving.

### Step 3: Run the Live Feed
Execute your script:
`python usb_camera_test.py`

A new window should open on your Raspberry Pi desktop via Raspberry Pi Connect showing a live video feed from your webcam. Wave to the camera! When you are ready to stop the stream, make sure the video window is actively selected and press the `q` key on your keyboard to safely exit the script and close the window.

**Troubleshooting:**
* **Wrong Camera ID:** If the script fails to open the camera, change the `camera_id` variable in your script to `1` or `2` (trying the other `/dev/video` numbers listed in Step 1).
* **Low Voltage:** Webcams draw significant power. If a "Low voltage warning" appears on your desktop or the camera drops out, ensure you are using an official, properly rated Raspberry Pi power adapter.

---

## Part 5: Seeing the Edges in Real-Time

We have successfully processed a static image, and we have successfully streamed live video. Now, let's combine them. We are going to apply the Sobel edge detection filter to every single frame of our live video feed as it comes in. 

### Step 1: Preparing the Script
Ensure you are still in your `opencv_testing` directory and your virtual environment is active:
`cd ~/dev/opencv_testing`
`source .venv/bin/activate`

Copy the real-time edge detection script from our workshop repository:
`cp ~/dev/Intro-to-Embedded-Linux-Development-Computer-Vision-and-Edge-AI/live_sobel.py .`

### Step 2: Inspecting the Code
Let's open it up in Vim to see how we combined the two concepts:
`vim live_sobel.py`

Look closely at the `while True:` loop. You will see that instead of just displaying the frame, we are intercepting it, converting it to grayscale, doing the heavy Sobel math, and *then* displaying the newly generated edge frame. 

*(Note: If your camera ID was not `0` in the last part, press `i`, change the `camera_id` variable, press `Esc`, and type `:wq` to save and quit. Otherwise, just type `:q` to exit).*

### Step 3: Run the Edge Stream
Execute your script:
`python live_sobel.py`

You should now see two windows: your standard live feed, and a real-time feed consisting entirely of calculated edges! Move your hand in front of the camera and watch the math happen instantly. 

Press `q` on your keyboard while selecting one of the video windows to close the program.

### What's Next?
Applying edge filters to every single frame of a 30fps video is just one image processing technique, but as you might have noticed if your video feed lagged slightly, it is quite computationally intensive. 

Now that we have a live video feed established, we don't have to process every pixel. We can use simpler, more efficient techniques to compare frames against each other over time. This allows us to do **motion detection**, which leads us directly into Part 6...

---

## Part 6: Motion Detection via Frame Differencing

Applying heavy math (like the Sobel filter) to every pixel of every frame takes a lot of processing power. If we are building a security camera or a wildlife trap, we only care when something *moves*. 

Instead of analyzing every frame from scratch, we can take a "baseline" photo of the background. Then, for every new video frame, we mathematically subtract the new frame from the baseline. If the result is zero, nothing has changed. If the result is greater than zero, those specific pixels must represent movement! 



### Step 1: Preparing the Script
Make sure your camera is plugged in, you are still in your `opencv_testing` directory, and your virtual environment is active.

Copy the motion detection script from our workshop repository:
`cp ~/dev/Intro-to-Embedded-Linux-Development-Computer-Vision-and-Edge-AI/motion_detect.py .`

### Step 2: Inspecting the Code
Let's open it up in our text editor:
`vim motion_detect.py`

Scroll down and look at the `cv2.absdiff()` function. This calculates the absolute difference between our initial baseline frame and the current frame. Next, we use `cv2.threshold()` to convert any slight changes into stark white pixels, and `cv2.findContours()` to draw a green box around those white pixels.

*(Note: Remember to change the `camera_id` variable using Insert Mode if your camera is not at index `0`, then type `:wq` to save and quit).*

### Step 3: Run the Motion Tracker
**Important:** Before you run this command, point the camera at a static background and *step out of the frame*. The script uses the very first frame it sees as the empty baseline. 

Execute your script:
`python motion_detect.py`

Two windows will pop up:
1. **Motion Detection:** The live color feed. When you walk into the frame, a green rectangle should track your movement.
2. **Threshold (The Math):** A black-and-white window showing exactly what the computer "sees" as motion. White pixels are moving objects; black pixels are the static background.

Press `q` on your keyboard while selecting one of the video windows to safely exit the program.

### What's Next?
Motion detection tells us *where* something is, but it doesn't tell us *what* it is. A waving tree branch will trigger this script just as easily as a person. To solve this, we need to introduce Deep Learning and Object Recognition...

---

## Part 7: Deep Learning with YOLO

Motion detection tells us *where* something is, but it doesn't tell us *what* it is. A waving tree branch will trigger our motion script just as easily as a person. To solve this, we need to introduce Deep Learning and Object Recognition.

We are going to use **YOLO** (You Only Look Once), specifically the state-of-the-art YOLO26 nano model (`yolov26n`). 



### Step 1: Installing the AI Library
Make sure your virtual environment is still active (`source .venv/bin/activate`). We need to install the Ultralytics library, which manages the YOLO models.
`uv pip install ultralytics`

### Step 2: Preparing the Script
Copy the YOLO detection script from our workshop repository:
`cp ~/dev/Intro-to-Embedded-Linux-Development-Computer-Vision-and-Edge-AI/yolo_detect.py .`

Let's look at the code:
`vim yolo_detect.py`

Notice how incredibly simple the Ultralytics library makes this. We load the model, pass it a frame, and it hands back the frame with bounding boxes and labels automatically drawn on it!

*(Remember to check your `camera_id` variable before typing `:wq` to exit).*

### Step 3: Run the AI
Execute your script:
`python yolo_detect.py`

*Note: The very first time you run this, it will take a few seconds to download the `yolov26n.pt` model weights from the internet.*

Hold up your phone, a coffee cup, or just sit in the frame. The AI should draw boxes around you and categorize you. 

**The Problem:** You will likely notice the video feed is now quite laggy. Why? Because `yolov26n` is looking at the *entire* image frame, doing object detection, segmentation (finding the exact pixel outlines), and classification all at the same time. Doing this 30 times a second on an embedded device is a massive computational bottleneck. 

How do we improve this? We combine our techniques.

---

## Part 8: The Ultimate Edge AI Pipeline

To fix our lag, we are going to build a true Edge AI pipeline. We will use our highly efficient motion detection (CPU math) to find *where* things are. Then, we will crop out just the bounding box of the moving object and pass that tiny image to a specialized, classification-only AI model (`yolov26n-cls`). 

By only running the AI on a small crop of the image, and *only* when motion is detected, our frame rate will skyrocket!



### Step 1: Preparing the Pipeline Script
Copy the final script:
`cp ~/dev/Intro-to-Embedded-Linux-Development-Computer-Vision-and-Edge-AI/smart_motion_classify.py .`

Inspect the grand finale:
`vim smart_motion_classify.py`

Scroll through and see how Part 6 and Part 7 have been merged. We find the motion contour, create an image `frame_crop` of just that moving area, and pass it to our `classifier_model`.

### Step 2: Run the Pipeline
Point your camera at a static background (so it can get its baseline) and run the script:
`python smart_motion_classify.py`

Step into the frame. You should see the green motion-tracking box from Part 6, but now it has a text label above it telling you exactly what is moving, running much smoother than Part 7!

Congratulations! You have just built a highly optimized, context-aware Edge AI vision system from scratch.
