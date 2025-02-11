const express = require('express');
const fileUpload = require('./file-upload');
const path = require('path');
const fs = require('fs');
const axios = require('axios');
const FormData = require('form-data');

const router = express.Router();

router.post('/upload', fileUpload.single('audioFile'), async (req, res) => {
  const audioFile = req.file;
  if (!audioFile) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  const filePath = path.join(__dirname, audioFile.path);

  const form = new FormData();
  form.append('file', fs.createReadStream(filePath), {
    filename: audioFile.originalname,
    contentType: audioFile.mimetype,
  });

  try {
    const response = await axios.post('http://localhost:7000/recommend', form, {
      headers: {
        ...form.getHeaders(),
      },
    });
    console.log('Response from recommendation service:', response.data);
    fs.unlink(filePath, (err) => {
      if (err) {
        console.error('Error deleting file:', err);
      }
    });

    res.status(200).json(response.data);
  } catch (error) {
    console.error(
      'Error sending file to recommendation service:',
      error.response?.data || error.message
    );
    fs.unlink(filePath, (err) => {
      if (err) {
        console.error('Error deleting file after failure:', err);
      }
    });

    res.status(500).json({ error: 'Failed to process the file' });
  }
});

module.exports = router;
