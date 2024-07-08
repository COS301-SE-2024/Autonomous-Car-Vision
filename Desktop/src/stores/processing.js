import { writable, get } from 'svelte/store';

// Initialize writable stores
export const processing = writable(false);
export const videoUrl = writable('');
export const originalVideoURL = writable('');
export const processingQueue = writable([]);

let isStateLoaded = false;

// Function to load state from electron-store
export async function loadState() {
    const store = window.electronAPI.loadStoreProcess(); // Ensure correct usage of electronAPI
    processing.set(store.processing);
    videoUrl.set(store.videoUrl);
    originalVideoURL.set(store.originalVideoURL);
    processingQueue.set(store.processingQueue);
    isStateLoaded = true;
}

// Function to save state to electron-store
export async function saveState(state) {
    if (isStateLoaded) { // Only save if the state has been loaded
        await window.electronAPI.saveStoreProcess(state);
        console.log("State saved:", state); // Debugging log
    }
}

// Subscribe to stores and save state on change
processing.subscribe(value => {
    if (isStateLoaded) { // Only save if the state has been loaded
        saveState({
            processing: value,
            videoUrl: get(videoUrl),
            originalVideoURL: get(originalVideoURL),
            processingQueue: get(processingQueue)
        });
    }
});

videoUrl.subscribe(value => {
    if (isStateLoaded) { // Only save if the state has been loaded
        saveState({
            processing: get(processing),
            videoUrl: value,
            originalVideoURL: get(originalVideoURL),
            processingQueue: get(processingQueue)
        });
    }
});

processingQueue.subscribe(value => {
    if (isStateLoaded) { // Only save if the state has been loaded
        saveState({
            processing: get(processing),
            videoUrl: get(videoUrl),
            originalVideoURL: get(originalVideoURL),
            processingQueue: value
        });
    }
});

originalVideoURL.subscribe(value => {
    if (isStateLoaded) { // Only save if the state has been loaded
        saveState({
            processing: get(processing),
            videoUrl: get(videoUrl),
            originalVideoURL: value,
            processingQueue: get(processingQueue)
        });
    }
});

// Load state when the module is initialized
loadState();