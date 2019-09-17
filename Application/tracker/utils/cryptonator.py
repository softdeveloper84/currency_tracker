import requests
from .logger import Logger


class Cryptonator:
    """
    Class for interaction with cryptonator api (www.cryptonator.com)
    """
    base_url = "https://api.cryptonator.com/api"
    logger = Logger("Cryptonator").get_instance()
    all_possible_currency_codes = list()

    @classmethod
    def get_exchange_info_by_currency_pair(cls, curr_pair):
        """ Get json performance of exchange info
        :param curr_pair: currency pair
        :return: dictionary with exchange info
        """
        base = curr_pair[0]
        target = curr_pair[1]
        url = "{}/ticker/{}-{}".format(cls.base_url, base, target)
        try:
            exchange_info = requests.get(url).json()
            return exchange_info
        except Exception as err:
            cls.logger.error(err)
        return None

    @classmethod
    def get_all_possible_currency_codes(cls):
        """ Get all available codes for currency exchange
        :return: list of a
        """
        if not cls.all_possible_currency_codes:
            url = "{}/currencies".format(cls.base_url)
            try:
                response = requests.get(url).json()
                for row in response['rows']:
                    code = row['code']
                    if not (code, None) in cls.all_possible_currency_codes:
                        cls.all_possible_currency_codes.append((code, None))
            except Exception as err:
                cls.logger.error(err)
        return cls.all_possible_currency_codes
