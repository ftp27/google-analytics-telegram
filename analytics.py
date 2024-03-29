from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    FilterExpression, Filter
)

from datetime import date
from datetime import timedelta

class Analytics:
    def __init__(self, config):
        self.property_id = config['property_id']
        self.client = BetaAnalyticsDataClient()
        self.date_format = "%Y-%m-%d"

    def run_report(self, dimension_name, event_filter, limit):
        """Runs a simple report on a Google Analytics 4 property."""
        week_ago = (date.today() - timedelta(days = 7)).strftime(self.date_format)
        
        dimension_filter = None
        if event_filter != None:
            dimension_filter = FilterExpression(
                filter=Filter(
                    field_name="eventName",
                    string_filter=Filter.StringFilter(value=event_filter),
                )
            )

        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            dimensions=[Dimension(name=dimension_name)],
            metrics=[Metric(name="activeUsers")],
            date_ranges=[DateRange(start_date=week_ago, end_date="today")], 
            dimension_filter=dimension_filter,
            limit=limit,
        )
        response = self.client.run_report(request)
        result = []
        for row in response.rows:
            demension = row.dimension_values[0].value
            value = row.metric_values[0].value
            if demension == "(not set)" or demension == "": 
                continue
            result.append((demension, value))
        return result