const express = require('express');
const HttpError = require('./http-error');
const fileUpload = require('./file-upload');

const router = express.Router();

router.post('/upload', fileUpload.single('audioFile'), (req, res, next) => {
  const audioFile = req.file;
  if (!audioFile) {
    const error = new HttpError('No file found', 404);
    return next(error);
  }

  res.status(201).json({ audioFile: audioFile });
});
module.exports = router;
