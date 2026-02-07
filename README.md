# Karnataka F.C Web App 🍗

A Flask-based web application for a restaurant, featuring a menu, contact form, and customer reviews.

## 📁 Project Structure

```
restorant/
├── static/              # CSS, JS, Images
├── templates/           # HTML Templates
├── app.py               # Main Flask Application
├── requirements.txt     # Python Dependencies
├── .env                 # Environment Variables (Secrets)
├── firebase_key.json    # Firebase Admin SDK Key (DO NOT COMMIT TO GITHUB)
└── README.md            # This file
```

## 🛠️ Local Setup

1.  **Clone the repository** (if you haven't already).
2.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    ```
3.  **Activate variables**:
    -   Windows: `.venv\Scripts\activate`
    -   Mac/Linux: `source .venv/bin/activate`
4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
5.  **Run the app**:
    ```bash
    python app.py
    ```
    The app will run at `http://127.0.0.1:5000`.

## 🚀 Deployment Guide on Render

### Step 1: Push to GitHub
Make sure your project is pushed to a GitHub repository. **IMPORTANT**: Ensure `firebase_key.json` and `.env` are listed in your `.gitignore` file so they are NOT uploaded to GitHub.

### Step 2: Create a New Web Service on Render
1.  Log in to [Render.com](https://render.com).
2.  Click **New +** -> **Web Service**.
3.  Connect your GitHub repository.

### Step 3: Configure Service
-   **Name**: `karnataka-fc` (or any name you like)
-   **Region**: Singapore (or nearest to you)
-   **Runtime**: Python 3
-   **Build Command**: `pip install -r requirements.txt`
-   **Start Command**: `gunicorn app:app`

### Step 4: Environment Variables
Add the following Environment Variables in the Render Dashboard (under **Environment** tab):

| Key | Value |
| :--- | :--- |
| `MAIL_PASSWORD` | `awsm cihj stwh ikit` (Or your app password) |
| `PYTHON_VERSION` | `3.10.0` (Optional, good practice) |

### Step 5: Firebase Key (Secret File)
Since we didn't upload `firebase_key.json` to GitHub (for security), we need to give it to Render manually.

1.  In your Render Service Dashboard, go to **"Environment"**.
2.  Scroll down to **"Secret Files"**.
3.  Click **"Add Secret File"**.
4.  **Filename**: `firebase_key.json`
5.  **Content**: Open your local `firebase_key.json` file, copy everything, and paste it here.
6.  Click **"Save Changes"**.

Render will effectively put this file at `/etc/secrets/firebase_key.json`, and our `app.py` is already configured to look for it there!

### Step 6: Deploy
Click **Create Web Service**. Render will start building your app. Watch the logs. Once it says "Live", your site is ready!
#
