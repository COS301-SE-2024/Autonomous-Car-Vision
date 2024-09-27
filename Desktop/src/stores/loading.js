import { writable } from 'svelte/store';

export const isLoading = writable(false);
export const isDownloading = writable(false);
export const isProcessing = writable(false);
