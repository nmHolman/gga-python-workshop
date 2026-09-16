"""
content_audit.py

Flags items in an ArcGIS org that may be worth reviewing:
  - STALE:  not modified in over STALE_DAYS
  - LARGE:  larger than LARGE_SIZE_MB
  - PUBLIC: shared with everyone

This script identifies candidates for review. It does not make the
governance decision for you.

Usage:
    python content_audit.py

Requires:
    pip install arcgis pandas
"""

from datetime import datetime
import pandas as pd
from arcgis.gis import GIS

STALE_DAYS = 730         # ~2 years
LARGE_SIZE_MB = 500       # adjust threshold for your org


def connect():
    return GIS("home")
    # import getpass
    # url = "https://your-org.maps.arcgis.com"
    # username = "your_username"
    # password = getpass.getpass("Password: ")
    # return GIS(url, username, password)


def days_since(dt):
    return (datetime.now() - dt).days


def get_size_mb(item):
    try:
        return (item.size or 0) / (1024 * 1024)
    except Exception:
        return 0


def get_sharing(item):
    try:
        sharing = item.shared_with
        if sharing.get("everyone"):
            return "Everyone"
        elif sharing.get("org"):
            return "Organization"
        elif sharing.get("groups"):
            return "Groups"
        else:
            return "Private"
    except Exception:
        return "Unknown"


def audit_items(gis, max_items=200):
    items = gis.content.search(query="", max_items=max_items)

    records = []
    for item in items:
        modified_dt = datetime.fromtimestamp(item.modified / 1000)
        stale = days_since(modified_dt) > STALE_DAYS
        size_mb = get_size_mb(item)
        large = size_mb > LARGE_SIZE_MB
        sharing = get_sharing(item)
        public = sharing == "Everyone"

        flags = []
        if stale:
            flags.append("STALE")
        if large:
            flags.append("LARGE")
        if public:
            flags.append("PUBLIC")

        records.append({
            "title": item.title,
            "owner": item.owner,
            "modified": modified_dt.date(),
            "size_mb": round(size_mb, 1),
            "sharing": sharing,
            "flags": ", ".join(flags) if flags else "",
        })

    return pd.DataFrame(records)


def main():
    gis = connect()
    audit_df = audit_items(gis)
    audit_df.to_csv("content_audit.csv", index=False)
    flagged = len(audit_df[audit_df["flags"] != ""])
    print(f"Flagged {flagged} of {len(audit_df)} items for review -> content_audit.csv")


if __name__ == "__main__":
    main()
