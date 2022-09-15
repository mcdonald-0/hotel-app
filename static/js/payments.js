function include(file) {

    var script = document.createElement('script');
    script.src = file;
    script.type = 'text/javascript';
    script.defer = true;

    document.getElementsByTagName('head').item(0).appendChild(script);

}

include('https://js.paystack.co/v1/inline.js')

var paymentData = JSON.parse(document.getElementById('payment-data').textContent),
    paymentButton = document.getElementById('make-payment-button');

function makePayment() {
    let currency = "NGN";
    let ref = paymentData['ref'];
    let obj = {
        key: paymentData['paystack_public_key'],
        email:  paymentData['guest_email'],
        amount: paymentData['amount_value'],
        ref:  ref,
        callback: function(response) {
            var url = $("#verified-payment-url").attr("data-url");
            window.location.href = url;
        }
    }
    if (Boolean(currency)) {
        obj.currency = currency.toUpperCase();
    }

    var handler = PaystackPop.setup(obj);
    handler.openIframe()
}

paymentButton.addEventListener('click', makePayment, false);



