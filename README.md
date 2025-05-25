# GhostCheck 
**GhostCheck** is a custom tkinter-based desktop application that helps you analyze your Instagram followers and following lists. It allows you to quickly find:

- Who **doesn't follow you back**
- Who **you don't follow back**
- A combined list of **everyone involved**
- The option to **unfollow users** directly via Selenium automation


## ⚙️ Features

- 🖥️ Intuitive and modern GUI using `customtkinter`
- 📥 Upload HTML data from Instagram to load your followers and following
- 🤖 Automated login and unfollowing using `undetected-chromedriver`
- 📊 Compare followers vs following with a click
- 🌙 Supports light, dark, and system UI themes
- 🔧 Saves UI appearance and scaling preferences


## 📸 Important Notice

> 🧾 You **must manually request** your **followers and following data** from Instagram in order to use this application.

### How to Export Instagram Data:
1. Go to your Instagram profile on a web browser.
2. Click **Settings > Your Activity > Download your information**
3. Choose **HTML format**
4. Select only **Connections > Followers and Following**
5. Once you receive the email from Instagram, **extract the ZIP file**
6. Open the app and upload:
   - You’ll be prompted to select `start_here.html`, and the app will locate the correct files automatically.
  
## Tutorial
1. Make sure you have ready your insatgram data. (Locate the start_here.html)
2. Press Upload Followers Data and select start_here.html
3. Same thing for the following button
4. Who doesn't Follow you Back, Who you don't Follow Back, Everyone: Makes a list based on your selection
5. Check the people you want to unfollow
6. Press the Log In button AND MANUALLY log in to your account
7. Press the unfollow button and let the magic happen. (It will take a few seconds per follower)
![image](https://github.com/user-attachments/assets/52e68a18-9f31-414e-a8bd-5df45951b70b)

## 🧠 How it Works

1. Upload both the **followers** and **following** HTML files.
2. GhostCheck will parse and display users in each group.
3. Use built-in buttons to:
   - See who doesn’t follow you back
   - See who you don’t follow back
   - Display everyone once
4. Select users to unfollow using checkboxes and click **Unfollow**.




## 🔧 Requirements

- Python 3.8+
- Google Chrome browser

### Python Libraries

Install dependencies using pip:

```bash
pip install -r requirements.txt
