from django.conf.urls import url
from django.conf.urls import include
from . import views

stocks = [
    url('today$', views.QuoteTodayView.as_view(), name='today'),
    url('(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})$',
        views.QuoteRangedView.as_view(), name='ranged'),
    url('(?P<time_ago>\d+(d|m|y))$', views.QuoteRangedDetailed.as_view(),
        name='ranged-detailed'),
]

urlpatterns = [
    url('(?P<symbol>\w+)/', include(stocks))
]
