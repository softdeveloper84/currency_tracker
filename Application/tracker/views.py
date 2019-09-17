from django.shortcuts import render
from .forms import CurrencyForm
from .models import CurrencyModel
from .models import ExchangeModel
from .utils.logger import Logger


def index(request):
    """ index controller
    :param request: input request parameter
    :return: rendered template for index.html
    """
    logger = Logger("index").get_instance()

    result = list()
    if request.method == "POST":
        form = CurrencyForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
    else:
        form = CurrencyForm()
    try:
        pairs = CurrencyModel.get_actual_currencies_pair()
        for pair in pairs:
            base = pair[0]
            target = pair[1]
            latest_price = ExchangeModel.objects.filter(base=base, target=target).order_by('-id')[0].price
            result.append([base, target, latest_price])
    except Exception as err:
        logger.error(err)
    return render(request, 'index.html', {"context": result, "form": form})
