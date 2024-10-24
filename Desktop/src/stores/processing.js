import { writable, get } from 'svelte/store';

// Initialize writable stores
export const processing = writable(false);
export const cuda = writable(false);
export const localProcess = writable(false);
export const videoUrl = writable('');
export const originalVideoURL = writable('');
export const processingQueue = writable([]);
export const remoteProcessingQueue = writable([]);

let isStateLoaded = false;

// Function to load state from electron-store
export async function loadState() {
    const store = window.electronAPI.loadStoreProcess(); // Ensure correct usage of electronAPI
    processing.set(store.processing);
    cuda.set(store.cuda);
    localProcess.set(store.localProcess);
    videoUrl.set(store.videoUrl);
    originalVideoURL.set(store.originalVideoURL);
    processingQueue.set(store.processingQueue);
    remoteProcessingQueue.set(store.remoteProcessingQueue);
    isStateLoaded = true;
}

// Function to save state to electron-store
export async function saveState(state) {
    if (isStateLoaded) { // Only save if the state has been loaded
        await window.electronAPI.saveStoreProcess(state);
    }
}

// Subscribe to stores and save state on change
processing.subscribe(value => {
    if (isStateLoaded) { // Only save if the state has been loaded
        saveState({
            processing: value,
            cuda: get(cuda),
            localProcess: get(localProcess),
            videoUrl: get(videoUrl),
            originalVideoURL: get(originalVideoURL),
            processingQueue: get(processingQueue),
            remoteProcessingQueue: get(remoteProcessingQueue),
        });
    }
});

cuda.subscribe(value => {
    if (isStateLoaded) { // Only save if the state has been loaded
        saveState({
            processing: get(processing),
            cuda: value,
            localProcess: get(localProcess),
            videoUrl: get(videoUrl),
            originalVideoURL: get(originalVideoURL),
            processingQueue: get(processingQueue),
            remoteProcessingQueue: get(remoteProcessingQueue),
        });
    }
});

localProcess.subscribe(value => {
    if (isStateLoaded) { // Only save if the state has been loaded
        saveState({
            processing: get(processing),
            cuda: get(cuda),
            localProcess: value,
            videoUrl: get(videoUrl),
            originalVideoURL: get(originalVideoURL),
            processingQueue: get(processingQueue),
            remoteProcessingQueue: get(remoteProcessingQueue),
        });
    }
});

videoUrl.subscribe(value => {
    if (isStateLoaded) { // Only save if the state has been loaded
        saveState({
            processing: get(processing),
            cuda: get(cuda),
            localProcess: get(localProcess),
            videoUrl: value,
            originalVideoURL: get(originalVideoURL),
            processingQueue: get(processingQueue),
            remoteProcessingQueue: get(remoteProcessingQueue),
        });
    }
});

processingQueue.subscribe(value => {
    if (isStateLoaded) { // Only save if the state has been loaded
        saveState({
            processing: get(processing),
            cuda: get(cuda),
            localProcess: get(localProcess),
            videoUrl: get(videoUrl),
            originalVideoURL: get(originalVideoURL),
            processingQueue: value,
            remoteProcessingQueue: get(remoteProcessingQueue),
        });
    }
});

originalVideoURL.subscribe(value => {
    if (isStateLoaded) { // Only save if the state has been loaded
        saveState({
            processing: get(processing),
            cuda: get(cuda),
            localProcess: get(localProcess),
            videoUrl: get(videoUrl),
            originalVideoURL: value,
            processingQueue: get(processingQueue),
            remoteProcessingQueue: get(remoteProcessingQueue),
        });
    }
});

remoteProcessingQueue.subscribe(value => {
    if (isStateLoaded) { // Only save if the state has been loaded
        saveState({
            processing: get(processing),
            cuda: get(cuda),
            localProcess: get(localProcess),
            videoUrl: get(videoUrl),
            originalVideoURL: get(originalVideoURL),
            processingQueue: get(processingQueue),
            remoteProcessingQueue: value,
        });
    }
});

// Load state when the module is initialized
loadState();