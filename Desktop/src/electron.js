const { app, BrowserWindow, ipcMain, dialog, View } = require('electron');
const path = require('path');
const crypto = require('crypto');
const fs = require('fs');
const { LookupTable, AIModels } = require('./database');
const axios = require('axios');
const FormData = require('form-data')
const { Sequelize } = require('sequelize');
const ffmpegFluent = require('fluent-ffmpeg');
const ffmpegPath = require('ffmpeg-static');
const ffprobePath = require('ffprobe-static').path;
const express = require('express');


const os = require('os');
const { Worker, isMainThread } = require('worker_threads');


async function loadElectronStore() {
    const { default: Store } = await import('electron-store');
    return new Store();
}


async function createWindow() {
    const mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            enableRemoteModule: false,
        },
        autoHideMenuBar: true,
        icon: path.join(__dirname, 'assets', 'HighViz(transparent)-white.png'),
    });

    mainWindow.loadFile('public/index.html');
    // mainWindow.webContents.openDevTools();
    // Initialize the store after the window is created
    store = await loadElectronStore();
}

app.on('ready', createWindow);

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

try {
    require('electron-reloader')(module)
} catch (_) { }

// handler for token storing

let store;

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

// IPC handler for hashing password
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
        const result = await LookupTable.create(record);
        return { success: true, data: result };
    } catch (error) {
        console.error('Failed to insert data:', error);
        return { success: false, error: error.message };
    }
});
// IPC handler for selecting data by mname
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

// IPC handler for updating data by mid
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
ipcMain.handle('fetch-videos', async () => {
    try {
        const records = await LookupTable.findAll({ where: { localurl: { [Sequelize.Op.not]: null } } });
        return { success: true, data: records };
    } catch (error) {
        console.error('Failed to fetch videos:', error);
        return { success: false, error: error.message };
    }
});

// Extract frames handler
ipcMain.handle('extract-frames', async (event, videoPath) => {
    try {
        console.log("VIDEO PATH:", videoPath);

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
        const outputDir = path.join(path.dirname(videoPath), 'frames', videoName);

        // checks if output directory exists

        if (!fs.existsSync(outputDir)) {
            fs.mkdirSync(outputDir, { recursive: true });
        }

        // Checking if the frames are already generated
        const frameFiles = fs.readdirSync(outputDir);
        if (frameFiles.length > 1) {
            console.log('Frames already exist for:', videoPath);
            const framePaths = frameFiles.map(file => path.join(outputDir, file));
            return framePaths;
        }

        console.log('output directory: ', outputDir);

        const MAX_FRAMES = 100;
        const maxFrameCount = Math.min(MAX_FRAMES, Math.floor(duration * 0.5));
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

// IPC handler to run a python script with set parameters
ipcMain.handle('run-python-script', async (event, scriptPath, args) => {
    return new Promise((resolve, reject) => {
        const { spawn } = require('child_process');
        const python = spawn('python', [scriptPath, ...args]);

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
            return { success: true, exists: true };
        } else {
            return { success: true, exists: false };
        }
    } catch (error) {
        console.error('Error checking file existence:', error);
        return { success: false, error: error.message };
    }
});

// IPC handler to delete a video file
ipcMain.handle('delete-video-file', async (event, filePath) => {
    try {
        // Delete the video file - Move it to deleted folder
        if (fs.existsSync(filePath)) {
            // Move the video file to the Deleted folder in development mode
            const deletedDir = path.join(path.dirname(filePath), 'Deleted', path.basename(filePath, path.extname(filePath)));
            fs.mkdirSync(deletedDir, { recursive: true });
            const newFilePath = path.join(deletedDir, path.basename(filePath));
            fs.renameSync(filePath, newFilePath);
        } else {
            return { success: false, error: 'File does not exist' };
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

        return { success: true };
    } catch (error) {
        console.error('Error deleting file or frames:', error);
        return { success: false, error: error.message };
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
            return { success: false, error: 'Video file does not exist' };
        }

        // Get the user's Downloads folder path
        const appDataPath = app.getPath('userData');
        const downloadsDir = path.join(appDataPath, 'Downloads');
        const destinationPath = path.join(downloadsDir, videoName);

        console.log('Moving video file to:', destinationPath);
        console.log('from: ', deletedDir);
        // Move the video file to the Downloads folder
        fs.renameSync(videoFilePath, destinationPath);

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

const server = express();
const PORT = 3000;

server.use((req, res, next) => {
    const type = mime.getType(req.path);
    if (type) {
        res.setHeader('Content-Type', type);
    }
    next();
});

// Serve static files from the "public" directory
server.use(express.static(path.join(__dirname, 'public')));

// Fallback to index.html for single-page applications
server.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});