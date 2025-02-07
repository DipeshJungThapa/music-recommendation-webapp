const express = require('express');
const HttpError = require('./http-error');
const { check } = require('express-validator');
const router = express.Router();

router.post('/recommend', check('file').not().isEmpty(), (req, res, next) => {
  const file = req.file;
  if (!file) {
    const error = new HttpError('No file found', 404);
    return next(error);
  }
  res.json({ message: 'Recommendation received' });
});
module.exports = router;
