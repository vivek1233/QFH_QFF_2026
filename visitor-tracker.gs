/**
 * QFF 2026 — Visitor Tracker (Google Apps Script)
 * ─────────────────────────────────────────────────
 * Deploy this as a Web App:
 *   Execute as: Me
 *   Who has access: Anyone
 *
 * Then paste the Web App URL into index.html (GAS_URL variable).
 * And paste the published CSV URL into admin.html (SHEET_CSV_URL variable).
 */

var SHEET_NAME = 'Visitors';

// Admin password is NOT stored in code. Set it once in:
// Apps Script → Project Settings → Script properties → ADMIN_PASSWORD
// Visitor data is only returned to a request that supplies this password.
// Keep the Google Sheet itself PRIVATE (do not share it).

function jsonOut(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

// Prevent spreadsheet formula injection from untrusted visitor data
function clean(v) {
  v = (v === undefined || v === null) ? '' : String(v).slice(0, 500);
  return /^[=+\-@]/.test(v) ? "'" + v : v;
}

// Admin-only: return all visitor rows if the password is correct
function listVisitors(password) {
  var saved = PropertiesService.getScriptProperties().getProperty('ADMIN_PASSWORD');
  if (!saved || password !== saved) {
    Utilities.sleep(1000);
    return jsonOut({ status: 'denied' });
  }
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
  if (!sheet || sheet.getLastRow() < 2) return jsonOut({ status: 'ok', rows: [] });
  var values = sheet.getRange(2, 1, sheet.getLastRow() - 1, 13).getValues();
  var rows = values.map(function (r) {
    return r.map(function (c) {
      return c instanceof Date ? c.toISOString() : String(c);
    });
  });
  return jsonOut({ status: 'ok', rows: rows });
}

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    if (data.action === 'list') return listVisitors(data.password);

    var ss   = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName(SHEET_NAME);

    // Create sheet + header row if it doesn't exist
    if (!sheet) {
      sheet = ss.insertSheet(SHEET_NAME);
      sheet.appendRow([
        'Timestamp', 'IP Address', 'City', 'Region', 'Country', 'Country Code',
        'Latitude', 'Longitude', 'ISP / Org', 'Timezone', 'Page', 'Referrer', 'User Agent'
      ]);
      // Freeze header row and style it
      sheet.setFrozenRows(1);
      sheet.getRange(1, 1, 1, 13).setFontWeight('bold').setBackground('#2D1B69').setFontColor('#ffffff');
      sheet.setColumnWidth(1, 160);  // Timestamp
      sheet.setColumnWidth(2, 120);  // IP
      sheet.setColumnWidth(3, 120);  // City
      sheet.setColumnWidth(4, 120);  // Region
      sheet.setColumnWidth(5, 130);  // Country
      sheet.setColumnWidth(6, 60);   // Code
      sheet.setColumnWidth(7, 80);   // Lat
      sheet.setColumnWidth(8, 80);   // Lng
      sheet.setColumnWidth(9, 200);  // Org
      sheet.setColumnWidth(10, 160); // Timezone
      sheet.setColumnWidth(11, 300); // Page
      sheet.setColumnWidth(12, 200); // Referrer
      sheet.setColumnWidth(13, 300); // UA
    }

    // Append the visitor row
    sheet.appendRow([
      clean(data.timestamp),
      clean(data.ip),
      clean(data.city),
      clean(data.region),
      clean(data.country),
      clean(data.country_code),
      clean(data.latitude),
      clean(data.longitude),
      clean(data.org),
      clean(data.timezone),
      clean(data.page),
      clean(data.referrer),
      clean(data.ua)
    ]);

    return ContentService
      .createTextOutput(JSON.stringify({ status: 'ok' }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Handle GET requests (health check / test)
function doGet(e) {
  return ContentService
    .createTextOutput(JSON.stringify({ status: 'QFF2026 Visitor Tracker is live.' }))
    .setMimeType(ContentService.MimeType.JSON);
}
