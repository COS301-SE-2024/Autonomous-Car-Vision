// videoScanner.js
const fs = require('fs');
const path = require('path');

// Function to get video file paths for the Carla Drives
function getVideoFiles(directory) {
  return new Promise((resolve, reject) => {
    fs.readdir(directory, (err, files) => {
      if (err) {
        console.error("erorr reading directory: ", err);
        return reject(err);
      }

      console.log('Files found:', files); 

      const videoFiles = files
        .filter(file => {
          const ext = path.extname(file).toLowerCase();
          return ['.mp4', '.avi', '.mkv', '.mov', '.flv'].includes(ext);
        })
        .map(file => ({
          path: path.join(directory, file),
          type: path.extname(file).toLowerCase()
        }));

      resolve(videoFiles);
    });
  });
}

module.exports = { getVideoFiles };
