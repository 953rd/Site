import uuid

from django.views.generic import DetailView
from yookassa import Configuration, Payment
from http import HTTPStatus

from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from common.views import TitleMixin
from orders.forms import OrderForm
from orders.models import Order


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


class OrdersShowView(TitleMixin, ListView):
    model = Order
    title = "Алькир - заказы"
    template_name = 'orders/orders.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:orders')

    def get_queryset(self):
        queryset = super(OrdersShowView, self).get_queryset()
        category_id = self.kwargs.get('order_id')

        if category_id:
            return queryset.filter(category_id=category_id)
        else:
            return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrdersShowView, self).get_context_data()
        context['orders'] = Order.objects.all()

        return context


class OrderShowView(TitleMixin, DetailView):
    title = "Алькир - заказ"
    template_name = 'orders/order.html'
    model = Order
    context_object_name = 'order'
    success_url = reverse_lazy('orders:order_detail')
