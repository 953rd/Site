$(document).ready(function () {
    $('.quantity-input').on('change', function () {
        var basketId = $(this).data('basket-id');
        var quantity = $(this).val();
        $.ajax({
            url: '/products/baskets/update_quantity/' + basketId + '/', // Обновленный URL-адрес
            method: 'POST',
            data: {
                'basket_id': basketId,
                'quantity': quantity,
                'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: function (data) {
                // Обновим сумму и общее количество товаров в корзине
                $('.total-sum').text(data.total_sum.replace('.', ',') + ' руб.');
                $('.total-quantity').text(data.total_quantity);
                var basketSum = $('.basket-sum[data-basket-sum=' + basketId + ']');
                basketSum.find('.basket-sum-value').text(data.basket_sum.toString().replace('.', ',') + ' руб.');
                console.log(data.basket_sum)
            },
            error: function (xhr, textStatus, errorThrown) {
                console.log(xhr.responseText);
            }
        });
    });
});
