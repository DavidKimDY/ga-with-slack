"""Hello Analytics Reporting API V4."""
import datetime
import json

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]
KEY_FILE_LOCATION = "google_anaytics_api_key.json"
VIEW_ID = "214197006"
VIEW_ID_USER_ID = "214214459"


def initialize_analyticsreporting():
    """Initializes an Analytics Reporting API V4 service object.

    Returns:
      An authorized Analytics Reporting API V4 service object.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES
    )

    # Build the service object.
    analytics = build("analyticsreporting", "v4", credentials=credentials)

    return analytics


def get_today_and_yesterday_and_a_week_ago():
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    a_week_ago = today - datetime.timedelta(days=7)

    today = today.isoformat().split("T")[0]
    yesterday = yesterday.isoformat().split("T")[0]
    a_week_ago = a_week_ago.isoformat().split("T")[0]
    return today, yesterday, a_week_ago


def get_page_views_in_last_week(analytics):
    today, _, a_week_ago = get_today_and_yesterday_and_a_week_ago()
    return (
        analytics.reports()
        .batchGet(
            body={
                "reportRequests": [
                    {
                        "viewId": VIEW_ID,
                        "dateRanges": [{"startDate": a_week_ago, "endDate": today}],
                        "dimensions": [
                            {"name": "ga:pageTitle"},
                        ],
                        "metrics": [
                            {"expression": "ga:users"},
                            {"expression": "ga:pageViews"},
                        ],
                    }
                ]
            }
        )
        .execute()
    )


def get_device_category_in_last_week(analytics):
    today, _, a_week_ago = get_today_and_yesterday_and_a_week_ago()
    return (
        analytics.reports()
        .batchGet(
            body={
                "reportRequests": [
                    {
                        "viewId": VIEW_ID,
                        "dateRanges": [{"startDate": a_week_ago, "endDate": today}],
                        "dimensions": [
                            {"name": "ga:deviceCategory"},
                        ],
                        "metrics": [
                            {"expression": "ga:users"},
                            {"expression": "ga:pageViews"},
                        ],
                    }
                ]
            }
        )
        .execute()
    )


def get_page_view_in_last_day(analytics):
    today, yesterday, _ = get_today_and_yesterday_and_a_week_ago()
    return (
        analytics.reports()
        .batchGet(
            body={
                "reportRequests": [
                    {
                        "viewId": VIEW_ID,
                        "dateRanges": [{"startDate": yesterday, "endDate": today}],
                        "dimensions": [
                            {"name": "ga:pageTitle"},
                        ],
                        "metrics": [
                            {"expression": "ga:users"},
                            {"expression": "ga:pageViews"},
                        ],
                    }
                ]
            }
        )
        .execute()
    )


def get_userActivity(analytics):
    return analytics.user()


def save(res, name):
    with open(name + ".json", "w", encoding="utf-8") as f:
        json.dump(res, f, indent="\t", ensure_ascii=False)


def daily():
    analytics = initialize_analyticsreporting()
    save(get_page_view_in_last_day(analytics), "daily_pageViews")


def weekly():
    analytics = initialize_analyticsreporting()
    save(get_device_category_in_last_week(analytics), "devices_category")
    save(get_page_views_in_last_week(analytics), "weekly_pageViews")

