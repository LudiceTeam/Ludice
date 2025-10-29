/**
 * API Client for Ludicé Backend
 * Handles all API requests with signature verification
 */

class LudiceAPI {
    constructor(baseUrl, secretKey) {
        this.baseUrl = baseUrl;
        this.secretKey = secretKey;
    }

    /**
     * Generate HMAC-SHA256 signature for API requests
     */
    async generateSignature(data) {
        const dataToSign = { ...data };
        delete dataToSign.signature;

        const dataStr = JSON.stringify(dataToSign, Object.keys(dataToSign).sort(), null, 0);

        const encoder = new TextEncoder();
        const keyData = encoder.encode(this.secretKey);
        const messageData = encoder.encode(dataStr);

        const cryptoKey = await crypto.subtle.importKey(
            'raw',
            keyData,
            { name: 'HMAC', hash: 'SHA-256' },
            false,
            ['sign']
        );

        const signature = await crypto.subtle.sign(
            'HMAC',
            cryptoKey,
            messageData
        );

        return Array.from(new Uint8Array(signature))
            .map(b => b.toString(16).padStart(2, '0'))
            .join('');
    }

    /**
     * Make a signed POST request to the backend
     */
    async post(endpoint, data) {
        try {
            // Add timestamp
            data.timestamp = Date.now() / 1000;

            // Generate signature
            data.signature = await this.generateSignature(data);

            debug.log('API Request:', endpoint, data);

            const response = await fetch(this.baseUrl + endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const responseData = await response.json().catch(() => response.text());

            debug.log('API Response:', response.status, responseData);

            return {
                status: response.status,
                data: responseData,
                ok: response.ok
            };
        } catch (error) {
            debug.error('API Error:', error);
            throw error;
        }
    }

    /**
     * Start a new game
     */
    async startGame(username, bet) {
        return await this.post(CONFIG.ENDPOINTS.START_GAME, {
            username,
            bet
        });
    }

    /**
     * Submit dice result
     */
    async submitResult(userId, gameId, result) {
        return await this.post(CONFIG.ENDPOINTS.WRITE_RESULT, {
            user_id: userId,
            game_id: gameId,
            result
        });
    }

    /**
     * Cancel opponent search
     */
    async cancelSearch(username, gameId) {
        return await this.post(CONFIG.ENDPOINTS.CANCEL_FIND, {
            username,
            id: gameId
        });
    }
}

// Initialize API client
const api = new LudiceAPI(CONFIG.API_BASE_URL, CONFIG.SYSTEM_SECRET);
