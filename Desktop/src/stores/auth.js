import { writable } from 'svelte/store';

export const token = writable(window.electronAPI.getToken());