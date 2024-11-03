from django.views.generic import ListView, TemplateView
# Create your views here.
from .charts.plotly_app import create_dash_app



class PlotlyExampleView(TemplateView):
    template_name = "example.html"
    context_object_name = "details" 


     
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        
        app_name = create_dash_app(stock_symbol="APPL")

        context["app_name"] = app_name

        session = self.request.session
        django_plotly_dash_objs = session.get("django_plotly_dash", {})

        # In view
        django_plotly_dash_objs[f"{app_name}_stock_symbol"] = app_name
        session['django_plotly_dash'] = django_plotly_dash_objs
        session.modified = True

        return context   