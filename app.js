document.addEventListener('DOMContentLoaded', async () => {
    const stripe = Stripe(pk_test_51QlDQSEONg3mlMtW45FdPVqjCeEcqeMZfYuqqP4CLnQDgLO62Yg1doBbBfswGNyAE1TDrORGGldly7ZJZ6NlSUoV00YlrVbZmk);
    const elements = stripe.elements();
    const cardElement = elements.create('card');
    cardElement.mount('#card-element');
  
    const paymentForm = document.getElementById('payment-form');
    paymentForm.addEventListener('submit', async (event) => {
      event.preventDefault();
  
      const { paymentIntent, error } = await stripe.createPaymentMethod({
        type: 'card',
        card: cardElement,
        billing_details: {
          name: document.getElementById('card-holder-name').value,
        },
      });
  
      if (error) {
        console.error(error);
      } else {
        const response = await fetch('/create-payment-intent', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            amount: 1000, // Amount in cents
            currency: 'usd',
            payment_method: paymentIntent.id,
          }),
        });
  
        const data = await response.json();
        const clientSecret = data.clientSecret;
  
        const result = await stripe.confirmCardPayment(clientSecret, {
          payment_method: {
            card: cardElement,
            billing_details: {
              name: document.getElementById('card-holder-name').value,
            },
          },
        });
  
        if (result.error) {
          console.error(result.error);
        } else {
          console.log('Payment succeeded:', result.paymentIntent);
          alert('Payment successful!');
        }
      }
    });
  });
  