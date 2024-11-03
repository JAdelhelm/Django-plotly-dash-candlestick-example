from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import PlotlyExampleView




app_name = "example_plotly"
urlpatterns = [
    path("", PlotlyExampleView.as_view(), name="plotly_example"),


]
