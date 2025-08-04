from core.router import api_router

from .report_card_api import ReportCardAPI
app_name = "report_card"


api_router.register("v1/report-cards", ReportCardAPI, basename="v1_report_cards_api")
urlpatterns = api_router.urls
