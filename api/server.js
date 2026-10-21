const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

const UPLOAD_DIR = path.join(__dirname, 'uploads');
if (!fs.existsSync(UPLOAD_DIR)) fs.mkdirSync(UPLOAD_DIR, { recursive: true });

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, UPLOAD_DIR);
  },
  filename: function (req, file, cb) {
    const unique = Date.now() + '_' + file.originalname.replace(/\s+/g, '_');
    cb(null, unique);
  }
});
const upload = multer({ storage: storage, limits: { fileSize: 5 * 1024 * 1024 } });

// Simple filename-based recognition stub (mirrors diet_ai recognize_image_stub)
function recognizeStub(filePath) {
  const fname = path.basename(filePath).toLowerCase();
  const tokens = ["chicken","salad","pizza","burger","banana","egg","rice","pasta","fish","apple"];
  const preds = [];
  const heur = {
    banana: 105, apple: 95, egg: 78, rice: 200, bread: 80,
    chicken: 240, pizza: 285, burger: 320, pasta: 350, fish: 220
  };
  for (const t of tokens) {
    if (fname.includes(t)) {
      preds.push({ name: t.charAt(0).toUpperCase() + t.slice(1), calories: heur[t] || 200 });
    }
  }
  if (preds.length === 0) preds.push({ name: 'Mixed Plate (est)', calories: 400 });
  return preds;
}

app.post('/api/upload', upload.single('plate_image'), (req, res) => {
  if (!req.file) return res.status(400).json({ error: 'No file uploaded' });
  const filePath = req.file.path;
  const preds = recognizeStub(filePath);
  return res.json({ uploaded: true, file: '/api/uploads/' + path.basename(filePath), predictions: preds });
});

app.use('/api/uploads', express.static(UPLOAD_DIR));

app.get('/api/health', (req, res) => res.json({ ok: true }));

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => console.log(`AI Diet API listening on ${PORT}`));
