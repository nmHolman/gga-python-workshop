"""
content_inventory.py

Builds a full inventory of items in an ArcGIS Online / Enterprise organization:
title, type, owner, item ID, created date, and modified date.

Usage:
    python content_inventory.py

Requires:
    pip install arcgis pandas
    An active ArcGIS session (ArcGIS Notebooks) or org credentials (see connect() below).
"""

from datetime import datetime
import pandas as pd
from arcgis.gis import GIS


def connect():
    """Connect to your GIS. Adjust for your environment."""
    # Inside ArcGIS Notebooks (no credentials needed):
    return GIS("home")

    # Outside ArcGIS Notebooks, uncomment and fill in instead:
    # import getpass
    # url = "https://your-org.maps.arcgis.com"
    # username = "your_username"
    # password = getpass.getpass("Password: ")
    # return GIS(url, username, password)


def build_inventory(gis, max_items=200):
    """Search the organization and return a DataFrame of all items found."""
    items = gis.content.search(query="", max_items=max_items)

    records = []
    for item in items:
        records.append({
            "title": item.title,
            "type": item.type,
            "owner": item.owner,
            "id": item.id,
            "created": datetime.fromtimestamp(item.created / 1000),
            "modified": datetime.fromtimestamp(item.modified / 1000),
        })

    return pd.DataFrame(records)


def main():
    gis = connect()
    inventory_df = build_inventory(gis)
    inventory_df.to_csv("content_inventory.csv", index=False)
    print(f"Saved {len(inventory_df)} items to content_inventory.csv")


if __name__ == "__main__":
    main()
