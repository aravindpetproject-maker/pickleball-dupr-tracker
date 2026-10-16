from services.file_service import (
    load_json,
    save_json
)


class DashboardStatsService:

    FILE_NAME = "dashboard_stats.json"

    @staticmethod
    def increment_views():

        data = load_json(
            DashboardStatsService.FILE_NAME
        )

        if (
            not data
            or
            not isinstance(
                data,
                dict
            )
        ):

            data = {
                "dashboardViews": 0
            }

        data["dashboardViews"] += 1

        save_json(
            DashboardStatsService.FILE_NAME,
            data
        )

    @staticmethod
    def get_views():

        data = load_json(
            DashboardStatsService.FILE_NAME
        )

        if (
            not data
            or
            not isinstance(
                data,
                dict
            )
        ):

            return 0

        return data.get(
            "dashboardViews",
            0
        )