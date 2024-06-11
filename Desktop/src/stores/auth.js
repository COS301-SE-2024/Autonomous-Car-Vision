import { writable } from 'svelte/store';

// export const isAuthenticated = writable(false);

// export function checkAuth() {
//   const token = window.electronAPI.getToken();
//   isAuthenticated.set(!!token); // Set to true if token exists, false otherwise
// }

export const token = writable(window.electronAPI.getToken());