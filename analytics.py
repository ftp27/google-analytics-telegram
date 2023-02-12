from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

from datetime import date
from datetime import timedelta

class Analytics:
    def __init__(self, config):
        self.property_id = config['property_id']

    def run_report(self, event_name, limit):
        """Runs a simple report on a Google Analytics 4 property."""
        client = BetaAnalyticsDataClient()
        date_format = "%Y-%m-%d"
        today = date.today().strftime(date_format)
        week_ago = (date.today() - timedelta(days = 7)).strftime(date_format)
        
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            dimensions=[Dimension(name="customEvent:" + event_name)], #"customEvent:category_name"
            metrics=[Metric(name="activeUsers")],
            date_ranges=[DateRange(start_date=week_ago, end_date="today")], 
            limit=limit,
        )
        response = client.run_report(request)
        result = []
        for row in response.rows:
            demension = row.dimension_values[0].value
            value = row.metric_values[0].value
            if demension == "(not set)": 
                continue
            result.append((demension, value))
        return result