const fs = require('fs');
const path = require('path');

// Function to recursively get video file paths for folders containing "drive"
function getVideoFiles(directory) {
  return new Promise((resolve, reject) => {
    function readDirectory(dir) {
      return new Promise((res, rej) => {
        fs.readdir(dir, { withFileTypes: true }, (err, entries) => {
          if (err) {
            return rej(err);
          }

          const promises = entries.map((entry) => {
            const fullPath = path.join(dir, entry.name);
            if (entry.isDirectory() && entry.name.toLowerCase().includes('drive')) {
              return readDirectory(fullPath);
            } else if (entry.isFile() && path.extname(entry.name).toLowerCase() === '.mp4' || entry.isFile() && path.extname(entry.name).toLowerCase() === '.avi') {
              return Promise.resolve({
                path: fullPath,
                name: path.basename(dir)  // Use folder name as video name
              });
            }
            return Promise.resolve(null);
          });

          Promise.all(promises)
            .then((results) => {
              // Flatten the array and filter out null values
              const files = results.flat().filter(Boolean);
              res(files);
            })
            .catch(rej);
        });
      });
    }

    readDirectory(directory)
      .then((files) => {
        console.log('MP4 Files found:', files);
        resolve(files);
      })
      .catch((err) => {
        console.error('Error reading directory:', err);
        reject(err);
      });
  });
}

module.exports = { getVideoFiles };
