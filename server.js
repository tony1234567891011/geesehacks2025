
const express = require('express');
const stripe = require('stripe')(sk_test_51QlDQSEONg3mlMtWJuMZzpworFQDciiVNLYeeGdzwuYswdGdIaLgyE0aW65QEQDiRd5VEaIH9DKlj6SkhjIsgF8u00oKng6OCz);
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

app.post('/create-payment-intent', async (req, res) => {
  const { amount, currency } = req.body;
  
  try {
    const paymentIntent = await stripe.paymentIntents.create({
      amount: amount,
      currency: currency,
    });

    res.status(200).send({
      clientSecret: paymentIntent.client_secret,
    });
  } catch (error) {
    res.status(500).send({ error: error.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
