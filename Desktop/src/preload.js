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
    getAppPath: async () => await ipcRenderer.invoke('get-app-path'),
    resolvePath: async (...segments) => await ipcRenderer.invoke('resolve-path', ...segments),
    readDirectory: (directoryPath) => ipcRenderer.invoke('read-directory', directoryPath),
    storeToken: (token) => ipcRenderer.send('store-token', token),
    getToken: () => ipcRenderer.sendSync('get-token'),
    clearToken: () => ipcRenderer.sendSync('clear-token'),
    storeUname: (uname) => ipcRenderer.send('store-uname', uname),
    getUname: () => ipcRenderer.sendSync('get-uname'),
    clearUname: () => ipcRenderer.sendSync('clear-uname'),
    storeUid: (uid) => ipcRenderer.send('store-uid', uid),
    getUid: () => ipcRenderer.sendSync('get-uid'),
    clearUid: () => ipcRenderer.sendSync('clear-uid'),
    storePrevPath: (prevPath) => ipcRenderer.send('store-prev-path', prevPath),
    getPrevPath: () => ipcRenderer.sendSync('get-prev-path'),
    clearPrevPath: () => ipcRenderer.sendSync('clear-prev-path'),
    storeUemail: (uemail) => ipcRenderer.send('store-uemail', uemail),
    getUemail: () => ipcRenderer.sendSync('get-uemail'),
    clearUemail: () => ipcRenderer.sendSync('clear-uemail'),
    storeTeamName: (teamName) => ipcRenderer.send('store-team-name', teamName),
    getTeamName: () => ipcRenderer.sendSync('get-team-name'),
    clearTeamName: () => ipcRenderer.sendSync('clear-team-name'),
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
    fileExists: (filePath) => fs.existsSync(path.resolve(filePath)),
    runPythonScript: (scriptPath, args) => ipcRenderer.invoke('run-python-script', scriptPath, args),
    uploadToAgent: (ip, port, filepath, uid, size, token, mname) => ipcRenderer.invoke('upload-to-agent', ip, port, filepath, uid, size, token, mname),
    downloadToClient: (ip, port, filepath, uid, size, token) => ipcRenderer.invoke('download-to-client', ip, port, filepath, uid, size, token),
    checkFileExistence: (filePath) => ipcRenderer.invoke('check-file-existence', filePath),
    deleteVideoFile: (filePath) => ipcRenderer.invoke('delete-video-file',filePath),
    getVideoFrame: (videoPath) => ipcRenderer.invoke('get-video-frame', videoPath),
    downloadVideo: (videoName, filePath) => ipcRenderer.invoke('move-deleted-video-to-downloads', videoName, filePath),
    getAIModels: () => ipcRenderer.invoke('get-ai-models'),
    loadStoreProcess: () => ipcRenderer.sendSync('load-store-process'),
    saveStoreProcess: async (store) => await ipcRenderer.invoke('save-store-process', store),
    queueVideo: (videoDetails) => ipcRenderer.invoke('queue-video', videoDetails),
    getVideoByURL: (videoURL) => ipcRenderer.invoke('getVideoByURL', videoURL),
    checkIfVideoProcessed: (videoUrl) => ipcRenderer.invoke('checkIfVideoProcessed', videoUrl),
    getProcessedVideos: (originalVidID) => ipcRenderer.invoke('getProcessedVideos', originalVidID),
    addVideo: (videoData) => ipcRenderer.invoke('addVideo', videoData),
    onPythonScriptDone: (callback) => ipcRenderer.on('python-script-done', callback),
    checkCUDA: () => ipcRenderer.invoke('check-cuda'),
    onProcessChanged: (callback) => ipcRenderer.on('process-changed', callback),
    selectDrivesDirectory: () => ipcRenderer.invoke('selectDrivesDirectory'),
    getDrivesDirectory: () => ipcRenderer.invoke('getDrivesDirectory'),
    getDriveVideos: (directory) => ipcRenderer.invoke('getDriveVideos', directory),
    readDriveLog: (directory) => ipcRenderer.invoke('readDriveLog', directory),
    moveVideo: (sourcePath, destFileName) => ipcRenderer.invoke('move-video', sourcePath, destFileName),
    openFTP: (event, uid, token, size, media_name, media_url, command) => ipcRenderer.invoke('open-ftp', event, uid, token, size, media_name, media_url, command),
    getFileSize: (filePath) => ipcRenderer.invoke('get-file-size', filePath),
    savePipeJson: async (jsonString) => { const result = await ipcRenderer.invoke('save-pipe-json', jsonString);  return result;},
    runPythonScript2: (scriptPath, args = []) => ipcRenderer.invoke('run-python-script2', scriptPath, args),
    googleSignIn: () => ipcRenderer.invoke('google-sign-in'),
    // Optional: Listen for the script completion event

});
