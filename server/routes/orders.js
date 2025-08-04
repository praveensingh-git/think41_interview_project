const express = require('express');
const router = express.Router();
const db = require('../db');

// GET /orders/customer/:user_id
router.get('/customer/:user_id', async (req, res) => {
  const userId = parseInt(req.params.user_id);
  if (isNaN(userId)) {
    return res.status(400).json({ error: 'Invalid customer ID' });
  }

  try {
    const userCheck = await db.query('SELECT * FROM users WHERE user_id = $1', [userId]);
    if (userCheck.rows.length === 0) {
      return res.status(404).json({ error: 'Customer not found' });
    }

    const result = await db.query('SELECT * FROM orders WHERE user_id = $1 ORDER BY order_date DESC', [userId]);
    res.status(200).json({ orders: result.rows });
  } catch (err) {
    res.status(500).json({ error: 'Failed to fetch orders for customer' });
  }
});

// GET /orders/:order_id
router.get('/:order_id', async (req, res) => {
  const orderId = parseInt(req.params.order_id);
  if (isNaN(orderId)) {
    return res.status(400).json({ error: 'Invalid order ID' });
  }

  try {
    const result = await db.query('SELECT * FROM orders WHERE order_id = $1', [orderId]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Order not found' });
    }
    res.status(200).json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: 'Failed to fetch order' });
  }
});

module.exports = router;