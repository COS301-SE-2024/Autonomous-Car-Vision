const { app, BrowserWindow, ipcMain, dialog, View, contextBridge } = require('electron');
const { spawn } = require('child_process');
const path = require('path');
const crypto = require('crypto');
const fs = require('fs');
const { LookupTable, AIModels, VideoTable } = require('./database');
const axios = require('axios');
const FormData = require('form-data')
const { Sequelize } = require('sequelize');
const ffmpegFluent = require('fluent-ffmpeg');
const ffmpegPath = require('ffmpeg-static');
const ffprobePath = require('ffprobe-static').path;
const { OAuth2Client } = require('google-auth-library');
const http = require('http');
const dotenv = require('dotenv');

require('dotenv').config();

let envPath = path.join(app.getAppPath(), '.env');
if (fs.existsSync(envPath)) {
    dotenv.config({ path: envPath });
}

const os = require('os');
const { Worker, isMainThread } = require('worker_threads');
const { getVideoFiles } = require('./videoScanner');
const { getJsonData } = require('./getJsonData');

const HOST_IP = process.env.HOST_IP;

let mainWindow;
let store;
let base_directory = '';

async function loadElectronStore() {
    const { default: Store } = await import('electron-store');
    return new Store();
}


async function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1080,
        height: 720,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            enableRemoteModule: false,
            webviewTag: true,
            nodeIntegration: true,
            webSecurity: false,
        },
        autoHideMenuBar: true,
        icon: path.join(__dirname, 'assets', 'HighViz(transparent)-white.png'),
    });

    mainWindow.loadFile('public/index.html');

    if (app.isPackaged) {
        mainWindow.webContents.on('devtools-opened', () => {
            mainWindow.webContents.closeDevTools();
        });

        mainWindow.webContents.on('context-menu', (e) => {
            e.preventDefault();
        });
    }
    store = await loadElectronStore();
}

app.whenReady().then(() => {
    createWindow();
    if (process.defaultApp) {
        if (process.argv.length >= 2) {
            app.setAsDefaultProtocolClient('myapp', process.execPath, [path.resolve(process.argv[1])])
        }
    } else {
        app.setAsDefaultProtocolClient('myapp')
    }
});

app.on('ready', () => {
    const { session } = require('electron');
    session.defaultSession.webRequest.onBeforeRequest((details, callback) => {
        if (details.url.includes('devtools://')) {
            callback({ cancel: false });
        } else {
            callback({ cancel: false });
        }
    });
});

app.on('open-url', (event, url) => {
    event.preventDefault();
    handleAuthCallback(url);
});

app.on('open-external', (event, url) => {
    event.preventDefault();
    console.log('Open external:', url);
    handleAuthCallback(url);
});


app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

const AdmZip = require('adm-zip');

function extractPythonFiles(pythonFile) {
    const appDataDir = path.join(getBaseDirectory(), 'python-scripts');
    const zipPath = path.join(app.getAppPath(), 'python.zip');

    console.log(`Zip Path: ${zipPath}`);
    console.log(`App Data Directory: ${appDataDir}`);

    if (!fs.existsSync(appDataDir)) {
        fs.mkdirSync(appDataDir, { recursive: true });
    }

    const zip = new AdmZip(zipPath);

    let extractedScriptPath;
    if(pythonFile === "cudaCheck.py") {
        extractedScriptPath = path.join(appDataDir, 'python', pythonFile);    
    }else {   
        extractedScriptPath = path.join(appDataDir, pythonFile);
    }

    if (fs.existsSync(extractedScriptPath)) {
        console.log(`Python script already extracted at: ${extractedScriptPath}`);
        return appDataDir;
    }

    zip.extractAllTo(appDataDir, true);

    if (fs.existsSync(extractedScriptPath)) {
        console.log(`Python script found at: ${extractedScriptPath}`);
    } else {
        console.error(`Python script NOT found at: ${extractedScriptPath}`);
    }

    return appDataDir;
}

ipcMain.handle('get-app-path', () => {
    return getBaseDirectory();
});

ipcMain.handle('read-directory', async (event, directoryPath) => {
    return new Promise((resolve, reject) => {
        fs.readdir(directoryPath, (err, files) => {
            if (err) {
                reject(err);
            } else {
                resolve(files);
            }
        });
    });
});

function getBaseDirectory() {
    if (os.platform() === 'win32') {
        base_directory = path.join(process.env.APPDATA, 'HVstore');
    } else if (os.platform() === 'linux') {
        base_directory = path.join(os.homedir(), '.local', 'share', 'HVstore');
    }
    return base_directory;
}

ipcMain.handle('get-host-ip', async (event) => {
    return process.env.HOST_IP;
});

//! token
ipcMain.on('store-token', (event, token) => {
    store.set('authToken', token);
    event.returnValue = true;
});

ipcMain.on('get-token', (event) => {
    const token = store.get('authToken');
    event.returnValue = token;
});

ipcMain.on('clear-token', (event) => {
    store.delete('authToken');
    event.returnValue = true;
});

//! uname
ipcMain.on('store-uname', (event, uname) => {
    store.set('uname', uname);
    event.returnValue = true;
});

ipcMain.on('get-uname', (event) => {
    const uname = store.get('uname');
    event.returnValue = uname;
});

ipcMain.on('clear-uname', (event) => {
    store.delete('uname');
    event.returnValue = true;
});

//! uid
ipcMain.on('store-uid', (event, uid) => {
    store.set('uid', uid);
    event.returnValue = true;
});

ipcMain.on('get-uid', (event) => {
    const uid = store.get('uid');
    event.returnValue = uid;
});

ipcMain.on('clear-uid', (event) => {
    store.delete('uid');
    event.returnValue = true;
});

//! uemail
ipcMain.on('store-uemail', (event, uemail) => {
    store.set('uemail', uemail);
    event.returnValue = true;
});

ipcMain.on('get-uemail', (event) => {
    const uemail = store.get('uemail');
    event.returnValue = uemail;
});

ipcMain.on('clear-uemail', (event) => {
    store.delete('uemail');
    event.returnValue = true;
});

//! prevPath
ipcMain.on('store-prev-path', (event, prevPath) => {
    store.set('prevPath', prevPath);
    event.returnValue = true;
});

ipcMain.on('get-prev-path', (event) => {
    const prevPath = store.get('prevPath');
    event.returnValue = prevPath;
});

ipcMain.on('clear-prev-path', (event) => {
    store.delete('prevPath');
    event.returnValue = true;
});

//! Team Name
ipcMain.on('store-team-name', (event, teamName) => {
    store.set('teamName', teamName);
    event.returnValue = true;
});

ipcMain.on('get-team-name', (event) => {
    const teamName = store.get('teamName');
    event.returnValue = teamName;
});

ipcMain.on('clear-team-name', (event) => {
    store.delete('teamName');
    event.returnValue = true;
});

ipcMain.on('load-store-process', (event) => {
    const storeData = store.get('appProcessing', {
        processing: false,
        cuda: false,
        localProcess: false,
        videoUrl: '',
        originalVideoURL: '',
        processingQueue: [],
        remoteProcessingQueue: []
    });
    event.returnValue = storeData;
});

ipcMain.handle('save-store-process', async (event, state) => {
    store.set('appProcessing', state);
});

function updateState(updates) {
    const currentState = store.get('appProcessing', {
        processing: false,
        cuda: false,
        localProcess: true,
        videoUrl: '',
        originalVideoURL: '',
        processingQueue: [],
        remoteProcessingQueue: []
    });
    const newState = { ...currentState, ...updates };
    console.log('Updated state:', newState);
    store.set('appProcessing', newState);
    mainWindow.webContents.send('process-changed');
    return newState;
}

ipcMain.handle('hash-password', async (event, password) => {
    const salt = crypto.randomBytes(16).toString('hex');
    const hash = crypto.scryptSync(password, salt, 64).toString('hex');
    return { hash, salt };
});

ipcMain.handle('hash-password-salt', async (event, password, salt) => {
    if (typeof salt !== 'string') {
        throw new TypeError('The "salt" argument must be of type string.');
    }
    const hash = crypto.scryptSync(password, salt, 64).toString('hex');
    return { hash };
});
ipcMain.handle('insert-data', async (event, record) => {
    try {
        const existingRecord = await LookupTable.findOne({ where: { mname: record.mname } });

        if (existingRecord) {
            console.log("ALREADY EXISTSS")
            return { success: false, error: 'File with the same filename has already been uploaded.' };
        }

        const result = await LookupTable.create(record);
        return { success: true, data: result };
    } catch (error) {
        console.error('Failed to insert data:', error);
        return { success: false, error: error.message };
    }
});
ipcMain.handle('select-data', async (event, mname) => {
    try {
        const result = await LookupTable.findOne({ where: { mname } });
        if (result) {
            return { success: true, data: result };
        } else {
            return { success: false, error: 'Record not found' };
        }
    } catch (error) {
        console.error('Failed to select data:', error);
        return { success: false, error: error.message };
    }
});

ipcMain.handle('ureq', async (event, mid, updates) => {
    try {
        const result = await LookupTable.update(updates, { where: { mid } });
        return { success: true, data: result };
    } catch (error) {
        console.error('Failed to update data:', error);
        return { success: false, error: error.message };
    }
});


ipcMain.handle('upload-file', async (event, filePath, mid, uid, token, mediaName) => {
    try {
        console.log('Uploading file from path:', filePath);

        const formData = new FormData();
        formData.append('media_url', fs.createReadStream(filePath));
        formData.append('mid', mid);
        formData.append('uid', uid);
        formData.append('token', token);
        formData.append('media_name', mediaName);

        const response = await axios.post('http://' + HOST_IP + ':8000/upload/', formData, {
            headers: {
                ...formData.getHeaders(),
            },
        });

        console.log('Upload response:', response.data);
        return { success: true, data: response.data };
    } catch (error) {
        console.error('Failed to upload file:', error);
        return { success: false, error: error.message };
    }
});


ipcMain.handle('open-file-dialog', async () => {
    const result = await dialog.showOpenDialog({
        properties: ['openFile'],
        filters: [
            { name: 'Videos', extensions: ['mkv', 'avi', 'mp4', 'mov'] }
        ]
    });

    if (result.canceled) {
        return { canceled: true };
    } else {
        return { canceled: false, filePath: result.filePaths[0] };
    }
});
ipcMain.handle('fetch-videos', async (event, uid) => {
    try {
        const records = await LookupTable.findAll({ where: { localurl: { [Sequelize.Op.not]: null }, uid: uid } });
        return { success: true, data: records };
    } catch (error) {
        console.error('Failed to fetch videos:', error);
        return { success: false, error: error.message };
    }
});

ipcMain.handle('extract-frames', async (event, videoPath) => {
    try {
        const { format } = await new Promise((resolve, reject) => {
            ffmpegFluent(videoPath)
                .setFfprobePath(ffprobePath)
                .ffprobe((err, metadata) => {
                    if (err) {
                        reject(err);
                    } else {
                        resolve(metadata);
                    }
                });
        });
        const duration = format.duration;
        const videoName = path.basename(videoPath, path.extname(videoPath));
        const outputDir = path.join(app.getPath('userData'), 'frames', videoName);

        if (!fs.existsSync(outputDir)) {
            fs.mkdirSync(outputDir, { recursive: true });
        }

        const frameFiles = fs.readdirSync(outputDir);
        if (frameFiles.length > 1) {
            console.log('Frames already exist for:', videoPath);
            const framePaths = frameFiles.map(file => path.join(outputDir, file));
            return framePaths;
        }

        const MAX_FRAMES = 120;
        const framesRequired = 20;
        const MinFrames = Math.max(framesRequired, Math.floor(duration * 0.5));
        const maxFrameCount = Math.min(MinFrames, MAX_FRAMES);
        const frameRate = maxFrameCount / duration;

        let threadCount = Math.min(Math.floor(os.cpus().length / 2), maxFrameCount);
        const chunkDuration = duration / threadCount;

        const promises = [];
        for (let i = 0; i < threadCount; i++) {
            const startTime = i * chunkDuration;
            const worker = new Worker(path.join(__dirname, 'frameExtractorWorker.js'), {
                workerData: {
                    videoPath,
                    outputDir,
                    startTime,
                    duration: chunkDuration,
                    frameRate,
                    threadIndex: i + 1
                }
            });

            promises.push(new Promise((resolve, reject) => {
                worker.on('message', (msg) => {
                    if (msg.error) {
                        reject(new Error(msg.error));
                    } else {
                        resolve();
                    }
                });
                worker.on('error', reject);
                worker.on('exit', (code) => {
                    if (code !== 0) {
                        reject(new Error(`Worker stopped with exit code ${code}`));
                    }
                });
            }));
        }

        await Promise.all(promises);

        const framePaths = fs.readdirSync(outputDir).map(file => path.join(outputDir, file));
        return framePaths;
    } catch (error) {
        console.error('Error extracting frames:', error);
        throw error;
    }
});


ipcMain.handle('save-file', async (event, sourcePath, fileName) => {
    const appDataPath = app.getPath('userData');
    const downloadsPath = path.join(appDataPath, 'Downloads');

    if (!fs.existsSync(downloadsPath)) {
        fs.mkdirSync(downloadsPath);
    }

    const destinationPath = path.join(downloadsPath, fileName);

    return new Promise((resolve, reject) => {
        const readStream = fs.createReadStream(sourcePath);
        const writeStream = fs.createWriteStream(destinationPath);

        readStream.on('error', reject);
        writeStream.on('error', reject);
        writeStream.on('finish', () => resolve(destinationPath));

        readStream.pipe(writeStream);
    });
});

async function processQueue() {
    console.log("In process -----------------------------------------------");
    const {
        processing,
        cuda,
        localProcess,
        videoUrl,
        originalVideoURL,
        processingQueue,
        remoteProcessingQueue
    } = store.get('appProcessing', {
        processing: false,
        cuda: false,
        localProcess: false,
        videoUrl: '',
        originalVideoURL: '',
        processingQueue: [],
        remoteProcessingQueue: []
    });
    if (processing || processingQueue.length === 0) return;

    const nextVideo = processingQueue.shift();
    updateState({
        processing: true,
        cuda: cuda,
        localProcess: localProcess,
        videoUrl: nextVideo.outputVideoPath,
        originalVideoURL: originalVideoURL,
        processingQueue: processingQueue,
        remoteProcessingQueue: remoteProcessingQueue
    });

    try {
        const output = await runPythonScript(nextVideo.scriptPath, [
            nextVideo.videoPath,
            nextVideo.outputVideoPath,
            nextVideo.modelPath,
        ]);
        console.log("Python Script Output:", output);
        const {
            cuda,
            localProcess,
            originalVideoURL,
            processingQueue,
            remoteProcessingQueue
        } = store.get('appProcessing', {
            processing: false,
            cuda: false,
            videoUrl: '',
            originalVideoURL: '',
            processingQueue: [],
            remoteProcessingQueue: []
        });
        updateState({
            processing: false,
            cuda: cuda,
            localProcess: localProcess,
            videoUrl: '',
            originalVideoURL: originalVideoURL,
            processingQueue: processingQueue,
            remoteProcessingQueue: remoteProcessingQueue
        });
        processQueue();
    } catch (error) {
        console.error("Python Script Error:", error);
        updateState({
            processing: false,
            cuda: false,
            localProcess: false,
            videoUrl: '',
            originalVideoURL: originalVideoURL,
            processingQueue: processingQueue,
            remoteProcessingQueue: remoteProcessingQueue
        });
    }
}

ipcMain.handle('queue-video', async (event, videoDetails) => {
    let local = videoDetails.localProcess;
    console.log('Video Details being added:', videoDetails);
    if (local) {
        const {
            processing,
            cuda,
            localProcess,
            videoUrl,
            originalVideoURL,
            processingQueue,
            remoteProcessingQueue
        } = store.get('appProcessing', {
            processing: false,
            cuda: false,
            localProcess: false,
            videoUrl: '',
            originalVideoURL: '',
            processingQueue: [],
            remoteProcessingQueue: []
        });
        processingQueue.push(videoDetails);
        updateState({
            processing: processing,
            cuda: cuda,
            localProcess: localProcess,
            videoUrl: videoUrl,
            originalVideoURL: originalVideoURL,
            processingQueue: processingQueue,
            remoteProcessingQueue: remoteProcessingQueue
        });
        processQueue();
    } else {
        const {
            processing,
            cuda,
            localProcess,
            videoUrl,
            originalVideoURL,
            processingQueue,
            remoteProcessingQueue
        } = store.get('appProcessing', {
            processing: false,
            cuda: false,
            localProcess: false,
            videoUrl: '',
            originalVideoURL: '',
            processingQueue: [],
            remoteProcessingQueue: []
        });
        remoteProcessingQueue.push(videoDetails);
        updateState({
            processing: processing,
            cuda: cuda,
            localProcess: localProcess,
            videoUrl: videoUrl,
            originalVideoURL: originalVideoURL,
            processingQueue: processingQueue,
            remoteProcessingQueue: remoteProcessingQueue
        });
        processVideoRemotely(videoDetails);
    }

});

async function processVideoRemotely(videoDetails) {
    console.log('Processing video remotely:', videoDetails);
    setTimeout(() => {
        const {
            processing,
            cuda,
            localProcess,
            videoUrl,
            originalVideoURL,
            processingQueue,
            remoteProcessingQueue
        } = store.get('appProcessing', {
            processing: false,
            cuda: false,
            localProcess: false,
            videoUrl: '',
            originalVideoURL: '',
            processingQueue: [],
            remoteProcessingQueue: []
        });
        const index = remoteProcessingQueue.findIndex(video => video.outputVideoPath === videoDetails.outputVideoPath);
        if (index !== -1) {
            remoteProcessingQueue.splice(index, 1);
            updateState({
                processing: processing,
                cuda: cuda,
                localProcess: localProcess,
                videoUrl: videoUrl,
                originalVideoURL: originalVideoURL,
                processingQueue: processingQueue,
                remoteProcessingQueue: remoteProcessingQueue
            });
        }
    }, 15000);
}

// const { execFile } = require('child_process');

function runPythonScript(scriptPath, args) {
    console.log('Running Python Script:', scriptPath, args);
    return new Promise((resolve, reject) => {
        const python = spawn('python', [scriptPath, ...args], {
            detached: true,
            stdio: ['ignore', 'pipe', 'pipe'],
            shell: true,
            windowsHide: true
        });

        console.log("Script path: " + scriptPath);

        let output = '';
        let error = '';

        python.stdout.on('data', (data) => {
            output += data.toString();
        });

        python.stderr.on('data', (data) => {
            error += data.toString();
        });

        python.on('error', (err) => {
            reject(new Error("Failed to execute Python script: " + err.message));
        });

        python.on('close', (code) => {
            if (code === 0) {
                resolve(output);
                mainWindow.webContents.send('python-script-done', 'Video done processing');
            } else {
                mainWindow.webContents.send('python-script-done', 'Video done processing');
                console.log('Python script done but exited with unexpected code:', code);
                resolve(output);
            }
        });

        python.unref();
    });
}

ipcMain.handle('check-cuda', async () => {
    return new Promise((resolve, reject) => {
        const appPath = app.getAppPath();
        const extractedPath = extractPythonFiles('cudaCheck.py');  // Use app data directory
        const pythonPath = path.join(extractedPath, 'python', 'cudaCheck.py');  // Ensure the script has the correct path
        const python = spawn('python', [pythonPath], {
            cwd: __dirname,
            stdio: ['pipe', 'pipe', 'pipe'],
            shell: true,
        });

        let output = '';
        let error = '';

        python.stdout.on('data', (data) => {
            output += data.toString();
        });

        python.stderr.on('data', (data) => {
            error += data.toString();
        });

        python.on('close', (code) => {
            resolve(true);
            if (code === 0) {
                console.log("CUDA available:", output.trim() == 'True');
                resolve(output.trim() == 'True');
            } else {
                reject(new Error(error));
            }
        });

        python.on('error', (err) => {
            reject(new Error(`Failed to start Python script: ${err.message}`));
        });
    });
});

ipcMain.handle('upload-to-agent', async (event, ip, port, filepath, uid, size, token, mname) => {
    const extractedPath = extractPythonFiles('pythonUpload.py');
    const scriptPath = path.join(extractedPath, 'pythonUpload.py');

    let rec = await LookupTable.findOne({ where: { mname: mname, uid: uid } });
    const mid = rec.mid;
    const args = [ip, port, `"${filepath}"`, uid, size, token, mid];

    return new Promise((resolve, reject) => {
        const { spawn } = require('child_process');
        const python = spawn('python', [scriptPath, ...args], {});

        let output = '';
        let error = '';

        python.stdout.on('data', (data) => {
            const message = data.toString();
            output += message;
            console.log(`Python stdout: ${message}`);
        });

        python.stderr.on('data', (data) => {
            const message = data.toString();
            error += message;
            console.error(`Python stderr: ${message}`);
        });

        python.on('close', (code) => {
            console.log(`Python process exited with code ${code}`);
            if (code === 0) {
                resolve(output);
            } else {
                reject(new Error(error));
            }
        });

        python.on('error', (err) => {
            reject(new Error(`Failed to start Python script: ${err.message}`));
        });
    });
});



ipcMain.handle('download-to-client', async (event, ip, port, filepath, uid, size, token, videoDestination) => {
    const extractedPath = extractPythonFiles('pythonDownload.py');
    const scriptPath = path.join(extractedPath, 'pythonDownload.py');
    const fullFilepath = path.join(app.getPath('userData'), 'Downloads', filepath);
    let rec = await LookupTable.findOne({ where: { mname: filepath, uid: uid } });
    const mid = rec.mid;
    const args = [ip, port, filepath, uid, size, token, mid, videoDestination];

    return new Promise((resolve, reject) => {
        const { spawn } = require('child_process');
        const python = spawn('python', [scriptPath, ...args]);

        let output = '';
        let error = '';

        python.stdout.on('data', (data) => {
            output += data.toString();
            console.log(output);
        });

        python.stderr.on('data', (data) => {
            error += data.toString();
        });

        python.on('close', (code) => {
            if (code === 0) {
                resolve(output);
            } else {
                reject(new Error(error));
            }
        });
    });
});

ipcMain.handle('resolve-path', (event, ...segments) => {
    const resolvedPath = path.resolve(...segments); // Resolve the path from segments

    try {
        // Ensure that the directory structure exists by creating it if necessary
        fs.mkdirSync(resolvedPath, { recursive: true });
        console.log(`Directory created or already exists: ${resolvedPath}`);
    } catch (err) {
        console.error(`Error creating directory at path: ${resolvedPath}`, err);
        return { success: false, error: err.message };
    }

    // Return the resolved path
    console.log("RESOLVED PATH: ", resolvedPath)
    return resolvedPath;
});

ipcMain.handle('check-file-existence', async (event, filePath) => {
    try {
        if (fs.existsSync(filePath)) {
            return { success: true, exists: true };
        } else {
            return { success: true, exists: false };
        }
    } catch (error) {
        console.error('Error checking file existence:', error);
        return { success: false, error: error.message };
    }
});

ipcMain.handle('delete-video-file', async (event, filePath) => {
    try {
        if (fs.existsSync(filePath)) {
            fs.unlinkSync(filePath);
        } else {
            return { success: false, error: 'File does not exist' };
        }

        const framesDir = path.join(app.getPath('userData'), 'frames', path.basename(filePath, path.extname(filePath)));

        if (fs.existsSync(framesDir)) {
            const files = fs.readdirSync(framesDir);

            for (let i = 1; i < files.length; i++) {
                const framePath = path.join(framesDir, files[i]);
                if (fs.existsSync(framePath)) {
                    fs.unlinkSync(framePath);
                }
            }
        } else {
            console.warn(`Frames directory does not exist: ${framesDir}`);
        }

        return { success: true };
    } catch (error) {
        console.error('Error deleting file or frames:', error);
        return { success: false, error: error.message };
    }
});

ipcMain.handle('get-video-frame', async (event, videoPath) => {
    const videoName = path.basename(videoPath, path.extname(videoPath));
    const outputDir = path.join(app.getPath('userData'), 'frames', videoName);

    const frameFiles = fs.readdirSync(outputDir);
    if (frameFiles.length > 0) {
        console.log('Frames already exist for:', videoPath);
        const framePaths = frameFiles.map(file => path.join(outputDir, file));
        return framePaths;
    }
});

ipcMain.handle('move-deleted-video-to-downloads', async (event, videoName, filePath) => {
    try {
        const videoFilePath = filePath;

        if (!fs.existsSync(videoFilePath)) {
            return { success: false, error: 'Video file does not exist' };
        }

        const appDataPath = app.getPath('userData');
        const downloadsDir = path.join(appDataPath, 'Downloads');

        // Ensure the Downloads directory exists
        if (!fs.existsSync(downloadsDir)) {
            fs.mkdirSync(downloadsDir, { recursive: true });
            console.log('Downloads directory created:', downloadsDir);
        }

        const destinationPath = path.join(downloadsDir, videoName);

        console.log('Moving video file to:', destinationPath);
        fs.renameSync(videoFilePath, destinationPath);

        const updatedRecord = await LookupTable.update(
            { localurl: destinationPath },
            { where: { mname: videoName } }
        );

        if (updatedRecord[0] === 0) {
            console.error('No record found to update');
            return { success: false, error: 'No record found to update' };
        }

        console.log('Video moved and lookup table updated:', destinationPath);
        return { success: true, videoFilePath: destinationPath };
    } catch (error) {
        console.error('Error moving video file:', error);
        return { success: false, error: error.message };
    }
});


ipcMain.handle('get-ai-models', async () => {
    try {
        const models = await AIModels.findAll();
        return { success: true, data: models.map(model => model.toJSON()) };
    } catch (error) {
        console.error('Failed to fetch AI models:', error);
        return { success: false, error: error.message };
    }
});
ipcMain.handle('getVideoByURL', async (event, videoURL) => {
    try {
        const video = await VideoTable.findOne({ where: { videoURL } });
        return video ? video.toJSON() : null;
    } catch (error) {
        console.error("Error fetching video by URL:", error);
        return null;
    }
});

ipcMain.handle('move-video', async (event, sourcePath, destFileName) => {
    return new Promise((resolve, reject) => {
        const appDataPath = app.getPath('userData');
        const downloadsDir = path.join(appDataPath, 'Downloads');
        const destFile = path.join(downloadsDir, destFileName);

        console.log("MOVE VIDEO PATH: ", sourcePath);
        console.log("MOVE downloadsDir PATH: ", downloadsDir);
        console.log("MOVE Dest PATH: ", destFile);

        fs.renameSync(sourcePath, destFile, (err) => {
            if (err) {
                reject(err);
            } else {
                resolve(`File moved to ${destFile}`);
            }
        });
    });
});

ipcMain.handle('open-ftp', async (event, uid, token, size, media_name, media_url, command) => {
    let mid = "";
    if (command == "SEND") {
        const rec = await LookupTable.create({
            mname: media_name,
            localurl: media_url,
            size: size,
            uid: uid,
        });
        mid = rec.mid;
    }
    const formData = new FormData();
    formData.append('uid', uid);
    formData.append('token', token);
    formData.append('size', size);
    formData.append('media_name', media_name);
    formData.append('media_url', media_url);
    formData.append('mid', mid);
    formData.append('command', command)

    try {
        const response = await axios.post('http://' + HOST_IP + ':8000/uploadFile/', formData, {
            headers: {
                ...formData.getHeaders(),
            },
        });

        console.log('Upload response:', response.data);
        const { aip, aport } = response.data;

        return { success: true, ip: aip, port: aport };
    } catch (error) {
        console.error('Error in FTP upload:', error);
        return { success: false, error: error.message };
    }
});

ipcMain.handle('get-file-size', (event, filePath) => {
    try {
        const stats = fs.Stats(filePath);
        console.log('File stats:', stats);
        let fileSize = stats.size;
        return fileSize.toString();
    } catch (error) {
        console.error('Error getting file size:', error);
        return null;
    }
});
ipcMain.handle('checkIfVideoProcessed', async (event, videoUrl) => {
    try {
        const video = await VideoTable.findOne({ where: { videoUrl } });
        if (!video) return null;
        const originalID = video.videoID
        const videos = await VideoTable.findOne({ where: { originalVidID: originalID } });
        if (videos) return true;
        else return false;
    } catch (error) {
        console.error("Error fetching video by URL:", error);
        return null;
    }
});

ipcMain.handle('getProcessedVideos', async (event, originalVidID) => {
    try {
        const videos = await VideoTable.findAll({ where: { originalVidID } });
        return videos.map(video => video.toJSON());
    } catch (error) {
        console.error("Error fetching processed videos:", error);
        return [];
    }
});

ipcMain.handle('addVideo', async (event, videoData) => {
    try {
        const newVideo = await VideoTable.create(videoData);
        return newVideo.toJSON();
    } catch (error) {
        console.error("Error adding new video:", error);
        return null;
    }
});

function removeVideo(videoUrl) {
    return VideoTable.destroy({ where: { videoURL: videoUrl } });
}

ipcMain.handle('selectDrivesDirectory', async (event) => {
    const directoryPathFile = path.join(app.getPath('userData'), 'drivesDirectory.txt');
    const result = await dialog.showOpenDialog(mainWindow, {
        properties: ['openDirectory'],
    });
    if (result.filePaths.length > 0) {
        fs.writeFileSync(directoryPathFile, result.filePaths[0]);
        return result.filePaths[0];
    }
    return null;
})

ipcMain.handle('getDrivesDirectory', () => {
    const directoryPathFile = path.join(app.getPath('userData'), 'drivesDirectory.txt');
    if (fs.existsSync(directoryPathFile)) {
        return fs.readFileSync(directoryPathFile, 'utf-8');
    }
    return null;
});

ipcMain.handle('getDriveVideos', async (event, directory) => {
    try {
        return await getVideoFiles(directory);
    } catch (error) {
        console.error('Error getting video files:', error);
        return [];
    }
});

ipcMain.handle('readDriveLog', async (event, driveDirectory) => {
    try {
        return await getJsonData(driveDirectory);
    } catch (error) {
        console.error('Failed to read drive log:', error);
        return { error: 'Failed to read drive log' };
    }
});

ipcMain.handle('save-pipe-json', async (event, jsonString) => {
    try {
        let baseDirectory;
        const platform = os.platform();
        if (platform === 'win32') {
            baseDirectory = path.join(process.env.APPDATA, 'HVstore');
        } else if (platform === 'linux') {
            baseDirectory = path.join(os.homedir(), '.local', 'share', 'HVstore');
        } else {
            baseDirectory = path.join(process.env.APPDATA, 'HVstore');
        }

        const pipesDirectory = path.join(baseDirectory, 'pipes');
        if (!fs.existsSync(pipesDirectory)) {
            fs.mkdirSync(pipesDirectory, { recursive: true });
        }

        const filePath = path.join(pipesDirectory, 'pipes.json');

        let existingData = [];
        if (fs.existsSync(filePath)) {
            const fileContent = fs.readFileSync(filePath, 'utf-8');

            try {
                const parsedData = JSON.parse(fileContent);
                if (Array.isArray(parsedData)) {
                    existingData = parsedData;
                } else {
                    console.warn('Existing data is not an array, initializing as empty array');
                }
            } catch (error) {
                console.error('Error parsing JSON:', error);
            }
        }

        const newEntry = JSON.parse(jsonString);
        existingData.push(newEntry);

        fs.writeFileSync(filePath, JSON.stringify(existingData, null, 2), 'utf-8');

        return { success: true, message: 'JSON data saved successfully!' };
    } catch (error) {
        console.error('Error saving JSON data:', error);
        return { success: false, message: 'Failed to save JSON data.' };
    }
});

ipcMain.handle('get-pipe-json', async (event) => {
    try {
        let baseDirectory;
        const platform = os.platform();
        if (platform === 'win32') {
            baseDirectory = path.join(process.env.APPDATA, 'HVstore');
        } else if (platform === 'linux') {
            baseDirectory = path.join(os.homedir(), '.local', 'share', 'HVstore');
        } else {
            baseDirectory = path.join(process.env.APPDATA, 'HVstore');
        }

        const pipesDirectory = path.join(baseDirectory, 'pipes');
        const filePath = path.join(pipesDirectory, 'pipes.json');

        if (!fs.existsSync(filePath)) {
            return { success: true, data: [], message: 'No data found.' };
        }

        const fileContent = fs.readFileSync(filePath, 'utf-8');
        const jsonData = JSON.parse(fileContent);

        return { success: true, data: jsonData, message: 'Data retrieved successfully!' };
    } catch (error) {
        console.error('Error getting JSON data:', error);
        return { success: false, message: 'Failed to retrieve JSON data.' };
    }
});

ipcMain.handle('run-python-script2', async (event, scriptPath, args) => {
    return new Promise((resolve, reject) => {
        const pythonProcess = spawn('python', [scriptPath, ...args]);

        pythonProcess.stdout.on('data', (data) => {
            console.log(`stdout: ${data}`);
        });

        pythonProcess.stderr.on('data', (data) => {
            console.error(`stderr: ${data}`);
        });

        pythonProcess.on('close', (code) => {
            console.log(`Python script exited with code ${code}`);
            resolve(code);
            event.sender.send('python-script-done', code);
        });

        pythonProcess.on('error', (err) => {
            console.error('Failed to start subprocess.', err);
            reject(err);
        });
    });
});

ipcMain.handle('google-sign-in', async () => {
    const url = client.generateAuthUrl({
        access_type: 'offline',
        scope: ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']
    });

    const authWindow = new BrowserWindow({
        width: 500,
        height: 600,
        show: true,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            webSecurity: true,
        }
    });

    authWindow.loadURL(url);
    authWindow.show();

    return new Promise((resolve, reject) => {
        const handleNavigation = async (url) => {
            console.log("Navigated to URL:", url);
            const raw_code = /code=([^&]*)/.exec(url) || null;
            const code = (raw_code && raw_code.length > 1) ? raw_code[1] : null;
            const error = /\?error=(.+)$/.exec(url);

            if (code) {
                console.log("Authorization code found:", code);
                authWindow.destroy();

                try {
                    const { tokens } = await client.getToken(code);
                    client.setCredentials(tokens);
                    resolve(tokens);
                } catch (tokenError) {
                    console.error('Token exchange error:', tokenError);
                    reject(tokenError);
                }
            } else if (error) {
                console.error('Error during authentication:', error);
                authWindow.destroy();
                reject(new Error('Error during authentication: ' + error));
            }
        };

        authWindow.webContents.on('will-navigate', (event, url) => {
            handleNavigation(url);
        });

        authWindow.webContents.on('did-navigate', (event, url) => {
            handleNavigation(url);
        });

        authWindow.on('close', () => {
            reject(new Error('User closed the OAuth window'));
        });
    });
});

CLIENT_ID = process.env.CLIENT_ID;
CLIENT_SECRET = process.env.CLIENT_SECRET;
REDIRECT_URI = process.env.REDIRECT_URI;

const oauth2Client = new OAuth2Client(
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRECT_URI
);

ipcMain.handle('get-auth-url', async () => {
    const authUrl = oauth2Client.generateAuthUrl({
        access_type: 'offline',
        scope: ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']
    });
    return authUrl;
});

ipcMain.handle('exchange-code', async (event, code) => {
    try {
        const { tokens } = await oauth2Client.getToken(code);
        oauth2Client.setCredentials(tokens);

        const { data } = await oauth2Client.request({
            url: 'https://www.googleapis.com/oauth2/v2/userinfo'
        });

        return {
            success: true,
            user: data,
            tokens: tokens
        };
    } catch (error) {
        console.error('Error exchanging code:', error);
        return { success: false, error: error.message };
    }
});

ipcMain.handle('google-login-test', async () => {
    return new Promise((resolve, reject) => {
        const server = http.createServer(async (req, res) => {
            if (req.url.startsWith('/callback')) {
                const urlParams = new URL(`http://${HOST_IP}${req.url}`).searchParams;
                const code = urlParams.get('code');
                res.end('Authentication successful! You can close this window.');
                server.close();

                if (code) {
                    try {
                        const { tokens } = await oauth2Client.getToken(code);
                        oauth2Client.setCredentials(tokens);

                        const { data } = await oauth2Client.request({
                            url: 'https://www.googleapis.com/oauth2/v2/userinfo',
                        });

                        resolve({
                            success: true,
                            user: data,
                            tokens: tokens,
                        });
                    } catch (error) {
                        console.error('Error exchanging code:', error);
                        resolve({ success: false, error: error.message });
                    }
                } else {
                    resolve({ success: false, error: 'No code found in the query parameters' });
                }
            }
        });

        server.listen(0, () => {
            const port = server.address().port;
            const redirectUri = `http://${HOST_IP}:${port}/callback`;

            const oauth2Client = new OAuth2Client(
                CLIENT_ID,
                CLIENT_SECRET,
                redirectUri
            );

            const authUrl = oauth2Client.generateAuthUrl({
                access_type: 'offline',
                scope: [
                    'https://www.googleapis.com/auth/userinfo.profile',
                    'https://www.googleapis.com/auth/userinfo.email',
                ],
            });

            shell.openExternal(authUrl);
        });
    });
});

ipcMain.handle('get-auth-url-test', async () => {
    const authUrl = oauth2Client.generateAuthUrl({
        access_type: 'offline',
        scope: ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']
    });
    return authUrl;
});

async function handleAuthCallback(callbackUrl) {
    const parsedUrl = new URL(callbackUrl);
    const code = parsedUrl.searchParams.get('code');

    if (code) {
        try {
            const { tokens } = await oauth2Client.getToken(code);
            oauth2Client.setCredentials(tokens);

            const { data } = await oauth2Client.request({
                url: 'https://www.googleapis.com/oauth2/v2/userinfo'
            });

            mainWindow.webContents.send('auth-success', {
                success: true,
                user: data,
                tokens: tokens
            });
        } catch (error) {
            console.error('Error exchanging code:', error);
            mainWindow.webContents.send('auth-error', { success: false, error: error.message });
        }
    } else {
        mainWindow.webContents.send('auth-error', { success: false, error: 'No code found in the query parameters' });

    }
}

ipcMain.handle('get-last-signin', async (event, uid) => {
    return new Promise((resolve, reject) => {
        axios.post('http://' + HOST_IP + ':8000/api/getLastSignin/', { uid: uid })
            .then(response => {
                resolve(response.data);
            })
            .catch(error => {
                reject(error);
            });
    });
});

ipcMain.handle('update-last-signin', async (event, uid) => {
    return new Promise((resolve, reject) => {
        axios.post('http://' + HOST_IP + ':8000/api/updateLastSignin/', { uid: uid })
            .then(response => {
                resolve(response.data);
            })
            .catch(error => {
                reject(error);
            });
    });
});

ipcMain.handle('request-uptime', async (event) => {
    return new Promise((resolve, reject) => {
        axios.get('http://' + HOST_IP + ':8000/requestUptime/')
            .then(response => {
                resolve(response.data);
            })
            .catch(error => {
                reject(error);
            });
    });
});

ipcMain.handle('get-test-data', async (event) => {
    return new Promise((resolve, reject) => {
        axios.get('http://' + HOST_IP + ':8000/getTestData/')
            .then(response => {
                resolve(response.data);
            })
            .catch(error => {
                reject(error);
            });
    });
});


ipcMain.handle('get-base-directory', async (event) => {
    const platform = os.platform();

    let baseDirectory;
    if (platform === 'win32') {
        baseDirectory = path.join(process.env.APPDATA, 'HVstore');
    } else if (platform === 'linux') {
        baseDirectory = path.join(os.homedir(), '.local', 'share', 'HVstore');
    } else {
        console.warn('Unknown platform. Defaulting to home directory.');
        baseDirectory = path.join(os.homedir(), 'HVstore');
    }
    return baseDirectory;
});

function generateThumbnail(videoPath) {
    return new Promise((resolve, reject) => {
        const thumbnailPath = videoPath.replace(/\.[^/.]+$/, ".png");
        ffmpeg(videoPath)
            .on('end', () => resolve(thumbnailPath))
            .on('error', (err) => reject(err))
            .screenshot({
                timestamps: ['50%'],
                filename: 'thumbnail.png',
                folder: path.dirname(thumbnailPath),
            });
    });
}

ipcMain.handle('sync-sqlite', async (event, uid) => {
    return new Promise((resolve, reject) => {
        axios.post('http://' + HOST_IP + ':8000/api/syncSqlite/', { uid: uid })
            .then(response => {
                console.log("response", response.data);
                insertLookupData(response.data);
                console.log("DATA LOGGED", data);
                logLookupTableContents();
                resolve(response.data);
            })
            .catch(error => {
                console.log("error", error);
                reject(error);
            });
    });
});

async function insertLookupData(responseData) {
    try {
        const data = responseData.data;
        for (const item of data) {
            console.log("Attempting to insert item:", item);
            if (!item.media_name || !item.uid) {
                console.error("Invalid item data:", item);
                continue;
            }

            const existingItem = await LookupTable.findOne({ where: { mname: item.media_name } });
            if (existingItem) {
                console.log('Item already exists in the database:', item.media_name);
            }

            await LookupTable.create({
                mid: parseInt(item.mid),
                mname: item.media_name,
                localurl: item.media_url,
                size: 0,
                uid: item.uid
            });
            console.log('Item inserted successfully:', item.media_name);
        }
        console.log('All valid data inserted successfully');
    } catch (error) {
        console.error('Error inserting data:', error);
    }
}

async function logLookupTableContents() {
    try {
        const allRecords = await LookupTable.findAll();
        console.log('Contents of LookupTable:');
        allRecords.forEach(record => {
            console.log(record.toJSON());
        });
    } catch (error) {
        console.error('Error fetching LookupTable contents:', error);
    }
}