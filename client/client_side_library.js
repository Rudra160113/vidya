// File location: vidya/client/client_side_library.js

/**
 * A client-side library for interacting with the Vidya AI backend.
 * This library handles API calls and WebSocket communication.
 */
class VidyaClient {
    constructor(config) {
        this.config = config;
        this.apiBaseUrl = `http://${config.apiHost}:${config.apiPort}`;
        this.wsUrl = `ws://${config.wsHost}:${config.wsPort}`;
        this.ws = null;
        this.userId = config.userId || 'anonymous';
        console.log("VidyaClient initialized.");
    }

    /**
     * Sends a text query to the Vidya REST API and gets a response.
     * @param {string} text - The user's text query.
     * @returns {Promise<string>} - The AI's response.
     */
    async sendQuery(text) {
        const url = `${this.apiBaseUrl}/api/query`;
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text, user_id: this.userId })
            });
            const data = await response.json();
            if (response.ok) {
                return data.response;
            } else {
                throw new Error(data.error || 'API request failed');
            }
        } catch (error) {
            console.error("Error sending query:", error);
            return `An error occurred: ${error.message}`;
        }
    }

    /**
     * Establishes a WebSocket connection for real-time communication.
     * @param {function} onMessageCallback - Callback for incoming messages.
     * @param {function} onErrorCallback - Callback for connection errors.
     */
    connectWebSocket(onMessageCallback, onErrorCallback) {
        this.ws = new WebSocket(this.wsUrl);

        this.ws.onopen = () => {
            console.log("WebSocket connected.");
        };

        this.ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            onMessageCallback(message);
        };

        this.ws.onerror = (error) => {
            console.error("WebSocket error:", error);
            if (onErrorCallback) {
                onErrorCallback(error);
            }
        };

        this.ws.onclose = () => {
            console.log("WebSocket disconnected.");
        };
    }
}
