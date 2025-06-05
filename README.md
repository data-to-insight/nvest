# NVEST Tools(Contacts processing) & Regional Members Overview

This repo/tools provide browser-based uploading and processing NVEST contact data alongside a (quasi)live regional overview map. 
Uses **stlite** to run Streamlit/pyodide(in stlite) directly in browser and embeds both views via `<iframe>` containers into the html page(s) 


### Process Logic

1. **Upload** two contact CSVs:
   - *Wix signups:*  
     `NVEST/Contacts/contacts_web_signup/<latest>.csv`
   - *Other external contacts:*  
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
5. **Merge datasets** (on shared/common columns only)
6. **Flag steering group** by hard-coded email match (repo needs to stay private, as those emails now in code not upload via file)
7. **Preview flagged rows**, & option of timestamped CSV download

### Data Cleaning Logic:

- Drop empty rows/cols  
- Rename columns via `column_map`  
- Extract `domain` from `email`  
- Add missing cols: `steering_grp = 'N'`, `web_signup = 'Web|External'` (can be extended) 
- Parse `submission_date` as datetime  (empty dates get today())
- Sort by date, de-dup by `email` (basic cleaning + lower) (keep latest. Web sign-ups take priority)  
- Flag contacts `steering_grp = 'Y'` if email match  
- Highlight flagged steering_grp rows in preview for ref 
- Enable timestamped CSV download


---

## Features

- Upload CSV of D2I web signup contacts  
- Upload CSV of steering group member domains (Do we need this to be member not LA specific??) 
- Clean and de-dup contact data (retain newest - might need a discussion/chk on this)  
- Flag contacts as steering group members based on domain matching (so is currently whole LA based!)  
- Download(option) for processed contacts file  
- View members regional boundaries on map
- Runs fully in-browser (stlite/Pyodide - same as d2i SEND/AA tools)

---

## Structure

## Structure

- `index.html`:  
  The main interface with two-column layout  
  - Left: `upload_tool.html` (iframe)  
  - Right: Embedded Google Map (iframe)

- `upload_tool.html`:  
  HTML file embedding a stlite-powered Streamlit app:
  - Upload and clean three CSV input types:
    - D2I web signups (internal contacts)
    - Other external contact lists (those not yet registered via d2i site form)
    - One or more event attendance CSVs (labelled by date)
  - Auto-normalise emails, remove junk cols, de-duplicate
  - Cross-check and merge internal and external contacts (by email)
  - Process event files:
    - Add `*_invited`, `*_sent`, `*_attended` cols for <<each>> date-labelled events CSV
  - Apply steering group highlighting (this only for ref in the preview - it's not in the csv download)
  - Reorder output fields for Excel usability
  - Gives downloadable, merged and cleaned CSV output


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
