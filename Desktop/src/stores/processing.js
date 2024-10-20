import { writable, get } from 'svelte/store';

export const processing = writable(false);
export const cuda = writable(false);
export const localProcess = writable(false);
export const videoUrl = writable('');
export const originalVideoURL = writable('');
export const processingQueue = writable([]);
export const remoteProcessingQueue = writable([]);

let isStateLoaded = false;

export async function loadState() {
    const store = window.electronAPI.loadStoreProcess(); 
    processing.set(store.processing);
    cuda.set(store.cuda);
    localProcess.set(store.localProcess);
    videoUrl.set(store.videoUrl);
    originalVideoURL.set(store.originalVideoURL);
    processingQueue.set(store.processingQueue);
    remoteProcessingQueue.set(store.remoteProcessingQueue);
    isStateLoaded = true;
}

export async function saveState(state) {
    if (isStateLoaded) { 
        await window.electronAPI.saveStoreProcess(state);
    }
}

processing.subscribe(value => {
    if (isStateLoaded) { 
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
    if (isStateLoaded) { 
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
    if (isStateLoaded) { 
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
    if (isStateLoaded) { 
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
    if (isStateLoaded) { 
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
    if (isStateLoaded) { 
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
    if (isStateLoaded) { 
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

loadState();