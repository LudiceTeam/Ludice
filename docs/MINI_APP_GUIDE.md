# Telegram Mini App Integration Guide

Complete guide for setting up and deploying the Ludicé Telegram Mini App.

## Overview

The Ludicé Mini App provides a modern web interface accessible directly from Telegram. It offers:
- Native-like user experience
- Automatic theme adaptation
- Real-time game updates
- Secure payment integration

## Architecture

```
┌─────────────────┐
│  Telegram App   │
│  (iOS/Android)  │
└────────┬────────┘
         │
         │ WebView
         ▼
┌─────────────────┐
│    Mini App     │
│  (HTML/CSS/JS)  │
└────────┬────────┘
         │
         │ HTTPS API
         ▼
┌─────────────────┐
│  Backend API    │
│   (FastAPI)     │
└─────────────────┘
```

## 📋 Prerequisites

- HTTPS-enabled web server (required by Telegram)
- Telegram Bot with admin access
- Backend API running and accessible

## 🚀 Quick Setup

### 1. Configure Web Server

#### Option A: Nginx (Production)

```nginx
server {
    listen 443 ssl http2;
    server_name ludice.example.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    location / {
        root /var/www/ludice/web;
        index index.html;
        try_files $uri $uri/ /index.html;

        # Enable gzip
        gzip on;
        gzip_types text/css application/javascript application/json;
    }

    # API proxy (optional)
    location /api/ {
        proxy_pass http://localhost:8080/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

#### Option B: Caddy (Simple)

```caddy
ludice.example.com {
    root * /var/www/ludice/web
    file_server
    encode gzip

    # API proxy
    reverse_proxy /api/* localhost:8080
}
```

#### Option C: Development with ngrok

```bash
# Start local server
cd web
python -m http.server 8000

# In another terminal
ngrok http 8000 --domain=your-subdomain.ngrok-free.app
```

### 2. Update Configuration

Edit `web/js/config.js`:

```javascript
const CONFIG = {
    // Production API URL
    API_BASE_URL: 'https://api.ludice.example.com',

    // Same secret as backend
    SYSTEM_SECRET: 'your_secret_key_here',

    // Disable debug in production
    DEBUG: false,

    // Other settings...
};
```

### 3. Configure CORS on Backend

Update your FastAPI backend to allow Mini App domain:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ludice.example.com",
        "https://your-subdomain.ngrok-free.app",  # For development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4. Set Bot Menu Button

Add the Mini App to your bot's menu:

```python
from aiogram import Bot
from aiogram.types import MenuButtonWebApp, WebAppInfo

bot = Bot(token="YOUR_BOT_TOKEN")

# Set menu button
await bot.set_chat_menu_button(
    menu_button=MenuButtonWebApp(
        text="🎲 Play Game",
        web_app=WebAppInfo(url="https://ludice.example.com")
    )
)
```

Or use BotFather:
1. Send `/mybots` to @BotFather
2. Select your bot
3. Choose "Bot Settings" → "Menu Button"
4. Enter URL: `https://ludice.example.com`
5. Enter button text: `🎲 Play Game`

## 🎨 Customization

### Theme Colors

The Mini App automatically adapts to the user's Telegram theme. You can customize additional colors in `web/css/style.css`:

```css
:root {
    /* Custom brand colors */
    --primary-color: #2481cc;
    --success-color: #4caf50;
    --danger-color: #f44336;
    --warning-color: #ff9800;

    /* Override Telegram colors if needed */
    --tg-theme-button-color: #2481cc;
}
```

### Adding New Screens

1. Add HTML in `index.html`:

```html
<div id="my-screen" class="screen">
    <div class="container">
        <h2>My Screen</h2>
        <!-- Content here -->
    </div>
</div>
```

2. Add navigation in `app.js`:

```javascript
handleMyScreen() {
    this.showScreen('my-screen');
    // Load screen data...
}
```

3. Add event listener:

```javascript
document.getElementById('btn-my-screen')
    .addEventListener('click', () => this.handleMyScreen());
```

### Adding API Endpoints

1. Add endpoint in `web/js/api.js`:

```javascript
async myNewEndpoint(data) {
    return await this.post('/my/endpoint', {
        ...data,
        user_id: this.userId
    });
}
```

2. Use in `app.js`:

```javascript
async loadMyData() {
    const response = await api.myNewEndpoint({ param: 'value' });
    if (response.ok) {
        // Handle response
    }
}
```

## 🔐 Security

### Request Signing

All API requests from the Mini App are signed with HMAC-SHA256:

```javascript
// In api.js
async generateSignature(data) {
    // Remove signature field
    const dataToSign = { ...data };
    delete dataToSign.signature;

    // Sort and stringify
    const dataStr = JSON.stringify(
        dataToSign,
        Object.keys(dataToSign).sort()
    );

    // Generate HMAC-SHA256
    const encoder = new TextEncoder();
    const keyData = encoder.encode(this.secretKey);
    const messageData = encoder.encode(dataStr);

    const cryptoKey = await crypto.subtle.importKey(
        'raw', keyData,
        { name: 'HMAC', hash: 'SHA-256' },
        false, ['sign']
    );

    const signature = await crypto.subtle.sign(
        'HMAC', cryptoKey, messageData
    );

    return Array.from(new Uint8Array(signature))
        .map(b => b.toString(16).padStart(2, '0'))
        .join('');
}
```

### User Authentication

User identity is verified via Telegram WebApp initData:

```javascript
// Get user data from Telegram
const user = window.Telegram.WebApp.initDataUnsafe?.user;

// Include in API requests
const response = await api.post('/endpoint', {
    user_id: user.id,
    // ... other data
});
```

### HTTPS Requirement

Telegram requires HTTPS for Mini Apps. Use:
- Valid SSL certificate (Let's Encrypt is free)
- Or ngrok for development
- Never use HTTP in production

## 📱 Testing

### Local Testing

1. **Start local server:**
```bash
cd web
python -m http.server 8000
```

2. **Create HTTPS tunnel:**
```bash
ngrok http 8000
```

3. **Update bot menu button** with ngrok URL

4. **Test in Telegram:**
   - Open your bot
   - Click the menu button
   - Mini App should load

### Testing Checklist

- [ ] Mini App loads without errors
- [ ] Theme adapts to light/dark mode
- [ ] All buttons work correctly
- [ ] API requests are signed correctly
- [ ] Error handling works
- [ ] Back button navigation works
- [ ] Payment flow works (if applicable)
- [ ] Responsive on different screen sizes
- [ ] Works on iOS and Android
- [ ] Works in Telegram Desktop

### Debug Mode

Enable debug logging in `config.js`:

```javascript
const CONFIG = {
    DEBUG: true
};
```

Check browser console (F12) for logs:
```
[Ludicé] Initializing Mini App...
[Ludicé] User: {id: 123, first_name: "John"}
[Ludicé] API Request: /start/game {...}
[Ludicé] API Response: 200 {...}
```

## 🚀 Deployment

### Pre-deployment Checklist

- [ ] Update `API_BASE_URL` in config.js
- [ ] Set `DEBUG: false` in config.js
- [ ] Configure CORS on backend
- [ ] Set up HTTPS certificate
- [ ] Test in production-like environment
- [ ] Verify security headers
- [ ] Enable gzip compression
- [ ] Set cache headers for static assets

### Deploy to Production

1. **Build assets (if using bundler):**
```bash
cd web
npm run build  # if applicable
```

2. **Upload to server:**
```bash
rsync -avz web/ user@server:/var/www/ludice/web/
```

3. **Update bot menu button** with production URL

4. **Test thoroughly** on all platforms

### Continuous Deployment

Use GitHub Actions (see `.github/workflows/deploy.yml`):

```yaml
- name: Deploy Mini App
  run: |
    rsync -avz web/ ${{ secrets.DEPLOY_USER }}@${{ secrets.DEPLOY_HOST }}:/var/www/ludice/web/
```

## 🐛 Troubleshooting

### Mini App Not Loading

**Symptom:** Blank screen or loading forever

**Solutions:**
- Check browser console for errors
- Verify HTTPS is enabled
- Check CORS configuration
- Ensure `telegram-web-app.js` loads

### API Requests Failing

**Symptom:** 403 errors or CORS errors

**Solutions:**
- Verify API_BASE_URL in config.js
- Check CORS allowed origins on backend
- Verify signature generation matches backend
- Check network tab in browser dev tools

### Theme Not Applying

**Symptom:** Wrong colors or theme

**Solutions:**
- Ensure `Telegram.WebApp.ready()` is called
- Check theme params in console
- Verify CSS variables are set correctly

### Payment Not Working

**Symptom:** Payment flow fails

**Solutions:**
- Telegram Stars must be enabled for your bot
- Test with small amounts first
- Check payment provider configuration
- Verify webhook configuration

## 📚 Resources

- [Telegram Mini Apps Documentation](https://core.telegram.org/bots/webapps)
- [WebApp SDK Reference](https://core.telegram.org/bots/webapps#initializing-mini-apps)
- [Design Guidelines](https://core.telegram.org/bots/webapps#design-guidelines)
- [Best Practices](https://core.telegram.org/bots/webapps#best-practices)

## 🎯 Best Practices

1. **Keep it lightweight** - Minimize JS and CSS
2. **Progressive enhancement** - Core functionality without JS
3. **Responsive design** - Works on all screen sizes
4. **Native-like UX** - Follow Telegram design patterns
5. **Error handling** - Graceful fallbacks for all errors
6. **Security first** - Always validate and sign requests
7. **Performance** - Lazy load non-critical resources
8. **Testing** - Test on real devices, not just emulators

## 🔄 Updates

To update the Mini App after deployment:

1. Make changes to files in `web/`
2. Test locally with ngrok
3. Deploy to production
4. Users will get updates on next Mini App load
5. No need to update bot or backend (unless API changes)

---

**Need help?** Check our [Discord](https://discord.gg/ludice) or [open an issue](https://github.com/yourusername/Ludice/issues).
