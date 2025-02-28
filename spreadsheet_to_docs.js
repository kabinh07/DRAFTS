function generateConsentDocs() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = sheet.getDataRange().getValues();
  
  // Skip the header row
  data.shift(); 

  // Create a new Google Doc
  var doc = DocumentApp.create("Employee_Consent_Documents");
  var body = doc.getBody();

  // Set Page Margins (Left, Top, Right, Bottom in points)
  body.setMarginTop(28.8);   // 10.16 cm
  body.setMarginBottom(28.8); // 10.16 cm
  body.setMarginLeft(7.2);   // 2.54 cm
  body.setMarginRight(7.2); // 2.54 cm

  for (var i = 0; i < data.length; i++) {
    Logger.log("Processing row: " + i)
    var id = parseInt(data[i][0]).toString();         // Employee ID (Column 1)
    var name = data[i][1];       // Employee Name (Column 2)
    var joiningDateRaw = data[i][5]; // Joining Date (Column 6)

    // Format Joining Date (Convert from timestamp to "01 Aug 2022")
    var joiningDate = Utilities.formatDate(new Date(joiningDateRaw), Session.getScriptTimeZone(), "dd MMM yyyy");

    // Add a new page except for the first employee
    if (i > 0) {
      body.appendPageBreak();
    }

    // Title Formatting
    var title = body.appendParagraph("Consent for Membership Fees Deduction - Staff Club");
    title.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
    title.setFontSize(14).setBold(true).setUnderline(true).setLineSpacing(1.5);

    // Add some spacing
    body.appendParagraph("\n");

    // Create a paragraph for the consent text
    var consentPara = body.appendParagraph("");
    consentPara.setAlignment(DocumentApp.HorizontalAlignment.JUSTIFY);
    consentPara.setLineSpacing(1.5);

    // Append plain text first
    consentPara.appendText("I, ").setBold(false).setUnderline(false).setFontSize(12);

    // Append the Name (Bold)
    consentPara.appendText(name).setBold(true).setUnderline(false).setFontSize(12);
    
    // Append the rest of the sentence
    consentPara.appendText(", bearing ID- ").setBold(false).setUnderline(false).setFontSize(12);

    // Append the ID (Bold)
    consentPara.appendText(id).setBold(true).setUnderline(false).setFontSize(12);
    
    // Append the next part
    consentPara.appendText(", am signing up for membership of the Staff Club on ").setBold(false).setUnderline(false).setFontSize(12);

    // Append the Joining Date (Bold)
    consentPara.appendText(joiningDate).setBold(true).setUnderline(false).setFontSize(12);
    
    // Append the rest of the paragraph as plain text
    consentPara.appendText(" and am authorizing the Staff Club through the CPO division to deduct BDT 400 from my salary, " +
                   "at source, on a monthly basis, effective from 01 February 2025, as long as I keep my membership active.")
                   .setBold(false).setUnderline(false).setFontSize(12);

    var wordsToBold = [
      name, id.toString(), joiningDate, 
      "Staff Club", "CPO division", "BDT 400", 
      "salary", "monthly basis", "01 February 2025"
    ];
    
    wordsToBold.forEach(word => setBoldText(consentPara, word));

    consentPara.appendText("\n\n\n");

    // Signature Section
    var signature = body.appendParagraph("\nSignature: ___________________\nFull Name:");
    signature.setFontSize(12).setBold(false).setUnderline(false).setFontSize(12).setLineSpacing(1.5);
  }

  // Save & get the document URL
  var docUrl = doc.getUrl();
  Logger.log("Document created: " + docUrl);
  SpreadsheetApp.getUi().alert("Consent document created! \n" + docUrl);
}

function setBoldText(paragraph, word) {
  var text = paragraph.getText();
  var start = text.indexOf(word);
  if (start !== -1) {
    paragraph.editAsText().setBold(start, start + word.length - 1, true);
  }
}
