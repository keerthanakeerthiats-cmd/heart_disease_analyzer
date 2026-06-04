# ⚡ Quick ngrok Setup - Follow This Exactly

## Step 1: Create Your Free ngrok Account (2 minutes)

1. Open your browser and go to: **https://dashboard.ngrok.com/signup**

2. Click **"Sign up with Google"** or **"Sign up with GitHub"** (easiest)
   - OR enter Email + Password

3. **Verify your email** (click the link in the email)

4. **Log in** to https://dashboard.ngrok.com

You should now see the dashboard.

---

## Step 2: Get Your AuthToken (1 minute)

1. In the ngrok dashboard, click **"Get Started"** or go directly to:
   https://dashboard.ngrok.com/get-started/your-authtoken

2. You'll see a page with your token displayed. It looks like:
   ```
   2dE7dG_abc123XYZdefgh12345ijklmnop
   ```

3. **Copy this entire token** to your clipboard

---

## Step 3: Run the ngrok Setup Script (1 minute)

1. Go to your project folder:
   `C:\Users\VARUN COMPUTERS\Desktop\7th SEM\hhhhpppff`

2. **Double-click** the file named `SETUP_NGROK.bat`

3. A command window will appear asking:
   ```
   Enter your ngrok authtoken: 
   ```

4. **Paste your token** (right-click → Paste) that you copied in Step 2

5. Press **Enter**

6. Wait a few seconds... you should see:
   ```
   Forwarding    https://abc123-456-78-90.ngrok-free.app -> http://localhost:5001
   ```

7. **Copy that https://... URL** — that's your public link!

---

## Step 4: Share Your Public URL

The URL from Step 3 (e.g., `https://abc123-456-78-90.ngrok-free.app`) is **your public address**.

You can now:
- ✅ Open it in your browser from any device
- ✅ Share it with others to access your app from anywhere
- ✅ Test it on your phone using mobile data

---

## ⏹️ Stopping the Tunnel

When you're done:
1. Go to the command window where ngrok is running
2. Press **Ctrl+C**
3. The tunnel closes

Each time you run `SETUP_NGROK.bat`, you get a **new public URL** (free tier behavior).

---

## ✅ You're Done!

Your app is now publicly accessible. Share that https://... URL with anyone who needs access.

**Next time you want to share:** Just run `SETUP_NGROK.bat` again → paste your authtoken → get a new URL.

---

## 🆘 Issues?

| Problem | Solution |
|---------|----------|
| "ngrok not found" | Extract ngrok.zip first: `Expand-Archive -Path ngrok.zip -DestinationPath .\ngrok -Force` |
| "Invalid authtoken" | Check you copied the full token from dashboard.ngrok.com |
| "Connection refused" | Check Flask is still running in the other PowerShell window |
| Page says "ERR_NGROK_..." | Restart `SETUP_NGROK.bat` and paste token again |

---

Ready? Follow the 4 steps above and reply back with your public URL once you see the "Forwarding" line! 🎉
