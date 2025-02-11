const express = require('express');
const controller = require('./controllers');
const fileUpload = require('./file-upload');

const router = express.Router();

router.post(
  '/upload',
  fileUpload.single('audioFile'),
  controller.recommendation
);

module.exports = router;
