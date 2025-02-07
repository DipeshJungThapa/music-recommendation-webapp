const express = requrie('express');
const fs = require('fs');
const path = require('path');

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
});

app.listen(port);
