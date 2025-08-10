// File location: vidya/client/frontend_config.js

/**
 * Configuration for the VidyaClient library.
 */
const vidyaConfig = {
    // The hostname and port for the REST API server
    apiHost: 'localhost',
    apiPort: 5000,

    // The hostname and port for the WebSocket server
    wsHost: 'localhost',
    wsPort: 8765,

    // A unique identifier for the user. In a real app, this would be
    // set after a user logs in.
    userId: 'user_A1B2C3D4',

    // Other client-side configuration options can go here
    // e.g., defaultTheme: 'dark'
};
