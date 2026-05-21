/**
 * Telemetry System Configuration
 *
 * Single service deployment:
 * - Uses same origin for both frontend and API
 * - Works on localhost:8000 (local)
 * - Works on Render domain (production)
 * - No configuration needed!
 */

// API URL = Current location origin
// This works everywhere - localhost, Render, custom domains
const API_URL = window.location.origin;
