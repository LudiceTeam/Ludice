# Ludicé Telegram Mini App

This is the web interface for the Ludicé dice game, designed to run as a Telegram Mini App.

## 📁 Structure

```
web/
├── index.html          # Main HTML file
├── css/
│   └── style.css       # Styles with Telegram theme support
├── js/
│   ├── config.js       # Configuration and settings
│   ├── api.js          # API client for backend communication
│   └── app.js          # Main application logic
├── assets/             # Images, icons, etc.
└── README.md          # This file
```

## 🚀 Features

- ✅ Telegram WebApp SDK integration
- ✅ Automatic theme adaptation (light/dark mode)
- ✅ HMAC-SHA256 request signing
- ✅ Responsive design for all mobile devices
- ✅ Native-like animations and transitions
- ✅ Game lobby and matchmaking UI
- ✅ User profile and statistics

## 🛠️ Setup

### 1. Configure the Bot

Add a menu button to your Telegram bot that opens the Mini App:

```python
from aiogram.types import MenuButtonWebApp, WebAppInfo

# Set menu button
await bot.set_chat_menu_button(
    menu_button=MenuButtonWebApp(
        text="Play Game",
        web_app=WebAppInfo(url="https://yourdomain.com/web/")
    )
)
```

### 2. Host the Web Files

You can host the Mini App using:

**Option A: Simple HTTP Server (Development)**
```bash
cd web
python3 -m http.server 8000
```

**Option B: Nginx (Production)**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /web/ {
        alias /path/to/Ludice/web/;
        index index.html;
    }
}
```

**Option C: GitHub Pages**
1. Push the `web/` folder to a GitHub repository
2. Enable GitHub Pages in repository settings
3. Use the provided URL in your bot

### 3. Update Configuration

Edit `js/config.js` and update:

```javascript
const CONFIG = {
    API_BASE_URL: 'https://your-backend-api.com',
    SYSTEM_SECRET: 'your_secret_key',
    DEBUG: false  // Set to false in production
};
```

### 4. CORS Configuration

Ensure your backend API allows requests from the Mini App domain:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🎨 Telegram Theme

The Mini App automatically adapts to the user's Telegram theme (light/dark mode). Theme colors are applied via CSS variables:

- `--tg-theme-bg-color`
- `--tg-theme-text-color`
- `--tg-theme-button-color`
- etc.

## 🔐 Security

- All API requests are signed with HMAC-SHA256
- User authentication via Telegram WebApp initData
- Timestamp validation prevents replay attacks
- Secrets are configured server-side

## 📱 Testing

### Local Testing

1. Start the web server:
   ```bash
   cd web
   python3 -m http.server 8000
   ```

2. Use ngrok for HTTPS tunnel:
   ```bash
   ngrok http 8000
   ```

3. Update bot menu button with ngrok URL

4. Open bot in Telegram and click the menu button

### Production Testing

1. Deploy to your hosting
2. Update bot configuration with production URL
3. Test in Telegram app (iOS/Android/Desktop)

## 🔧 Development

### Adding New Screens

1. Add HTML in `index.html`:
```html
<div id="new-screen" class="screen">
    <!-- Content here -->
</div>
```

2. Add navigation in `app.js`:
```javascript
showNewScreen() {
    this.showScreen('new-screen');
}
```

### Styling

Follow Telegram's design guidelines:
- Use native-like components
- Respect theme colors
- Keep touch targets >= 44px
- Use system fonts

### API Integration

Add new endpoints in `api.js`:

```javascript
async myNewEndpoint(data) {
    return await this.post('/my/endpoint', data);
}
```

## 📚 Resources

- [Telegram Mini Apps Documentation](https://core.telegram.org/bots/webapps)
- [WebApp SDK Reference](https://core.telegram.org/bots/webapps#initializing-mini-apps)
- [Design Guidelines](https://core.telegram.org/bots/webapps#design-guidelines)

## 🐛 Troubleshooting

### Mini App not loading
- Check HTTPS is enabled (required by Telegram)
- Verify CORS configuration
- Check browser console for errors

### Theme not applying
- Ensure `telegram-web-app.js` is loaded first
- Call `Telegram.WebApp.ready()` on initialization

### API requests failing
- Verify backend URL in `config.js`
- Check CORS settings on backend
- Ensure signature generation matches backend

## 🎯 TODO

- [ ] Implement real-time game play screen
- [ ] Add WebSocket for live updates
- [ ] Implement leaderboard
- [ ] Add sound effects
- [ ] Add haptic feedback
- [ ] Implement payment integration
- [ ] Add animations for dice rolling
- [ ] Multi-language support

## 📄 License

Part of the Ludicé project.
