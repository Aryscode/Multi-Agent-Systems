const express = require('express');
const fs = require('fs').promises;
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const DATA_DIR = path.resolve(__dirname, '..', 'data'); // files will be stored here
const AUTH_KEY = process.env.FUN_APIS_ONLY_API_KEY || '';

app.use(express.json());

// simple auth middleware if FUN_APIS_ONLY_API_KEY is set
app.use('/api', (req, res, next) => {
  if (!AUTH_KEY) return next();
  const auth = req.get('authorization') || '';
  if (!auth.startsWith('Bearer ')) return res.status(401).json({ error: 'Missing Bearer token' });
  const token = auth.slice('Bearer '.length).trim();
  if (token !== AUTH_KEY) return res.status(403).json({ error: 'Invalid token' });
  next();
});

// helper to resolve and validate target path inside DATA_DIR
function resolveFilePath(requestPath) {
  // trim leading slash if present
  if (requestPath.startsWith('/')) requestPath = requestPath.slice(1);
  // disallow empty names
  if (!requestPath) throw { status: 400, message: 'File path required' };
  // normalize to prevent path traversal
  const target = path.resolve(DATA_DIR, requestPath);
  if (!target.startsWith(DATA_DIR + path.sep)) {
    throw { status: 400, message: 'Invalid file path' };
  }
  return target;
}

// Create a file (POST /api/files/<path>)
app.post('/api/files/*', async (req, res) => {
  try {
    const reqPath = req.params[0] || '';
    const filePath = resolveFilePath(reqPath);
    const dir = path.dirname(filePath);

    const { content } = req.body;
    if (typeof content !== 'string') {
      return res.status(400).json({ error: 'Request body must include string "content"' });
    }

    await fs.mkdir(dir, { recursive: true });
    await fs.writeFile(filePath, content, 'utf8');

    return res.status(201).json({ ok: true, path: reqPath });
  } catch (err) {
    const status = err && err.status ? err.status : 500;
    const message = err && err.message ? err.message : String(err);
    return res.status(status).json({ error: message });
  }
});

// Read a file (GET /api/files/<path>)
app.get('/api/files/*', async (req, res) => {
  try {
    const reqPath = req.params[0] || '';
    const filePath = resolveFilePath(reqPath);

    const data = await fs.readFile(filePath, 'utf8');
    res.type('text/plain').status(200).send(data);
  } catch (err) {
    // map common errors
    if (err && err.code === 'ENOENT') return res.status(404).json({ error: 'File not found' });
    const status = err && err.status ? err.status : 500;
    const message = err && err.message ? err.message : String(err);
    return res.status(status).json({ error: message });
  }
});

// simple delete endpoint (optional)
app.delete('/api/files/*', async (req, res) => {
  try {
    const reqPath = req.params[0] || '';
    const filePath = resolveFilePath(reqPath);
    await fs.unlink(filePath);
    return res.json({ ok: true, path: reqPath });
  } catch (err) {
    if (err && err.code === 'ENOENT') return res.status(404).json({ error: 'File not found' });
    const status = err && err.status ? err.status : 500;
    const message = err && err.message ? err.message : String(err);
    return res.status(status).json({ error: message });
  }
});

app.listen(PORT, async () => {
  try {
    await fs.mkdir(DATA_DIR, { recursive: true });
  } catch (e) {}
  console.log(`Mock Filesystem API listening on http://localhost:${PORT}`);
  console.log(`Data directory: ${DATA_DIR}`);
});