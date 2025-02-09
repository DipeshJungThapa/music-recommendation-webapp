const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
require('dotenv').config();

const routes = require('./routes');
const HttpError = require('./http-error');

const app = express();
app.use(express.json());
const port = process.env.PORT || 5000;

app.use(
  cors({
    origin: '*',
    methods: ['GET', 'POST', 'PATCH', 'DELETE'],
    allowedHeaders: [
      'Origin',
      'X-Requested-With',
      'Content-Type',
      'Accept',
      'Authorization',
      'role',
    ],
  })
);
app.use('/', routes);
app.use((req, res, next) => {
  const error = new HttpError("couldn't find the route", 404);
  next(error);
});
app.use((error, req, res, next) => {
  if (req.file) {
    fs.unlink(req.file.path, () => {
      console.log(error);
    });
  }
  if (res.headerSent) {
    return next(error);
  }
  res
    .status(error.code || 500)
    .json({ message: error.message || 'an unknown error occured' });
});
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
