from django.urls import path
from . import views

urlpatterns = [
    path('login/',      views.login_view,         name='login'),
    path('logout/',     views.logout_view,         name='logout'),
    path('dashboard/',  views.dashboard,           name='dashboard'),
    path('trade/',      views.trade,               name='trade'),
    path('history/',    views.history,             name='history'),
    path('api/quote/',  views.api_quote,           name='api_quote'),
    path('api/chart/',  views.api_portfolio_chart, name='api_chart'),
    path('api/search/', views.api_search,          name='api_search'),
]
