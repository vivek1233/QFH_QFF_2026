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

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
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
      data.timestamp    || '',
      data.ip           || '',
      data.city         || '',
      data.region       || '',
      data.country      || '',
      data.country_code || '',
      data.latitude     || '',
      data.longitude    || '',
      data.org          || '',
      data.timezone     || '',
      data.page         || '',
      data.referrer     || '',
      data.ua           || ''
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
