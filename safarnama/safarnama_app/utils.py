import csv
import requests
from io import StringIO
from .models import Review

def fetch_and_save_google_form_responses(sheet_url):
    """
    Fetch data from a Google Sheet CSV and save it to the database.

    :param sheet_url: URL of the published Google Sheet in CSV format
    """
    response = requests.get(sheet_url)
    if response.status_code == 200:
        csv_data = StringIO(response.text)
        reader = csv.DictReader(csv_data)  # Automatically maps header row to dict keys

        for row in reader:
            # Ensure the column names in your CSV match these keys
            name = row.get("Name")
            review = row.get("Review")
            rating = row.get("Rating")

            # Skip rows with missing data
            if not (name and review and rating):
                continue

            # Avoid duplicate entries
            if not Review.objects.filter(name=name, review=review).exists():
                Review.objects.create(
                    name=name,
                    review=review,
                    rating=int(rating)
                )
    else:
        raise Exception(f"Failed to fetch data. Status code: {response.status_code}")
