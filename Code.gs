const SHEET_NAME = "records";

function doPost(e) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName(SHEET_NAME);

    const data = JSON.parse(e.postData.contents);

    // Keep column order aligned with your Google Sheet header
    sheet.appendRow([
      data.record_id || "",
      data.record_type || "",
      data.name || "",
      data.phone || "",
      data.crop || "",
      data.quantity_kg || "",
      data.location || "",
      data.date || "",
      data.price_xof || "",
      data.grade || "",
      data.notes || "",
      data.hub_name || "",
      data.storage_days || "",
      data.storage_fee_xof || "",
      data.payment_ref || "",
      data.payment_status || "",
      new Date().toISOString()
    ]);

    return ContentService
      .createTextOutput(JSON.stringify({status: "success"}))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({status: "error", message: err.message}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet() {
  return ContentService.createTextOutput("Mali Produce API is running.");
}
