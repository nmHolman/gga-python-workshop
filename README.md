# Python for GIS Professionals
### From ArcGIS Automation to Modern Geospatial Analytics

A 3.5-hour, project-based workshop for GIS analysts, administrators, and power users in local government who are newer to Python. Built for Google Colab.

## What's in this package

```
python-for-gis/
├── 01_python_fundamentals.ipynb   Python basics through GIS examples, intro to Pandas, 311 analysis
├── 02_arcgis_api_labs.ipynb       ArcGIS API basics + 3 step-by-step admin automation labs
├── 03_duckdb.ipynb                DuckDB fundamentals + a real spatial analysis over Overture Maps data
├── 03_gis_admin/                  Standalone take-home copies of the three admin scripts
│   ├── content_inventory.py
│   ├── content_audit.py
│   └── inactive_users.py
├── data/
│   ├── 311_requests.csv           Synthetic 311 service request dataset (2,500 records)
│   └── sample_org_users.csv       Synthetic org-user dataset (Lab 3 fallback for non-admins)
└── README.md                      This file
```

## Distributing via GitHub

These notebooks are built to be hosted on GitHub and opened directly in Colab — no local install, no manual data upload.

**These notebooks are already configured for `github.com/nmholman/ubiquitous-barnacle`.** If you're pushing to that repo as-is, no changes are needed — just push and go. If you fork this or reuse it under a different repo, update `GITHUB_RAW_BASE` in these three spots before publishing:
```python
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/nmholman/ubiquitous-barnacle/main"
```
- `01_python_fundamentals.ipynb` — setup cell near the top
- `02_arcgis_api_labs.ipynb` — Lab 3's data-loading cell
- `03_duckdb.ipynb` — setup cell near the top

**One-time setup before the workshop:**

1. Push this whole `python-for-gis/` folder to a **public** GitHub repo. (Public matters: a private repo requires each attendee to link GitHub to Colab and be granted repo access individually — much more friction for a live room. The data here is synthetic and the admin scripts contain no credentials, so public is safe.)
2. Confirm the repo path above matches where you actually pushed it.
3. Commit and push.

**Links to give attendees** (or point them to `File → Open notebook → GitHub` and paste your repo URL):
```
https://colab.research.google.com/github/nmholman/ubiquitous-barnacle/blob/main/01_python_fundamentals.ipynb
https://colab.research.google.com/github/nmholman/ubiquitous-barnacle/blob/main/02_arcgis_api_labs.ipynb
https://colab.research.google.com/github/nmholman/ubiquitous-barnacle/blob/main/03_duckdb.ipynb
```

**Tell attendees to do this immediately after opening each notebook:** `File → Save a copy in Drive`. Opening a notebook from GitHub gives them a read-only view — edits aren't saved back to your repo, and won't persist if they don't save their own copy first.

## Running the workshop

1. Attendees open `01_python_fundamentals.ipynb` from your GitHub link, save a copy to their own Drive, then run the setup cells — they install everything needed for the *entire* workshop and download the data file, so that only has to happen once.
2. Work through notebooks in order: `01` → `02` → `03`. (`03_gis_admin/` is a standalone take-home copy of the labs embedded in `02`, not something you run during the session.)
3. `02` requires a live ArcGIS Online or Enterprise connection — either an ArcGIS Notebooks environment (`GIS("home")` works automatically) or an org username/password if running in plain Colab. Lab 3 in that notebook needs admin privileges to list org users; it auto-falls-back to sample data for attendees who don't have them (see below).
4. `03`'s Overture Maps section queries public cloud-hosted data directly — no account or API key needed, just an internet connection. The capstone (Section 4.3) covers coffee shops across Georgia, joined against live Georgia county boundaries pulled from a public ArcGIS REST service, visualized as a per-capita choropleth.

## Handling Colab disconnects mid-workshop

With three-plus hours and a few breaks, a runtime disconnect/reset is likely for at least a few attendees. Each notebook's setup cells are safe to re-run at any point — they check whether packages are installed and whether the data file is already present before doing anything, so:

- If a participant returns from a break and a later cell errors (`NameError`, `FileNotFoundError`, `ModuleNotFoundError`), tell them to just re-run the setup cells near the top of that notebook, then continue — no need to re-run the whole notebook.
- Every cell is written to be safely re-runnable, so there's no "you broke it, start over" scenario.
- Remind attendees to `File → Save a copy in Drive` right at the start (see above) — that protects their *notebook and answers*, which re-running setup doesn't cover, since that only restores data/connections, not a lost tab.

## What to tell attendees to bring/prepare

A Google account is necessary but not sufficient. Send this checklist ahead of time:

1. **A Google account**, and — this is the part worth stressing — **test signing into Colab with it a day or two before**, from the actual laptop/network they'll use in class. `colab.research.google.com` should load and let them create a blank notebook and run `print("test")`. This matters especially for a local-government audience: some agency-managed Google Workspace accounts or locked-down networks block Colab, GitHub, or Drive outright, and that's not something you want to discover live in the room. If their work account is restricted, tell them to bring a personal Gmail account as a backup.
2. **ArcGIS Online or Enterprise credentials**, tested ahead of time — org URL, username/password (or SSO login flow if that's how their org authenticates). Have them confirm they can log into their portal in a browser first.
3. **Sufficient ArcGIS privileges to search org content and list org users.** Lab 1/2 (content inventory, content audit) work for any authenticated member — `gis.content.search()` just returns whatever is shared with that person, so a non-admin's results will be a narrower slice of the org, not an error. **Lab 3 (inactive users) is the one that actually requires Administrator privileges** (or a custom role with org-member visibility) to list other users' accounts. Non-admin attendees don't need to be paired up or given a shared login for this — the lab **automatically detects restricted access and falls back to a bundled sample dataset** (`data/sample_org_users.csv`), so everyone in the room runs the identical flagging code and finishes with a working script, just against sample data instead of their live org if they lack admin rights.
4. **A laptop with a modern browser** (Chrome or Edge recommended) — no other software install needed, everything runs in Colab.
5. Optional but helpful: **send the GitHub repo link and Colab links in advance**, so first-thing setup isn't the first time they've clicked anything.

## A note on data

- `311_requests.csv` is **synthetic** — generated to be realistic for a local-government 311 system, not real resident data. Swap in your own extract if you have one; the notebook code doesn't need to change as long as column names match (`department`, `request_type`, `status`, `created_date`, `days_open`).
- `sample_org_users.csv` is likewise **synthetic** — used only as a Lab 3 fallback for attendees without admin privileges (see above).
- The ArcGIS API labs in `02` are written to run against **your own organization** — they can't be pre-run against a specific org since every organization's content and users differ.
- `03`'s capstone pulls **live data from two public sources** at run time: Overture Maps (coffee shop locations, via cloud-hosted Parquet) and a public ArcGIS REST service (Georgia county boundaries + population, from SAGIS). Both require nothing but an internet connection, but since they're live services, verify both are reachable in a real run-through before the workshop — the Overture release string is set near the top of Section 4.2 and should be checked against docs.overturemaps.org/release-calendar if you're running this materially later than when it was built.

## Suggested next steps for participants

- ArcGIS API for Python documentation: https://developers.arcgis.com/python/
- DuckDB documentation: https://duckdb.org/docs/
- Overture Maps documentation: https://docs.overturemaps.org/
- Consider scheduling `content_audit.py` and `inactive_users.py` as recurring notebooks in ArcGIS Notebooks, or via a cron job, to build a lightweight ongoing governance habit.
