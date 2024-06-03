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
    hashPassword: (password) => ipcRenderer.invoke('hash-password', password),
    hashPasswordSalt: (password,salt) => ipcRenderer.invoke('hash-password-salt', password, salt),
    insertData: (record) => ipcRenderer.invoke('insert-data', record),
    selectData: (mname) => ipcRenderer.invoke('select-data', mname),
    updateData: (mid, updates) => ipcRenderer.invoke('ureq', mid, updates),
    uploadFile: (filePath, mid, uid, token, mediaName) => ipcRenderer.invoke('upload-file', filePath, mid, uid, token, mediaName),
});
