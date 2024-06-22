window.addEventListener('DOMContentLoaded', () => {
    const replaceText = (selector, text) => {
      const element = document.getElementById(selector);
      if (element) element.innerText = text;
    }
  
    for (const type of ['chrome', 'node', 'electron']) {
      replaceText(`${type}-version`, process.versions[type]);
    }
  });
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    storeToken: (token) => ipcRenderer.send('store-token', token),
    getToken: () => ipcRenderer.sendSync('get-token'),
    clearToken: () => ipcRenderer.sendSync('clear-token'),
    storeUname: (uname) => ipcRenderer.send('store-uname', uname),
    getUname: () => ipcRenderer.sendSync('get-uname'),
    clearUname: () => ipcRenderer.sendSync('clear-uname'),
    storeUid: (uid) => ipcRenderer.send('store-uid', uid),
    getUid: () => ipcRenderer.sendSync('get-uid'),
    clearUid: () => ipcRenderer.sendSync('clear-uid'),
    storeUemail: (uemail) => ipcRenderer.send('store-uemail', uemail),
    getUemail: () => ipcRenderer.sendSync('get-uemail'),
    clearUemail: () => ipcRenderer.sendSync('clear-uemail'),
    hashPassword: (password) => ipcRenderer.invoke('hash-password', password),
    hashPasswordSalt: (password,salt) => ipcRenderer.invoke('hash-password-salt', password, salt),
    insertData: (record) => ipcRenderer.invoke('insert-data', record),
    selectData: (mname) => ipcRenderer.invoke('select-data', mname),
    updateData: (mid, updates) => ipcRenderer.invoke('ureq', mid, updates),
    uploadFile: (filePath, mid, uid, token, mediaName) => ipcRenderer.invoke('upload-file', filePath, mid, uid, token, mediaName),
    openFileDialog: () => ipcRenderer.invoke('open-file-dialog'),
    fetchVideos: () => ipcRenderer.invoke('fetch-videos'),
    extractFrames: (videoPath) => ipcRenderer.invoke('extract-frames', videoPath),
    saveFile: (fileBuffer, fileName) => ipcRenderer.invoke('save-file', fileBuffer, fileName),
    runPythonScript: (scriptPath, args) => ipcRenderer.invoke('run-python-script', scriptPath, args),
    checkFileExistence: (filePath) => ipcRenderer.invoke('check-file-existence', filePath),
    deleteVideoFile: (filePath) => ipcRenderer.invoke('delete-video-file',filePath),
    getVideoFrame: (videoPath) => ipcRenderer.invoke('get-video-frame', videoPath),
  });
