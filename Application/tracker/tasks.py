from datetime import timedelta
from celery import task
from celery.task import periodic_task
from .utils.cryptonator import Cryptonator
from .models import CurrencyModel
from .models import ExchangeModel


@periodic_task(run_every=timedelta(seconds=10), soft_time_limit=5)
def get_currency_exchange():
    """ Periodic celery task for started exchange procedure
    :return: None
    """
    currency_pairs = CurrencyModel.get_actual_currencies_pair()
    for currency_pair in currency_pairs:
        do_exchange.delay(currency_pair)


@task
def do_exchange(currency_pair):
    """ Info exchange celery task (for fixed currency pair)
    :param currency_pair: current currency pair
    :return:
    """
    exchange_info = Cryptonator.get_exchange_info_by_currency_pair(currency_pair)
    ExchangeModel.store_exchange_data(exchange_info)
