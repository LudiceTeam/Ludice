/**
 * Configuration file for Ludicé Telegram Mini App
 */

const CONFIG = {
    // Backend API URL
    API_BASE_URL: 'http://127.0.0.1:8080',

    // API Endpoints
    ENDPOINTS: {
        START_GAME: '/start/game',
        WRITE_RESULT: '/write/res',
        CANCEL_FIND: '/cancel/find',
        GET_BALANCE: '/get/balance',
        GET_STATS: '/get/stats'
    },

    // Game Settings
    MIN_BET: 10,
    MAX_BET: 1000000,

    // Polling Settings
    OPPONENT_POLL_INTERVAL: 2000, // 2 seconds
    OPPONENT_POLL_MAX_TIME: 300000, // 5 minutes

    // System Secret (should match backend)
    SYSTEM_SECRET: 'our_secret_key',

    // Debug Mode
    DEBUG: true
};

// Debug logger
const debug = {
    log: (...args) => {
        if (CONFIG.DEBUG) {
            console.log('[Ludicé]', ...args);
        }
    },
    error: (...args) => {
        if (CONFIG.DEBUG) {
            console.error('[Ludicé Error]', ...args);
        }
    },
    warn: (...args) => {
        if (CONFIG.DEBUG) {
            console.warn('[Ludicé Warning]', ...args);
        }
    }
};
