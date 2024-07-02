import { writable, get } from 'svelte/store';

// Initialize writable stores
export const processing = writable(false);
export const videoUrl = writable('');
export const processingQueue = writable([]);

// Function to load state from electron-store
export async function loadState() {
    const store = await window.electronAPI.loadStoreProcess(); // Ensure correct usage of electronAPI
    processing.set(store.processing);
    videoUrl.set(store.videoUrl);
    processingQueue.set(store.processingQueue);
}

// Function to save state to electron-store
export async function saveState(state) {
    await window.electronAPI.saveStoreProcess(state); // Ensure correct usage of electronAPI
}

// Subscribe to stores and save state on change
processing.subscribe(value => saveState({
    processing: value,
    videoUrl: get(videoUrl),
    processingQueue: get(processingQueue)
}));

videoUrl.subscribe(value => saveState({
    processing: get(processing),
    videoUrl: value,
    processingQueue: get(processingQueue)
}));

processingQueue.subscribe(value => saveState({
    processing: get(processing),
    videoUrl: get(videoUrl),
    processingQueue: value
}));

// Load state when the module is initialized
loadState();