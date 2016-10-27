from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import permissions
from yahoo import YahooFinance
from yahoo import YahooChartApi


class QuoteTodayView(APIView):

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, symbol):
        ret = YahooFinance()\
            .stock_quote_today(symbol)['query']['results']['quote']
        return Response(ret)


class QuoteRangedView(APIView):

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, symbol, start_date, end_date):
        ret = YahooFinance().stock_quote_ranged(
                symbol, start_date, end_date)['query']['results']['quote']
        return Response(ret)


class QuoteRangedDetailed(APIView):

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, symbol, time_ago):
        return Response(YahooChartApi().quote_by_range(symbol, time_ago))
