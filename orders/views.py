import uuid
from yookassa import Configuration, Payment
from http import HTTPStatus

from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.http import HttpResponseRedirect

from common.views import TitleMixin
from orders.forms import OrderForm

class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Алькир - Спасибо за заказ!'

class CanceledTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/canceled.html'


class OrderCreateView(TitleMixin, CreateView):
    title = 'Алькир - Оформление заказа'
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)

        Configuration.account_id = settings.ACCOUNT_ID
        Configuration.secret_key = settings.SECRET_KEY

        payment = Payment.create({
            'amount': {
                'value': '1.00',
                'currency': 'RUB'
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': '{}{}'.format(settings.DOMAIN_NAME,
                                            reverse("orders:order_success"))
            },
            'capture': True,
            'description': 'Order No. 1'
        }, uuid.uuid4())

        return HttpResponseRedirect(payment.confirmation.confirmation_url,
                                    status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user

        return super(OrderCreateView, self).form_valid(form)
