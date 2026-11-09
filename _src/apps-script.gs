/**
 * Diwali Playdate Singapore — form inbox.
 * Bound to the "Diwali Playdate 2027 Sign-ups" Google Sheet.
 *
 * POST (from the website forms): appends one row to the tab named after the form
 *   (Waitlist, Volunteers, Talent show, Partner). New fields become new columns.
 * GET ?key=READ_KEY&tab=Waitlist&after=N: returns rows after row N as JSON.
 *   Used by the Mac job that posts each new sign-up to the WhatsApp group.
 *
 * Set READ_KEY under Project Settings → Script properties.
 */
const TABS = ['Waitlist', 'Volunteers', 'Talent show', 'Partner'];

function doPost(e) {
  const p = Object.assign({}, e.parameter || {});
  const tabName = TABS.indexOf(p.form) >= 0 ? p.form : 'Other';
  delete p.form;
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const sh = sheet_(tabName);
    let headers = sh.getLastRow() ? sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0] : [];
    if (!headers.length) { headers = ['Submitted at']; sh.appendRow(headers); sh.setFrozenRows(1); }
    Object.keys(p).forEach(k => {
      if (headers.indexOf(k) < 0) { headers.push(k); sh.getRange(1, headers.length).setValue(k); }
    });
    const row = headers.map(h => h === 'Submitted at' ? new Date() : (p[h] || ''));
    sh.appendRow(row);
  } finally {
    lock.releaseLock();
  }
  return ContentService.createTextOutput(JSON.stringify({ ok: true })).setMimeType(ContentService.MimeType.JSON);
}

function doGet(e) {
  const q = e.parameter || {};
  const key = PropertiesService.getScriptProperties().getProperty('READ_KEY');
  if (!key || q.key !== key) return json_({ error: 'forbidden' });
  const out = {};
  (q.tab ? [q.tab] : TABS).forEach(t => {
    const sh = SpreadsheetApp.getActive().getSheetByName(t);
    if (!sh || sh.getLastRow() < 2) { out[t] = []; return; }
    const vals = sh.getDataRange().getDisplayValues();
    const headers = vals[0];
    const after = Number(q.after || 1);
    out[t] = vals.slice(1).map((r, i) => {
      const o = { _row: i + 2 };
      headers.forEach((h, j) => o[h] = r[j]);
      return o;
    }).filter(o => o._row > after);
  });
  return json_(out);
}

function sheet_(name) {
  const ss = SpreadsheetApp.getActive();
  return ss.getSheetByName(name) || ss.insertSheet(name);
}

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}
