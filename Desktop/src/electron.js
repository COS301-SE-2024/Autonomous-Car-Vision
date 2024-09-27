const {app, BrowserWindow, ipcMain, dialog, View} = require('electron');
const {spawn} = require('child_process');
const path = require('path');
const crypto = require('crypto');
const fs = require('fs');
const {LookupTable, AIModels, VideoTable} = require('./database');
const axios = require('axios');
const FormData = require('form-data')
const {Sequelize} = require('sequelize');
const ffmpegFluent = require('fluent-ffmpeg');
const ffmpegPath = require('ffmpeg-static');
const ffprobePath = require('ffprobe-static').path;
const {OAuth2Client} = require('google-auth-library');
const http = require('http');
// import ability to get .env data
require('dotenv').config();

const os = require('os');
const {Worker, isMainThread} = require('worker_threads');
const {getVideoFiles} = require('./videoScanner');
const {getJsonData} = require('./getJsonData');


let mainWindow;
let store;

async function loadElectronStore() {
    const {default: Store} = await import('electron-store');
    return new Store();
}


async function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 800,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            enableRemoteModule: false,
            webviewTag: true,
        },
        autoHideMenuBar: true,
        icon: path.join(__dirname, 'assets', 'HighViz(transparent)-white.png'),
    });

    mainWindow.loadFile('public/index.html');
    // mainWindow.webContents.openDevTools();
    // Initialize the store after the window is created
    store = await loadElectronStore();
}

app.whenReady().then(() => {
    createWindow();
  
    // Register protocol handler
    if (process.defaultApp) {
      if (process.argv.length >= 2) {
        app.setAsDefaultProtocolClient('myapp', process.execPath, [path.resolve(process.argv[1])])
      }
    } else {
      app.setAsDefaultProtocolClient('myapp')
    }
  });

  app.on('ready', () => {
    // Suppress specific DevTools warnings
    const { session } = require('electron');
    session.defaultSession.webRequest.onBeforeRequest((details, callback) => {
      if (details.url.includes('devtools://')) {
        callback({cancel: false});
      } else {
        callback({cancel: false});
      }
    });
  
    createWindow();
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

// try {
//     require('electron-reloader')(module)
// } catch (_) { }


// Get app path
ipcMain.handle('get-app-path', () => {
    return app.getAppPath();
});

// Read directory handler
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

// Helper function to update the store state
function updateState(updates) {
    const currentState = store.get('appProcessing', {
        processing: false,
        cuda: false,
        localProcess: false,
        videoUrl: '',
        originalVideoURL: '',
        processingQueue: [],
        remoteProcessingQueue: []
    });
    const newState = {...currentState, ...updates};
    console.log('Updated state:', newState);
    store.set('appProcessing', newState);
    mainWindow.webContents.send('process-changed'); // Notify renderer about state change
    return newState;
}

// IPC handler for hashing password
ipcMain.handle('hash-password', async (event, password) => {
    const salt = crypto.randomBytes(16).toString('hex');
    const hash = crypto.scryptSync(password, salt, 64).toString('hex');
    return {hash, salt};
});

ipcMain.handle('hash-password-salt', async (event, password, salt) => {
    if (typeof salt !== 'string') {
        throw new TypeError('The "salt" argument must be of type string.');
    }
    const hash = crypto.scryptSync(password, salt, 64).toString('hex');
    return {hash};
});
ipcMain.handle('insert-data', async (event, record) => {
    try {
        const result = await LookupTable.create(record);
        return {success: true, data: result};
    } catch (error) {
        console.error('Failed to insert data:', error);
        return {success: false, error: error.message};
    }
});
// IPC handler for selecting data by mname
ipcMain.handle('select-data', async (event, mname) => {
    try {
        const result = await LookupTable.findOne({where: {mname}});
        if (result) {
            return {success: true, data: result};
        } else {
            return {success: false, error: 'Record not found'};
        }
    } catch (error) {
        console.error('Failed to select data:', error);
        return {success: false, error: error.message};
    }
});

// IPC handler for updating data by mid
ipcMain.handle('ureq', async (event, mid, updates) => {
    try {
        const result = await LookupTable.update(updates, {where: {mid}});
        return {success: true, data: result};
    } catch (error) {
        console.error('Failed to update data:', error);
        return {success: false, error: error.message};
    }
});
ipcMain.handle('upload-file', async (event, filePath, mid, uid, token, mediaName) => {
    try {
        console.log('Uploading file from path:', filePath); // Log file path for debugging

        const formData = new FormData();
        formData.append('media_url', fs.createReadStream(filePath));
        formData.append('mid', mid);
        formData.append('uid', uid);
        formData.append('token', token);
        formData.append('media_name', mediaName);

        const response = await axios.post('http://localhost:8000/upload/', formData, {
            headers: {
                ...formData.getHeaders(),
            },
        });

        console.log('Upload response:', response.data); // Log response for debugging
        return {success: true, data: response.data};
    } catch (error) {
        console.error('Failed to upload file:', error);
        return {success: false, error: error.message};
    }
});
ipcMain.handle('open-file-dialog', async () => {
    const result = await dialog.showOpenDialog({
        properties: ['openFile'],
        filters: [
            {name: 'Videos', extensions: ['mkv', 'avi', 'mp4', 'mov']}
        ]
    });

    if (result.canceled) {
        return {canceled: true};
    } else {
        return {canceled: false, filePath: result.filePaths[0]};
    }
});
ipcMain.handle('fetch-videos', async () => {
    try {
        const records = await LookupTable.findAll({where: {localurl: {[Sequelize.Op.not]: null}}});
        return {success: true, data: records};
    } catch (error) {
        console.error('Failed to fetch videos:', error);
        return {success: false, error: error.message};
    }
});

// Extract frames handler
ipcMain.handle('extract-frames', async (event, videoPath) => {
    try {
        const {format} = await new Promise((resolve, reject) => {
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
        const outputDir = path.join(path.dirname(videoPath), 'frames', videoName);

        // checks if output directory exists

        if (!fs.existsSync(outputDir)) {
            fs.mkdirSync(outputDir, {recursive: true});
        }

        // Checking if the frames are already generated
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


// IPC handler to save the file and return the file path
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

// Function to process the queue
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
        //call the run-python-script IPC handler

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
        processQueue(); // Process the next video in the queue
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

// IPC handler to queue a video for processing
ipcMain.handle('queue-video', async (event, videoDetails) => {
    // fetch localProcess from videoDetails
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
        // Process video remotely
        processVideoRemotely(videoDetails);
    }

});

// Function to process video remotely
async function processVideoRemotely(videoDetails) {
    // TODO: Implement remote processing
    console.log('Processing video remotely:', videoDetails);
    // Function should return success or failure
    // Either add listner for when the video is done processing or return a promise
    // If the process was unsuccessful, return false and notify user of failure
    // After notifying user, remove from local database because it is already there
    // Once done, failure of success, remove from remoteProcessingQueue
    // Notify user on success
    // mainWindow.webContents.send('python-script-done', 'Video done processing');

    // INFO: This is a placeholder function for remote processing, above steps
    // the video path will already be added to the local data base
    // but the user will not be able to view it until it is processed
    // this is only to show that the video is being processed
    // so the video has to be removed from the database if the processing fails

    // To remove use:
    // removeVideo(videoDetails.outputVideoPath);

    // Wait for 15 seconds then remove the video details from the remote processing queue
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

// Function to run a python script with set parameters
function runPythonScript(scriptPath, args) {
    console.log('Running Python Script:', scriptPath, args);
    return new Promise((resolve, reject) => {
        const python = spawn('python', [scriptPath, ...args], {
            detached: true,  // Detach the process
            stdio: ['ignore', 'pipe', 'pipe'],  // Ignore stdin, but pipe stdout and stderr
            shell: true,  // Run the command through a shell
            windowsHide: true  // Hide the terminal window on Windows
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
            // Handle the error event, for example, when the process could not be spawned, killed, or there's a sending message error
            reject(new Error("Failed to execute Python script: " + err.message));
        });

        python.on('close', (code) => {
            if (code === 0) {
                resolve(output);
                mainWindow.webContents.send('python-script-done', 'Video done processing');
            } else {
                // If the process exited with a code other than 0, it means there was an error
                mainWindow.webContents.send('python-script-done', 'Video done processing');
                console.log('Python script done but exited with unexpected code:', code);
                resolve(output);
            }
        });

        // Detach the process and allow it to continue running
        python.unref();
    });
}

// IPC handler for checking CUDA availability
ipcMain.handle('check-cuda', async () => {
    return new Promise((resolve, reject) => {
        console.log("Checking cuda availability")
        // get the root directory of the app
        const appPath = app.getAppPath();
        let pythonPath = path.join(appPath, '..');
        pythonPath = path.join(pythonPath, 'Models/cudaCheck.py');
        const python = spawn('python', [pythonPath], {
            cwd: __dirname, // Ensure the working directory is correct
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
    const scriptPath = 'src/routes/pythonUpload.py';
    let rec = await LookupTable.findOne({ where: { mname: mname, uid: uid } });
    const mid = rec.mid;
    const args = [ip, port, `"${filepath}"`, uid, size, token, mid];
    console.log("ARGS: " + args.join(" "));

    return new Promise((resolve, reject) => {
        const { spawn } = require('child_process');

        const python = spawn('python', [scriptPath, ...args], {});

        console.log("Running Python script:");
        console.log("Script path: " + scriptPath);
        console.log("Args: " + args.join(" "));

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
                resolve(output);  // Resolve with the captured output
            } else {
                reject(new Error(error));  // Reject with the captured error
            }
        });

        python.on('error', (err) => {
            reject(new Error(`Failed to start Python script: ${err.message}`));
        });
    });
});



ipcMain.handle('download-to-client', async (event, ip, port, filepath, uid, size, token) => {
    const scriptPath = 'src/routes/pythonDownload.py';
    let rec = await LookupTable.findOne({where: {mname: filepath, uid: uid}});
    const mid = rec.mid;
    const args = [ip, port, filepath, uid, size, token, mid];

    return new Promise((resolve, reject) => {
        const {spawn} = require('child_process');
        const python = spawn('python', [scriptPath, ...args]);

        console.log("Script path: " + scriptPath);
        console.log("Args: " + args.join(" "));
        let output = '';
        let error = '';

        python.stdout.on('data', (data) => {
            output += data.toString();
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
    return path.resolve(...segments);
});

// IPC handler to check if a video file exists
ipcMain.handle('check-file-existence', async (event, filePath) => {
    try {
        if (fs.existsSync(filePath)) {
            return {success: true, exists: true};
        } else {
            return {success: true, exists: false};
        }
    } catch (error) {
        console.error('Error checking file existence:', error);
        return {success: false, error: error.message};
    }
});

// IPC handler to delete a video file
ipcMain.handle('delete-video-file', async (event, filePath) => {
    try {
        // Delete the video file - Move it to deleted folder
        if (fs.existsSync(filePath)) {
            // Move the video file to the Deleted folder in development mode
            const deletedDir = path.join(path.dirname(filePath), 'Deleted', path.basename(filePath, path.extname(filePath)));
            fs.mkdirSync(deletedDir, {recursive: true});
            const newFilePath = path.join(deletedDir, path.basename(filePath));
            fs.renameSync(filePath, newFilePath);
        } else {
            return {success: false, error: 'File does not exist'};
        }

        // Determine the frames directory path
        const framesDir = path.join(path.dirname(filePath), 'frames', path.basename(filePath, path.extname(filePath)));

        // Check if frames directory exists
        if (fs.existsSync(framesDir)) {
            const files = fs.readdirSync(framesDir);

            // Keep the first frame and delete the rest
            for (let i = 1; i < files.length; i++) {
                const framePath = path.join(framesDir, files[i]);
                if (fs.existsSync(framePath)) {
                    fs.unlinkSync(framePath);
                }
            }
        } else {
            console.warn(`Frames directory does not exist: ${framesDir}`);
        }

        return {success: true};
    } catch (error) {
        console.error('Error deleting file or frames:', error);
        return {success: false, error: error.message};
    }
});

ipcMain.handle('get-video-frame', async (event, videoPath) => {
    const videoName = path.basename(videoPath, path.extname(videoPath));
    const outputDir = path.join(path.dirname(videoPath), 'frames', videoName);

    // Checking if the frames are already generated
    const frameFiles = fs.readdirSync(outputDir);
    if (frameFiles.length > 0) {
        console.log('Frames already exist for:', videoPath);
        const framePaths = frameFiles.map(file => path.join(outputDir, file));
        return framePaths;
    }
});

// IPC handler to move a video file from the Deleted folder to the Downloads folder
ipcMain.handle('move-deleted-video-to-downloads', async (event, videoName, filePath) => {
    try {
        const deletedDir = path.join(path.dirname(filePath), 'Deleted', path.basename(filePath, path.extname(filePath)));
        const videoFilePath = path.join(deletedDir, `${videoName}`);

        if (!fs.existsSync(videoFilePath)) {
            return {success: false, error: 'Video file does not exist'};
        }

        // Get the user's Downloads folder path
        const appDataPath = app.getPath('userData');
        const downloadsDir = path.join(appDataPath, 'Downloads');
        const destinationPath = path.join(downloadsDir, videoName);

        console.log('Moving video file to:', destinationPath);
        console.log('from: ', deletedDir);
        // Move the video file to the Downloads folder
        fs.renameSync(videoFilePath, destinationPath);

        return {success: true, videoFilePath: destinationPath};
    } catch (error) {
        console.error('Error moving video file:', error);
        return {success: false, error: error.message};
    }
});

ipcMain.handle('get-ai-models', async () => {
    try {
        const models = await AIModels.findAll();
        return {success: true, data: models.map(model => model.toJSON())};
    } catch (error) {
        console.error('Failed to fetch AI models:', error);
        return {success: false, error: error.message};
    }
});
// Handler to get video from the database by URL
ipcMain.handle('getVideoByURL', async (event, videoURL) => {
    try {
        const video = await VideoTable.findOne({where: {videoURL}});
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
        const response = await axios.post('http://localhost:8000/uploadFile/', formData, {
            headers: {
                ...formData.getHeaders(),
            },
        });

        console.log('Upload response:', response.data); // Log response for debugging

        // Extract IP and port from the response
        const {aip, aport} = response.data;

        return {success: true, ip: aip, port: aport};
    } catch (error) {
        console.error('Error in FTP upload:', error);
        return {success: false, error: error.message};
    }
});

ipcMain.handle('get-file-size', (event, filePath) => {
    try {
        const stats = fs.Stats(filePath);
        console.log('File stats:', stats);
        let fileSize = stats.size;
        //   convert to string
        return fileSize.toString();
        //   return stats.size;
    } catch (error) {
        console.error('Error getting file size:', error);
        return null;
    }
});
// Handler to get processed videos by original video ID
ipcMain.handle('checkIfVideoProcessed', async (event, videoUrl) => {
    try {
        const video = await VideoTable.findOne({where: {videoUrl}});

        // If the video is not found, return null
        if (!video) return null;

        // Get the videoID
        const originalID = video.videoID

        // Fetch all videos with the given original video ID
        const videos = await VideoTable.findOne({where: {originalVidID: originalID}});
        // Return true if at least one video is processed, else return false
        if (videos) return true;
        else return false;
    } catch (error) {
        console.error("Error fetching video by URL:", error);
        return null;
    }
});

// Handler to get all processed videos for a given original video ID
ipcMain.handle('getProcessedVideos', async (event, originalVidID) => {
    try {
        const videos = await VideoTable.findAll({where: {originalVidID}});
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

// Function to remove video from VideoTable
function removeVideo(videoUrl) {
    return VideoTable.destroy({where: {videoURL: videoUrl}});
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
        return {error: 'Failed to read drive log'};
    }
});

// Ipc handler to save json pipe file
ipcMain.handle('save-pipe-json', async (event, jsonString) => {
    try {
        // Determine the base directory based on the operating system
        let baseDirectory;
        const platform = os.platform();
        if (platform === 'win32') {
            baseDirectory = path.join(process.env.APPDATA, 'HVstore');
        } else if (platform === 'linux') {
            baseDirectory = path.join(os.homedir(), '.local', 'share', 'HVstore');
        } else {
            baseDirectory = path.join(process.env.APPDATA, 'HVstore'); // Default to Windows for unsupported OS
        }

        // Ensure the 'pipes' directory exists
        const pipesDirectory = path.join(baseDirectory, 'pipes');
        if (!fs.existsSync(pipesDirectory)) {
            fs.mkdirSync(pipesDirectory, {recursive: true});
        }

        // File path for the pipes.json
        const filePath = path.join(pipesDirectory, 'pipes.json');

        // Read the existing JSON data if the file exists
        let existingData = [];
        if (fs.existsSync(filePath)) {
            const fileContent = fs.readFileSync(filePath, 'utf-8');
            existingData = JSON.parse(fileContent);
        }

        // Append the new JSON data
        existingData.push(JSON.parse(jsonString));

        // Write the updated data back to the file
        fs.writeFileSync(filePath, JSON.stringify(existingData, null, 2), 'utf-8');

        return {success: true, message: 'JSON data saved successfully!'};
    } catch (error) {
        console.error('Error saving JSON data:', error);
        return {success: false, message: 'Failed to save JSON data.'};
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
            event.sender.send('python-script-done', code); // Optional: Notify the renderer process
        });

        pythonProcess.on('error', (err) => {
            console.error('Failed to start subprocess.', err);
            reject(err);
        });
    });
});
// const client = new OAuth2Client(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI);

ipcMain.handle('google-sign-in', async () => {
    // Generate the Google OAuth authorization URL
    const url = client.generateAuthUrl({
      access_type: 'offline', // Ensures we get a refresh token
      scope: ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']
    });
    
    const authWindow = new BrowserWindow({
      width: 500,
      height: 600,
      show: true,
      webPreferences: {
        nodeIntegration: false,
        contextIsolation: true,
        webSecurity: true, // Enable web security
      }
    });

    authWindow.loadURL(url);
    authWindow.show();

    return new Promise((resolve, reject) => {
      // Listen for URL navigation changes
      const handleNavigation = async (url) => {
        console.log("Navigated to URL:", url); // Log the URL to see where it's going
        const raw_code = /code=([^&]*)/.exec(url) || null;
        const code = (raw_code && raw_code.length > 1) ? raw_code[1] : null;
        const error = /\?error=(.+)$/.exec(url);

        if (code) {
          console.log("Authorization code found:", code);
          authWindow.destroy();

          try {
            // Exchange the authorization code for access tokens
            const { tokens } = await client.getToken(code);
            client.setCredentials(tokens);
            resolve(tokens); // Send the tokens to the frontend
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

      // Capture the navigation on both will-navigate and did-navigate events
      authWindow.webContents.on('will-navigate', (event, url) => {
        handleNavigation(url);
      });

      authWindow.webContents.on('did-navigate', (event, url) => {
        handleNavigation(url);
      });

      // Close the window on redirect or when the user cancels authentication
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
      // Create an HTTP server
      const server = http.createServer(async (req, res) => {
        if (req.url.startsWith('/callback')) {
          const urlParams = new URL(`http://localhost${req.url}`).searchParams;
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
  
      // Start listening on a random port
      server.listen(0, () => {
        const port = server.address().port;
        const redirectUri = `http://localhost:${port}/callback`;
  
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
  
        // Open the default browser to the authentication URL
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
    }else{
        mainWindow.webContents.send('auth-error', { success: false, error: 'No code found in the query parameters' });

    }
  }

  ipcMain.handle('get-last-signin', async (event, uid) => {
    return new Promise((resolve, reject) => {
        //TODO: get last signin from the database with uid and an axios post
        axios.post('http://localhost:8000/api/getLastSignin/', { uid: uid })
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
        //TODO: update last signin in the database with uid and an axios post
        axios.post('http://localhost:8000/api/updateLastSignin/', { uid: uid })
        .then(response => {
            resolve(response.data);
        })
        .catch(error => {
            reject(error);
        });
    });
  });
