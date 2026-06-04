# How to Access Your Heart Disease Analyzer From Other Networks

Your Flask server is currently running on **http://127.0.0.1:5001** (local machine only).

---

## ✅ Current Status
- **Flask Server**: Running and accessible locally ✓
- **Your LAN IP**: `192.168.1.102`
- **On same WiFi/LAN**: You can already use `http://192.168.1.102:5001`

---

## 🌐 Option 1: ngrok (EASIEST - Recommended for Quick Testing)

**What is ngrok?** A free service that creates a secure public URL to your local server. Anyone with the URL can access your app from anywhere in the world, no router changes needed.

**Pros:**
- ✅ Works instantly, no router/firewall configuration
- ✅ Works on any network (home, office, mobile hotspot)
- ✅ Free tier gives you one tunnel at a time
- ✅ Very secure

**Cons:**
- ❌ URL changes each time you restart (unless you pay)
- ❌ Requires internet connection
- ❌ Free tier has bandwidth limits

### Step-by-Step (ngrok)

#### Step 1: Create a Free ngrok Account
1. Go to **https://dashboard.ngrok.com/signup** in your browser
2. Click "Sign Up with GitHub" or use Email + Password
3. Verify your email
4. Log in to **https://dashboard.ngrok.com**

#### Step 2: Get Your AuthToken
1. In the dashboard, click **"Get Started"** or go to **https://dashboard.ngrok.com/get-started/your-authtoken**
2. You'll see a token like: `2dE7d..._ABC123XYZ...` (keep this secret!)
3. Copy this token to your clipboard

#### Step 3: Set Up ngrok on Your PC (One-Time)
Open PowerShell in your project folder and run:
```powershell
.\ngrok\ngrok.exe authtoken YOUR_TOKEN_HERE
```
Replace `YOUR_TOKEN_HERE` with the token you copied in Step 2.

Example:
```powershell
.\ngrok\ngrok.exe authtoken 2dE7d_ABC123XYZ_your_full_token_here
```

#### Step 4: Start the Tunnel
In a **new PowerShell terminal** (keep Flask running in the other one), run:
```powershell
.\ngrok\ngrok.exe http 5001
```

#### Step 5: Share the Public URL
Your terminal will show something like:
```
Forwarding    https://1a2b-34-56-78-90.ngrok-free.app -> http://localhost:5001
```

**Copy that URL** (`https://1a2b-34-56-78-90.ngrok-free.app`) and share it with others. They can paste it in their browser and access your app from anywhere!

#### Step 6: Stop the Tunnel
Press **Ctrl+C** in the ngrok terminal to stop it. When you restart, you'll get a new URL.

---

## 🔧 Option 2: Router Port Forwarding (More Permanent)

**What is it?** You configure your WiFi router to forward external port 5001 to your PC's internal IP. This makes your app accessible using your home/office public IP address.

**Pros:**
- ✅ Permanent URL (as long as your public IP doesn't change)
- ✅ No third-party service needed
- ✅ Works for always-on servers

**Cons:**
- ❌ Complex router configuration (varies by router brand)
- ❌ Exposes your PC directly to the internet (security risk without proper setup)
- ❌ Your public IP may change (ISP-dependent)
- ❌ Requires Windows Firewall admin access

### Step-by-Step (Router Port Forwarding)

#### Step 1: Allow Port 5001 Through Windows Firewall (Admin Required)
Right-click **PowerShell** → Select **"Run as Administrator"** → Paste this:
```powershell
New-NetFirewallRule -DisplayName "Flask5001" -Direction Inbound -LocalPort 5001 -Protocol TCP -Action Allow
```
Press Enter. You should see no errors if successful.

#### Step 2: Find Your Home Public IP
In any PowerShell, run:
```powershell
Invoke-RestMethod -Uri "https://api.ipify.org"
```
This will show your public IP, e.g., `203.45.67.89`. Write it down.

#### Step 3: Access Your Router's Admin Panel
1. In your browser, go to **http://192.168.1.1** or **http://router.local**
   - If that doesn't work, check your router's label for the correct address
2. Log in with your WiFi admin username/password
   - Default for many routers: username `admin`, password `admin` or blank
   - Check your router's manual or bottom/back label if you don't know

#### Step 4: Find Port Forwarding Settings
This varies by router brand. Look for:
- **Port Forwarding**, **Port Mapping**, or **Virtual Server** section
- Usually in: **Settings → Network → Port Forwarding** or **Advanced → Port Forwarding**

#### Step 5: Create a Port Forward Rule
Create a new rule with these values:
- **External Port**: `5001`
- **Internal IP**: `192.168.1.102`
- **Internal Port**: `5001`
- **Protocol**: `TCP`
- **Enable**: Yes/On

Save and apply the changes.

#### Step 6: Test Access From Outside Your Network
1. From your **phone on mobile data** (not WiFi), open a browser
2. Go to: `http://203.45.67.89:5001` (replace with your public IP from Step 2)
3. If you see your Heart Disease Analyzer, it worked! ✅

#### Step 7: Share the Link
Tell others to use: `http://YOUR_PUBLIC_IP:5001`

Example: `http://203.45.67.89:5001`

---

## ⚠️ Security Notes (Important!)

### If Using ngrok (Option 1):
- ✅ ngrok adds HTTPS encryption automatically
- ✅ Safe to share the URL publicly
- ✅ ngrok handles security

### If Using Port Forwarding (Option 2):
- ⚠️ Your PC is directly exposed to the internet
- ⚠️ Consider these steps:
  1. **Add a username/password** to your Flask app (optional but recommended)
  2. **Change your router's admin password** (many leave it as default)
  3. **Enable router firewall** (most routers have this)
  4. **Close the port when not needed** (disable port forwarding rule)
  5. **Consider HTTPS** (add SSL certificate to Flask)

---

## 📋 Quick Decision Tree

| Scenario | Best Option |
|----------|------------|
| Want to share quickly for testing? | **ngrok (Option 1)** |
| App will run 24/7? | **Port Forwarding (Option 2)** |
| Using on mobile hotspot? | **ngrok (Option 1)** |
| ISP keeps changing IP? | **ngrok (Option 1)** |
| Want permanent URL? | **Port Forwarding (Option 2)** |
| Don't want to touch router? | **ngrok (Option 1)** |

---

## 🚀 Quick Start Commands

### Option 1 (ngrok) - Copy & Paste:
```powershell
# First time only: set authtoken (replace TOKEN with your token)
.\ngrok\ngrok.exe authtoken YOUR_TOKEN_HERE

# Every time you want a public URL:
.\ngrok\ngrok.exe http 5001
```

### Option 2 (Port Forwarding) - Steps:
1. Run PowerShell as Administrator and paste: `New-NetFirewallRule -DisplayName "Flask5001" -Direction Inbound -LocalPort 5001 -Protocol TCP -Action Allow`
2. Find your public IP: `Invoke-RestMethod -Uri "https://api.ipify.org"`
3. Log into your router at `http://192.168.1.1`
4. Add port forward rule: External 5001 → Internal 192.168.1.102:5001
5. Share: `http://YOUR_PUBLIC_IP:5001`

---

## 🎯 Next Steps

1. **Read through Option 1 or Option 2** above (choose one)
2. **Follow the step-by-step instructions** for your chosen option
3. **Test the URL** on another device
4. **Share the URL** with others

Need help? Check the **Common Issues** section below or the individual option details above.

---

## ❓ Common Issues

### "ngrok not found" Error
- Make sure you extracted `ngrok.zip` first (it should create `ngrok` folder)
- Run: `Expand-Archive -Path ngrok.zip -DestinationPath .\ngrok -Force`

### "Windows Firewall denied" (Port Forwarding)
- Right-click PowerShell → "Run as Administrator"
- Try the firewall command again

### "Cannot connect from outside my network"
- Port Forwarding: Check router logs for port forwarding rule
- ngrok: Make sure tunnel is still running (you should see "Forwarding" line)

### URL keeps changing with ngrok
- Free tier always gives new URL on restart
- Upgrade to paid ngrok tier for static URLs

### "Connection Refused" error
- Make sure Flask server is still running (check the Flask terminal)
- Check firewall allows port 5001

---

## 📞 Summary

- **Both options work** — choose based on your needs
- **ngrok is easiest** for sharing quickly
- **Port Forwarding is best** for permanent access
- **Your Flask server is already running** — just pick one method above and follow the steps!

Good luck! 🎉
