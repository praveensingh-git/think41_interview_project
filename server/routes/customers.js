const express = require('express');
const router = express.Router();
const db = require('../db');

// GET /customers?page=1&limit=10
router.get('/', async (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 10;
  const offset = (page - 1) * limit;

  try {
    const result = await db.query(
      'SELECT * FROM users ORDER BY user_id LIMIT $1 OFFSET $2',
      [limit, offset]
    );
    res.status(200).json({ customers: result.rows });
  } catch (err) {
    res.status(500).json({ error: 'Failed to fetch customers' });
  }
});

// GET /customers/:id
router.get('/:id', async (req, res) => {
  const customerId = parseInt(req.params.id);
  if (isNaN(customerId)) {
    return res.status(400).json({ error: 'Invalid customer ID' });
  }

  try {
    const userResult = await db.query('SELECT * FROM users WHERE user_id = $1', [customerId]);
    if (userResult.rows.length === 0) {
      return res.status(404).json({ error: 'Customer not found' });
    }

    const countResult = await db.query('SELECT COUNT(*) FROM orders WHERE user_id = $1', [customerId]);

    const customer = userResult.rows[0];
    const orderCount = parseInt(countResult.rows[0].count);

    res.status(200).json({ ...customer, order_count: orderCount });
  } catch (err) {
    res.status(500).json({ error: 'Failed to fetch customer' });
  }
});

module.exports = router;
