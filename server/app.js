const express = require('express');
const cors = require('cors');
const customerRoutes = require('./routes/customers');

const app = express();
app.use(cors());
app.use(express.json());


app.get('/', (req, res) => {
  res.send('✅ Customer Order Dashboard API is running. Use /customers or /customers/:id');
});

// Customer API
app.use('/customers', customerRoutes);

module.exports = app;
