const {app, BrowserWindow, ipcMain, dialog} = require('electron');
const path = require('path');
const crypto = require('crypto');
const fs = require('fs');
const { LookupTable } = require('./database');
const axios = require('axios');
const FormData = require('form-data')
const { Sequelize } = require('sequelize');

function createWindow() {
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

// try {
//     require('electron-reloader')(module)
// } catch (_) {}

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