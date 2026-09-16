"""
inactive_users.py

Flags user accounts in an ArcGIS org that may be worth reviewing:
  - INACTIVE:        no login for over INACTIVE_DAYS
  - NEVER LOGGED IN:  no recorded login
  - OLD ACCOUNT:      created more than OLD_ACCOUNT_YEARS ago

Useful for license reclamation, offboarding, and account cleanup.
This script identifies candidates for review; humans decide the action.

NOTE ON PRIVILEGES: listing every user in an org (gis.users.search()) typically
requires Administrator privileges. If you don't have them, this script falls
back to a small sample dataset (sample_org_users.csv, from this workshop's repo)
so you can still see the pattern run end-to-end.

Usage:
    python inactive_users.py

Requires:
    pip install arcgis pandas
"""

import os
import urllib.request
from datetime import datetime

import pandas as pd
from arcgis.gis import GIS

INACTIVE_DAYS = 180
OLD_ACCOUNT_YEARS = 3
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/nmholman/ubiquitous-barnacle/main"


def connect():
    return GIS("home")
    # import getpass
    # url = "https://your-org.maps.arcgis.com"
    # username = "your_username"
    # password = getpass.getpass("Password: ")
    # return GIS(url, username, password)


def days_since(dt):
    return (datetime.now() - dt).days


def audit_users_live(gis, max_users=200):
    """Requires admin (or equivalent) privileges. Raises if access is restricted."""
    org_users = gis.users.search(max_users=max_users)
    if len(org_users) <= 1:
        raise PermissionError("Only your own account is visible — likely no admin privileges.")

    records = []
    for u in org_users:
        created_dt = datetime.fromtimestamp(u.created / 1000)
        last_login_ts = getattr(u, "lastLogin", -1)

        flags = []
        if last_login_ts is None or last_login_ts == -1:
            flags.append("NEVER LOGGED IN")
            days_inactive = None
        else:
            last_login_dt = datetime.fromtimestamp(last_login_ts / 1000)
            days_inactive = days_since(last_login_dt)
            if days_inactive > INACTIVE_DAYS:
                flags.append("INACTIVE")

        if days_since(created_dt) > OLD_ACCOUNT_YEARS * 365:
            flags.append("OLD ACCOUNT")

        records.append({
            "username": u.username,
            "full_name": getattr(u, "fullName", ""),
            "role": u.role,
            "user_type": getattr(u, "userType", ""),
            "created": created_dt.date(),
            "days_inactive": days_inactive,
            "flags": ", ".join(flags) if flags else "",
        })

    return pd.DataFrame(records)


def audit_users_sample():
    """Fallback for accounts without admin privileges — uses sample data from the repo."""
    if not os.path.exists("sample_org_users.csv"):
        urllib.request.urlretrieve(f"{GITHUB_RAW_BASE}/data/sample_org_users.csv", "sample_org_users.csv")

    sample = pd.read_csv("sample_org_users.csv")
    records = []
    for _, u in sample.iterrows():
        created_dt = datetime.strptime(u["created"], "%Y-%m-%d")
        last_login_str = u["last_login"]

        flags = []
        if pd.isna(last_login_str) or last_login_str == "":
            flags.append("NEVER LOGGED IN")
            days_inactive = None
        else:
            last_login_dt = datetime.strptime(last_login_str, "%Y-%m-%d")
            days_inactive = days_since(last_login_dt)
            if days_inactive > INACTIVE_DAYS:
                flags.append("INACTIVE")

        if days_since(created_dt) > OLD_ACCOUNT_YEARS * 365:
            flags.append("OLD ACCOUNT")

        records.append({
            "username": u["username"],
            "full_name": u["full_name"],
            "role": u["role"],
            "user_type": u["user_type"],
            "created": created_dt.date(),
            "days_inactive": days_inactive,
            "flags": ", ".join(flags) if flags else "",
        })

    return pd.DataFrame(records)


def main():
    gis = connect()
    try:
        users_df = audit_users_live(gis)
        source = "live ArcGIS org"
    except Exception as e:
        print(f"Couldn't list org users ({e}). Falling back to sample data.")
        users_df = audit_users_sample()
        source = "sample dataset (no admin access detected)"

    users_df.to_csv("inactive_users.csv", index=False)
    flagged = len(users_df[users_df["flags"] != ""])
    print(f"Data source: {source}")
    print(f"Flagged {flagged} of {len(users_df)} users for review -> inactive_users.csv")


if __name__ == "__main__":
    main()
