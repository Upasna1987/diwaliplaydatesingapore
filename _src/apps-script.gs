/**
 * Diwali Playdate Singapore — form inbox.
 * Bound to the "Diwali Playdate 2027 Sign-ups" Google Sheet.
 *
 * POST (from the website forms): appends one row to the tab named after the form
 *   (Waitlist, Volunteers, Talent show). Only the fields listed in FIELDS are kept.
 * GET ?key=READ_KEY&tab=Waitlist&after=N: returns rows after row N as JSON.
 *   Used by the Mac job that posts each new sign-up to the WhatsApp group.
 *
 * Set READ_KEY under Project Settings → Script properties.
 */
// Only these fields are stored, in this column order. Anything else is ignored.
const FIELDS = {
  'Waitlist': ['name', 'email', 'phone', 'interest', 'adults', 'kids', 'kid_ages', 'message'],
  'Volunteers': ['name', 'email', 'phone', 'age_group', 'station_1', 'station_2', 'own_activity', 'video_link', 'experience'],
  'Talent show': ['parent_name', 'email', 'phone', 'child_age', 'child_name', 'talent', 'act_title', 'music', 'video_link', 'message'],
};
const TABS = Object.keys(FIELDS);

// Plain text only: no formulas, capped length.
function clean_(v) {
  v = String(v || '').slice(0, 1000);
  return /^[=+\-@\t\r]/.test(v) ? "'" + v : v;
}

function doPost(e) {
  const p = e.parameter || {};
  const fields = FIELDS[p.form];
  if (!fields) return json_({ error: 'unknown form' });
  const headers = ['Submitted at'].concat(fields);
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const sh = sheet_(p.form);
    if (!sh.getLastRow()) { sh.appendRow(headers); sh.setFrozenRows(1); }
    sh.appendRow([new Date()].concat(fields.map(f => clean_(p[f]))));
  } finally {
    lock.releaseLock();
  }
  return json_({ ok: true });
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
      const o = {};
      headers.forEach((h, j) => o[h] = r[j]);
      o._row = i + 2;
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
