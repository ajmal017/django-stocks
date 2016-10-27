from django.test import TestCase
# from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from stocks import yahoo

import logging
logger = logging.getLogger('stocks_info')


class YahooChartApiTestCase(TestCase):

    def setUp(self):
        self.ychart = yahoo.YahooChartApi()

    def test_yhoo_1d(self):
        resp = self.ychart.quote_by_range_raw('YHOO', '1d')
        logger.debug(resp)
        # self.assertEqual(len(resp) == , True)


class YahooFinanceQuoteTestCase(TestCase):

    def setUp(self):
        self.yfin = yahoo.YahooFinance()

    def test_yhoo_last_quote(self):
        resp = self.yfin.stock_quote_today('YHOO')
        self.assertEqual(resp['query']['count'], 1)

    def test_yhoo_month_quote(self):
        resp = self.yfin.stock_quote_month('YHOO', 2016, yahoo.JAN)
        self.assertEqual(resp['query']['count'], 19)


class APITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            'johndoe', 'johndoe@mail.com', 'johndoe')
        self.user.first_name = 'John'
        self.user.last_name = 'Doe'
        self.user.save()
        self.token = Token.objects.get(user=self.user)

    def test_today_quote(self):
        request = self.client.get('/stocks/YHOO/today')
        self.assertEqual(request.status_code, 401)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        request = self.client.get('/stocks/YHOO/today')
        self.assertEqual(request.status_code, 200)
