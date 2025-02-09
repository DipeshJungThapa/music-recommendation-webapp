const multer = require('multer');

const MIME_TYPE_MAP = {
  'audio/mpeg': 'mp3',
};

const fileUpload = multer({
  limits: 1000000,
  storage: multer.diskStorage({
    destination: (req, file, cb) => {
      cb(null, 'uploads');
    },
    filename: (req, file, cb) => {
      const ext = MIME_TYPE_MAP[file.mimetype];
      const originalName = file.originalname;
      const nameWithoutExtension = originalName
        .split('.')
        .slice(0, -1)
        .join('.');
      const newFileName = `${nameWithoutExtension}.${ext}`;

      cb(null, newFileName);
    },
  }),
  fileFilter: (req, file, cb) => {
    const isValid = !!MIME_TYPE_MAP[file.mimetype];
    let error = isValid ? null : new Error('Invalid mime type!');
    cb(error, isValid);
  },
});

module.exports = fileUpload;
