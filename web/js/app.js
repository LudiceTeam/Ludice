/**
 * Main Application Logic for Ludicé Telegram Mini App
 */

class LudiceApp {
    constructor() {
        this.tg = window.Telegram.WebApp;
        this.user = null;
        this.balance = 0;
        this.currentScreen = 'loading';
        this.gameState = {
            active: false,
            gameId: null,
            bet: 0,
            searching: false
        };

        this.init();
    }

    /**
     * Initialize the application
     */
    async init() {
        debug.log('Initializing Ludicé Mini App...');

        // Initialize Telegram WebApp
        this.tg.ready();
        this.tg.expand();

        // Apply Telegram theme
        this.applyTheme();

        // Get user data
        this.user = this.tg.initDataUnsafe?.user;

        if (!this.user) {
            debug.warn('No user data available');
            this.user = { id: 'test_user', first_name: 'Test User' };
        }

        debug.log('User:', this.user);

        // Setup event listeners
        this.setupEventListeners();

        // Load user data
        await this.loadUserData();

        // Show main menu
        setTimeout(() => {
            this.showScreen('main-menu');
        }, 1000);
    }

    /**
     * Apply Telegram theme colors
     */
    applyTheme() {
        const root = document.documentElement;
        const theme = this.tg.themeParams;

        if (theme.bg_color) root.style.setProperty('--tg-theme-bg-color', theme.bg_color);
        if (theme.text_color) root.style.setProperty('--tg-theme-text-color', theme.text_color);
        if (theme.hint_color) root.style.setProperty('--tg-theme-hint-color', theme.hint_color);
        if (theme.link_color) root.style.setProperty('--tg-theme-link-color', theme.link_color);
        if (theme.button_color) root.style.setProperty('--tg-theme-button-color', theme.button_color);
        if (theme.button_text_color) root.style.setProperty('--tg-theme-button-text-color', theme.button_text_color);
        if (theme.secondary_bg_color) root.style.setProperty('--tg-theme-secondary-bg-color', theme.secondary_bg_color);

        document.body.style.backgroundColor = theme.bg_color || '#ffffff';
    }

    /**
     * Setup event listeners for buttons
     */
    setupEventListeners() {
        // Main menu buttons
        document.getElementById('btn-play').addEventListener('click', () => this.showScreen('game-screen'));
        document.getElementById('btn-topup').addEventListener('click', () => this.handleTopUp());
        document.getElementById('btn-profile').addEventListener('click', () => this.showProfile());
        document.getElementById('btn-leaderboard').addEventListener('click', () => this.handleLeaderboard());

        // Game screen buttons
        document.getElementById('btn-back-game').addEventListener('click', () => this.showScreen('main-menu'));
        document.getElementById('btn-find-opponent').addEventListener('click', () => this.findOpponent());

        // Profile screen buttons
        document.getElementById('btn-back-profile').addEventListener('click', () => this.showScreen('main-menu'));

        // Telegram back button
        this.tg.BackButton.onClick(() => {
            if (this.currentScreen !== 'main-menu') {
                this.showScreen('main-menu');
            }
        });
    }

    /**
     * Show a specific screen
     */
    showScreen(screenId) {
        debug.log('Showing screen:', screenId);

        // Hide all screens
        document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));

        // Show target screen
        document.getElementById(screenId).classList.add('active');

        this.currentScreen = screenId;

        // Update Telegram back button
        if (screenId === 'main-menu') {
            this.tg.BackButton.hide();
        } else {
            this.tg.BackButton.show();
        }
    }

    /**
     * Load user data from backend
     */
    async loadUserData() {
        try {
            // TODO: Implement API call to get user balance and stats
            // For now, use placeholder data
            this.balance = 100;
            this.updateBalance();
        } catch (error) {
            debug.error('Failed to load user data:', error);
            this.tg.showAlert('Failed to load user data. Please try again.');
        }
    }

    /**
     * Update balance display
     */
    updateBalance() {
        document.getElementById('user-balance').textContent = `${this.balance} ⭐`;
    }

    /**
     * Find an opponent for the game
     */
    async findOpponent() {
        const betInput = document.getElementById('bet-amount');
        const bet = parseInt(betInput.value);

        // Validate bet
        if (!bet || bet < CONFIG.MIN_BET) {
            this.tg.showAlert(`Minimum bet is ${CONFIG.MIN_BET} ⭐`);
            return;
        }

        if (bet > this.balance) {
            this.tg.showAlert('Insufficient balance!');
            return;
        }

        try {
            debug.log('Starting game with bet:', bet);

            // Show searching status
            document.getElementById('game-status').classList.remove('hidden');
            document.querySelector('.status-text').textContent = 'Searching for opponent...';

            // Call API to start game
            const response = await api.startGame(String(this.user.id), bet);

            if (response.status === 200) {
                // Opponent found immediately
                this.gameState.gameId = response.data.replace(/"/g, '');
                this.gameState.bet = bet;
                this.gameState.active = true;

                document.querySelector('.status-text').textContent = '🎮 Opponent found! Starting game...';

                // TODO: Navigate to game play screen
                this.tg.showAlert('Game started! (Game play screen coming soon)');

            } else if (response.status === 400) {
                // Waiting for opponent
                this.gameState.gameId = response.data.detail;
                this.gameState.bet = bet;
                this.gameState.searching = true;

                document.querySelector('.status-text').textContent = '⏳ Searching for opponent...';

                // Start polling for opponent
                // TODO: Implement polling logic
            } else {
                throw new Error('Failed to start game');
            }

        } catch (error) {
            debug.error('Error finding opponent:', error);
            this.tg.showAlert('Failed to find opponent. Please try again.');
            document.getElementById('game-status').classList.add('hidden');
        }
    }

    /**
     * Handle top-up action
     */
    handleTopUp() {
        // Open Telegram payment or navigate to payment screen
        this.tg.showAlert('Payment integration coming soon!');
    }

    /**
     * Show user profile
     */
    async showProfile() {
        this.showScreen('profile-screen');

        // Update profile data
        document.getElementById('profile-name').textContent = this.user.first_name || 'User';

        // TODO: Load actual stats from backend
        document.getElementById('stat-games').textContent = '0';
        document.getElementById('stat-wins').textContent = '0';
        document.getElementById('stat-winrate').textContent = '0%';
    }

    /**
     * Handle leaderboard action
     */
    handleLeaderboard() {
        this.tg.showAlert('Leaderboard coming soon!');
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.ludiceApp = new LudiceApp();
});
