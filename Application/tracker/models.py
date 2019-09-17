from django.db import models
from .utils.cryptonator import Cryptonator
from .utils.logger import Logger


class ExchangeModel(models.Model):
    """
    ExchangeModel (item exchange info)
    """
    logger = Logger("EchangeModel").get_instance()

    timestamp = models.IntegerField()
    success = models.BooleanField()
    base = models.CharField(max_length=10, default="BTC")
    target = models.CharField(max_length=10, default="USD")
    price = models.FloatField()
    error = models.CharField(max_length=2048)

    def save(self, *args, **kwargs):
        """ Save to db procedure
        :param args: unnamed parameters
        :param kwargs: named parameters
        :return:
        """
        self.price = round(self.price, 2)
        super(ExchangeModel, self).save(*args, **kwargs)

    @classmethod
    def store_exchange_data(cls, data):
        """ Store exchange info to db
        :param data: dictionary with exchange info
        :return:
        """
        try:
            if isinstance(data, dict):
                ticker = data['ticker']
                base = ticker['base']
                target = ticker['target']
                price = float(ticker['price'])
                timestamp = data['timestamp']
                success = data['success']
                error = data['error']
                cls(base=base, target=target, price=price, timestamp=timestamp, success=success, error=error).save()
        except Exception as err:
            cls.logger.error(err)


class CurrencyModel(models.Model):
    """
    CurrencyModel (available currency codes and currency pairs)
    """
    logger = Logger("CurrencyModel").get_instance()
    possibly_choices = Cryptonator.get_all_possible_currency_codes()
    base = models.CharField(max_length=10, choices=possibly_choices)
    target = models.CharField(max_length=10, choices=possibly_choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['base', 'target'], name="unique_base_and_target"),
        ]

    @classmethod
    def get_actual_currencies_pair(cls):
        """ Get info about actual currency pairs in db
        :return: list of actual currency pairs
        """
        pairs = list()
        try:
            for pair in cls.objects.all().order_by('id'):
               pairs.append([pair.base, pair.target])
        except Exception as err:
            cls.logger.error(err)
        return pairs
