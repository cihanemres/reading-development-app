/**
 * Error Handler
 * Centralized error handling with user-friendly messages
 */
const ErrorHandler = {
    /**
     * Error message mappings (Turkish)
     */
    errorMessages: {
        // HTTP Status Codes
        400: {
            title: 'Geçersiz İstek',
            message: 'Gönderilen bilgiler hatalı. Lütfen kontrol edin.'
        },
        401: {
            title: 'Oturum Süresi Doldu',
            message: 'Lütfen tekrar giriş yapın.',
            action: 'redirect',
            redirectTo: '../login.html'
        },
        403: {
            title: 'Yetkisiz İşlem',
            message: 'Bu işlem için yetkiniz yok.'
        },
        404: {
            title: 'Bulunamadı',
            message: 'Aradığınız içerik bulunamadı.'
        },
        500: {
            title: 'Sunucu Hatası',
            message: 'Bir sorun oluştu. Lütfen daha sonra tekrar deneyin.',
            action: 'retry'
        },
        503: {
            title: 'Hizmet Kullanılamıyor',
            message: 'Sunucu şu anda bakımda. Lütfen daha sonra tekrar deneyin.'
        },
        // Network Errors
        'NetworkError': {
            title: 'Bağlantı Hatası',
            message: 'İnternet bağlantınızı kontrol edin.',
            action: 'retry'
        },
        'TimeoutError': {
            title: 'Zaman Aşımı',
            message: 'İşlem çok uzun sürdü. Lütfen tekrar deneyin.',
            action: 'retry'
        },
        // Default
        'default': {
            title: 'Hata',
            message: 'Bir hata oluştu. Lütfen tekrar deneyin.',
            action: 'retry'
        }
    },

    /**
     * Show error message to user
     * @param {Object} error - Error object or config
     */
    showError(error) {
        const errorConfig = this.parseError(error);

        // Create or update error boundary
        let errorBoundary = document.getElementById('errorBoundary');
        if (!errorBoundary) {
            errorBoundary = this.createErrorBoundary();
            document.body.appendChild(errorBoundary);
        }

        // Update content
        document.getElementById('errorTitle').textContent = errorConfig.title;
        document.getElementById('errorMessage').textContent = errorConfig.message;

        // Handle action button
        const actionBtn = document.getElementById('errorAction');
        if (errorConfig.action === 'retry' && errorConfig.retryFn) {
            actionBtn.textContent = 'Tekrar Dene';
            actionBtn.onclick = () => {
                this.dismissError();
                errorConfig.retryFn();
            };
            actionBtn.classList.remove('hidden');
        } else if (errorConfig.action === 'redirect') {
            actionBtn.textContent = 'Giriş Yap';
            actionBtn.onclick = () => {
                window.location.href = errorConfig.redirectTo;
            };
            actionBtn.classList.remove('hidden');
        } else {
            actionBtn.classList.add('hidden');
        }

        // Show error
        errorBoundary.classList.remove('hidden');
        errorBoundary.classList.add('fade-in');

        // Auto-dismiss after 5 seconds (unless persistent)
        if (!errorConfig.persistent) {
            setTimeout(() => this.dismissError(), 5000);
        }

        // Log error
        this.logError(error, errorConfig);
    },

    /**
     * Parse error into config object
     * @param {*} error - Error to parse
     * @returns {Object} Error config
     */
    parseError(error) {
        // If already a config object
        if (error.title && error.message) {
            return error;
        }

        // If HTTP response
        if (error.status) {
            const config = this.errorMessages[error.status] || this.errorMessages.default;
            return { ...config, originalError: error };
        }

        // If error type
        if (error.type) {
            const config = this.errorMessages[error.type] || this.errorMessages.default;
            return { ...config, originalError: error };
        }

        // If Error object
        if (error instanceof Error) {
            return {
                ...this.errorMessages.default,
                message: error.message,
                originalError: error
            };
        }

        // Default
        return this.errorMessages.default;
    },

    /**
     * Handle API errors
     * @param {Response} response - Fetch response
     * @param {string} operation - Operation description
     * @returns {Object} Error object
     */
    async handleApiError(response, operation = '') {
        let errorData = null;

        try {
            errorData = await response.json();
        } catch (e) {
            // Response not JSON
        }

        const error = {
            status: response.status,
            statusText: response.statusText,
            operation: operation,
            data: errorData
        };

        // Show error to user
        this.showError(error);

        return error;
    },

    /**
     * Retry operation with exponential backoff
     * @param {Function} fn - Function to retry
     * @param {number} maxRetries - Maximum retry attempts
     * @param {number} delay - Initial delay in ms
     * @returns {Promise} Result of operation
     */
    async retryOperation(fn, maxRetries = 3, delay = 1000) {
        for (let i = 0; i < maxRetries; i++) {
            try {
                return await fn();
            } catch (error) {
                if (i === maxRetries - 1) {
                    throw error;
                }

                // Exponential backoff
                const waitTime = delay * Math.pow(2, i);
                console.log(`Retry ${i + 1}/${maxRetries} after ${waitTime}ms...`);
                await new Promise(resolve => setTimeout(resolve, waitTime));
            }
        }
    },

    /**
     * Check network status
     * @returns {boolean} Online status
     */
    checkNetworkStatus() {
        return navigator.onLine;
    },

    /**
     * Dismiss error message
     */
    dismissError() {
        const errorBoundary = document.getElementById('errorBoundary');
        if (errorBoundary) {
            errorBoundary.classList.add('hidden');
            errorBoundary.classList.remove('fade-in');
        }
    },

    /**
     * Create error boundary HTML
     * @returns {HTMLElement} Error boundary element
     */
    createErrorBoundary() {
        const div = document.createElement('div');
        div.id = 'errorBoundary';
        div.className = 'hidden fixed top-4 right-4 z-50 max-w-md';
        div.innerHTML = `
            <div class="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg shadow-lg">
                <div class="flex items-start">
                    <i class="fas fa-exclamation-circle text-red-500 text-xl mr-3 mt-1"></i>
                    <div class="flex-1">
                        <h4 class="font-bold text-red-800" id="errorTitle">Hata</h4>
                        <p class="text-red-700 text-sm mt-1" id="errorMessage"></p>
                        <div class="mt-3 flex space-x-2">
                            <button id="errorAction" 
                                class="hidden bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700 transition">
                                Tekrar Dene
                            </button>
                            <button onclick="ErrorHandler.dismissError()" 
                                class="text-red-600 hover:text-red-800 text-sm font-semibold">
                                Kapat
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        return div;
    },

    /**
     * Log error for debugging
     * @param {*} error - Error to log
     * @param {Object} config - Error config
     */
    logError(error, config) {
        const isDev = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';

        if (isDev) {
            console.group('🔴 Error Handler');
            console.error('Title:', config.title);
            console.error('Message:', config.message);
            console.error('Original Error:', config.originalError || error);
            console.groupEnd();
        }
    },

    /**
     * Initialize network status monitoring
     */
    initNetworkMonitor() {
        window.addEventListener('online', () => {
            if (window.LoadingUtils) {
                LoadingUtils.showToast('Bağlantı yeniden kuruldu', 'success');
            }
            this.dismissError();
        });

        window.addEventListener('offline', () => {
            this.showError({
                title: 'Bağlantı Kesildi',
                message: 'İnternet bağlantınız yok. Bazı özellikler çalışmayabilir.',
                persistent: true
            });
        });
    }
};

// Auto-initialize
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        ErrorHandler.initNetworkMonitor();
        console.log('ErrorHandler initialized');
    });
} else {
    ErrorHandler.initNetworkMonitor();
    console.log('ErrorHandler initialized');
}
