import json
import sys
import urllib.request
from datetime import datetime, timezone

BASE_URL = "https://digital-leaflet.lidlplus.com/api/v1/DK"

def fetch_json(url):
    req = urllib.request.Request(
        url, 
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))

def fetch_lidl_raw_data():
    print("Fetching campaign groups...")
    try:
        campaign_groups = fetch_json(f"{BASE_URL}/campaignGroups")
    except Exception as e:
        print(f"Failed to fetch campaign groups: {e}")
        sys.exit(1)

    campaigns = {}
    groups = campaign_groups.get("groups", [])

    for week in groups:
        for campaign in week.get("campaigns", []):
            campaign_id = campaign.get("id")
            title = campaign.get("title", "")
            print(f"Fetching campaign: {title} ({campaign_id})")

            try:
                raw_campaign_data = fetch_json(f"{BASE_URL}/campaigns/{campaign_id}")
                campaigns[campaign_id] = raw_campaign_data
            except Exception as e:
                print(f"Warning: Failed to fetch campaign {campaign_id}: {e}")
                continue

    raw_output = {
        "fetchedAt": datetime.now(timezone.utc).isoformat(),
        "campaignGroups": campaign_groups,
        "campaigns": campaigns
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(raw_output, f, indent=2, ensure_ascii=False)

    print("Successfully saved raw data to data.json")

if __name__ == "__main__":
    fetch_lidl_raw_data()