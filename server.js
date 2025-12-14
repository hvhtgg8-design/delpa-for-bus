import express from "express";
import fetch from "node-fetch";
import crypto from "crypto";

const app = express();
app.use(express.json());

// In-memory storage for device tokens and users (replace with DB for production)
const devices = new Map(); // token -> { userId, created }
const users = new Map();   // userId -> { provider, linked }

// OAuth Credentials
const GITHUB_CLIENT_ID = "YOUR_GITHUB_CLIENT_ID";
const GITHUB_CLIENT_SECRET = "YOUR_GITHUB_CLIENT_SECRET";
const GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID";
const GOOGLE_CLIENT_SECRET = "YOUR_GOOGLE_CLIENT_SECRET";

// Helper: generate device token
function createDeviceToken(userId) {
  const token = crypto.randomBytes(32).toString("hex");
  devices.set(token, { userId, created: Date.now() });
  return token;
}

// --- GitHub OAuth ---
app.get("/oauth/github/callback", async (req, res) => {
  const { code } = req.query;

  const tokenRes = await fetch("https://github.com/login/oauth/access_token", {
    method: "POST",
    headers: { Accept: "application/json" },
    body: new URLSearchParams({
      client_id: GITHUB_CLIENT_ID,
      client_secret: GITHUB_CLIENT_SECRET,
      code
    })
  }).then(r => r.json());

  const user = await fetch("https://api.github.com/user", {
    headers: { Authorization: `Bearer ${tokenRes.access_token}` }
  }).then(r => r.json());

  const userId = `github:${user.id}`;
  users.set(userId, { provider: "github", linked: true });

  const deviceToken = createDeviceToken(userId);
  res.json({ provider: "github", id: user.id, deviceToken });
});

// --- Google OAuth ---
app.get("/oauth/google/callback", async (req, res) => {
  const { code } = req.query;

  const tokenRes = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      client_id: GOOGLE_CLIENT_ID,
      client_secret: GOOGLE_CLIENT_SECRET,
      code,
      grant_type: "authorization_code",
      redirect_uri: "http://localhost:3000/oauth/google/callback"
    })
  }).then(r => r.json());

  const user = await fetch(
    "https://www.googleapis.com/oauth2/v3/userinfo",
    { headers: { Authorization: `Bearer ${tokenRes.access_token}` } }
  ).then(r => r.json());

  const userId = `google:${user.sub}`;
  users.set(userId, { provider: "google", linked: true });

  const deviceToken = createDeviceToken(userId);
  res.json({ provider: "google", id: user.sub, deviceToken });
});

// --- Validate device token ---
app.post("/device/validate", (req, res) => {
  const { token } = req.body;
  if (devices.has(token)) {
    res.json({ valid: true, userId: devices.get(token).userId });
  } else {
    res.json({ valid: false });
  }
});

// --- List devices for a user ---
app.post("/device/list", (req, res) => {
  const { userId } = req.body;
  const userDevices = [];
  devices.forEach((v, k) => {
    if (v.userId === userId) userDevices.push({ token: k, created: v.created });
  });
  res.json({ devices: userDevices });
});

// --- Remove device ---
app.post("/device/remove", (req, res) => {
  const { token } = req.body;
  if (devices.has(token)) {
    devices.delete(token);
    res.json({ removed: true });
  } else {
    res.json({ removed: false });
  }
});

app.listen(3000, () => console.log("Auth backend running on http://localhost:3000"));