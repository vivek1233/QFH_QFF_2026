# Visitor Tracking — Setup Guide
## IBM Qiskit Fall Fest 2026

This guide sets up **free, serverless visitor tracking** for the website.
Visitor data (IP, city, country, timezone, etc.) is stored in a **Google Sheet**
and viewable on the **Admin Dashboard** at `/admin.html`.

---

## Architecture

```
Visitor lands on website
       ↓
ipapi.co (free IP geolocation API)
       ↓  returns city, country, lat/lng
Google Apps Script Web App (your backend)
       ↓  appends row
Google Sheet (your database)
       ↓  published as CSV
admin.html reads + displays table
```

---

## Step 1 — Create a Google Sheet

1. Go to [sheets.google.com](https://sheets.google.com) and create a new spreadsheet
2. Name it: **QFF2026 Visitor Tracker**
3. Leave it empty — the script will create the `Visitors` sheet and headers automatically

---

## Step 2 — Deploy the Google Apps Script

1. In your Google Sheet, go to **Extensions → Apps Script**
2. Delete any existing code in the editor
3. Copy the entire contents of **`visitor-tracker.gs`** and paste it in
4. Click **Save** (floppy disk icon), name the project: `QFF2026 Visitor Tracker`
5. Click **Deploy → New deployment**
6. Set:
   - **Type:** Web app
   - **Description:** QFF2026 Visitor Tracker v1
   - **Execute as:** Me
   - **Who has access:** Anyone
7. Click **Deploy** → authorise the permissions when prompted
8. **Copy the Web App URL** — it looks like:
   `https://script.google.com/macros/s/AKfycb.../exec`

---

## Step 3 — Paste the Web App URL into index.html

Open `index.html` and find this line near the bottom (inside the visitor tracker script):

```js
var GAS_URL = 'YOUR_GOOGLE_APPS_SCRIPT_WEB_APP_URL';
```

Replace `YOUR_GOOGLE_APPS_SCRIPT_WEB_APP_URL` with your copied URL:

```js
var GAS_URL = 'https://script.google.com/macros/s/AKfycb.../exec';
```

---

## Step 4 — Publish the Google Sheet as CSV

1. In your Google Sheet, go to **File → Share → Publish to web**
2. Set: **Visitors** sheet → **Comma-separated values (.csv)**
3. Click **Publish** and **Copy the link**
4. The link looks like:
   `https://docs.google.com/spreadsheets/d/SHEET_ID/gviz/tq?tqx=out:csv&sheet=Visitors`

---

## Step 5 — Paste the CSV URL into admin.html

Open `admin.html` and find this line near the bottom:

```js
var SHEET_CSV_URL = 'YOUR_GOOGLE_SHEET_CSV_URL';
```

Replace it with your published CSV URL:

```js
var SHEET_CSV_URL = 'https://docs.google.com/spreadsheets/d/SHEET_ID/gviz/tq?tqx=out:csv&sheet=Visitors';
```

---

## Step 6 — Set Your Admin Password

In `admin.html`, find:

```js
var ADMIN_PASSWORD_HASH = 'qff2026admin';
```

Change `qff2026admin` to your preferred admin password.

---

## Step 7 — Commit & Push

```bash
git add index.html admin.html
git commit -m "Configure visitor tracking with Google Apps Script"
git push origin main
```

The GitHub Actions workflow will deploy automatically within ~2 minutes.

---

## Accessing the Admin Dashboard

URL: **https://vivek1233.github.io/QFH_QFF_2026/admin.html**

- Enter your admin password to sign in
- View real-time visitor table with city, country, IP, timezone
- Use the **Download Excel** button to export all records as a `.csv` file (opens directly in Excel)
- Use **Refresh** to reload the latest data from Google Sheets

---

## Data Collected Per Visit

| Field | Description |
|-------|-------------|
| Timestamp | UTC time of visit (ISO 8601) |
| IP Address | Visitor's public IP |
| City | Detected city |
| Region | State / province |
| Country | Full country name |
| Country Code | ISO 2-letter code (e.g. IN, US) |
| Latitude | Approximate lat |
| Longitude | Approximate lng |
| ISP / Org | Internet service provider |
| Timezone | e.g. Asia/Kolkata |
| Page | Full URL visited |
| Referrer | Where they came from (or "direct") |
| User Agent | Browser + OS string |

---

## Privacy Notes

- Only **one record per browser session** is logged (not on every click)
- No cookies are set; no personal names are collected
- IP geolocation is handled by [ipapi.co](https://ipapi.co) (free tier: 1,000 requests/day)
- Data is stored only in **your own** Google Sheet — no third-party analytics platform
- Compliant with India DPDP Act 2023 for event analytics purposes

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| No data in admin dashboard | Check that both URLs are correctly pasted in `index.html` and `admin.html` |
| "Error loading data" in admin | Ensure the Google Sheet is published to web as CSV |
| Visits not being tracked | Open browser console on the website and check for fetch errors |
| Apps Script authorization error | Re-deploy the script and re-authorise permissions |
| ipapi.co rate limit | Free tier allows 1,000 requests/day; upgrade at ipapi.co for higher volume |
