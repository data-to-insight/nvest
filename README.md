# NVEST Tools(Contacts processing) & Regional Members Overview

This repo/tools provide browser-based uploading and processing NVEST contact data alongside a (quasi)live regional overview map. 
Uses **stlite** to run Streamlit/pyodide(in stlite) directly in browser and embeds both views via `<iframe>` containers into the html page(s) 

### Process Logic:

1. **Upload** contacts(from Wix downloaded) and steering group LAs files
    - W:\Performance Improvement Team\Data to Insight\NVEST\Contacts\contacts_web_signup\<get newest date file>.csv
    - W:\Performance Improvement Team\Data to Insight\NVEST\Contacts\contacts_other_sources\<get contacts_other_external file>.csv
2. **Clean & de-dup** contacts (keep most recent)  
3. **Add columns**: `domain`, `steering_grp` (default `"N"`), `web_signup` (default `"Web"`)  
4. **Update** `steering_grp` flag where `domain` matches one in steering group list  

### 🔄 Process Logic

1. **Upload** two contact CSVs:
   - 📥 *Wix signups:*  
     `NVEST/Contacts/contacts_web_signup/<latest>.csv`
   - 📥 *Other external contacts:*  
     `NVEST/Contacts/contacts_other_sources/<external>.csv`
2. **Clean + de-duplicate** each:
   - Drop blanks, rename columns
   - Parse `submission_date` (use today if missing)
   - Keep latest by `email`
3. **Remove overlaps** compare but remove from contacts_external, keep the web_signups record if exists (match on clean `email`). 
   - We need to remove before merge, as might not have submission date/time on external records - so determining most recent record not possible; so we assume web sign up is more recent as members directed to this input route after having shown interest via another route, e.g. workshop.       
4. **Add fields**:
   - `domain` (from email addr)  
   - `steering_grp` (default: `"N"`)  
   - `source`: `"Web"` for Wix, `"External"` for others
5. **Merge datasets** (on shared columns only)
6. **Flag steering group** by hardcoded email match (repo needs to stay private, as emails now in code not file)
7. **Preview flagged rows**, & option of timestamped CSV download

### Data Cleaning Logic:

- Drop empty rows/cols  
- Rename columns via `column_map`  
- Extract `domain` from `email`  
- Add missing cols: `steering_grp = 'N'`, `web_signup = 'Web|External'`  
- Parse `submission_date` as datetime  
- Sort by date, de-dup by `email` (keep latest)  
- Clean & lower `domain` in steering list  
- Flag contacts `steering_grp = 'Y'` if domain match  
- Highlight flagged rows  
- Enable timestamped CSV download


---

## Features

- Upload CSV of D2I web signup contacts  
- Upload CSV of steering group member domains (Do we need this to be member not LA specific??) 
- Clean and de-dup contact data (retain newest - might need a discussion/chk on this)  
- Flag contacts as steering group members based on domain matching (so is currently whole LA based!)  
- Download(option) for processed contacts file  
- View members regional boundaries on map
- Runs **fully in-browser** (no server or Python runtime needed)

---

## Structure

- `index.html`:  
  The main interface with a two-column layout using Bootstrap.  
  - Left: `upload_tool.html` (iframe)  
  - Right: Embedded Google Map (iframe)

- `upload_tool.html`:  
  HTML file embedding stlite-powered Streamlit app:
  - Upload and clean data
  - Match domains
  - Highlight steering group records(from additional upload file of domains)
  - Offer downloadable CSV

- `images/`:  
  Img assets (e.g., `d2i_logo.png`)

---

## Tech

- [Streamlit](https://streamlit.io) for data interface  
- [stlite](https://github.com/whitphx/stlite) to run Streamlit app directly in browser (WebAssembly + Pyodide)  
- [Bootstrap 5](https://getbootstrap.com) for layout  
- [Google My Maps](https://www.google.com/mymaps) for embedded regional visual

---

## Deployment Notes

Built to run in **GitHub Pages** and other static hosting providers. Ensure:

- avoid direct browser refresh on subpages (e.g., `/upload_tool.html`) unless served (e.g., via iframe or root-relative path) - i've not added # or 404 handling
- Test : python3 -m http.server 8501

---
