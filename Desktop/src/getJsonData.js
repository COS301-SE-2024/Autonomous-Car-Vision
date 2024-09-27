const fs = require('fs');
const path = require('path');

// Function to get JSON file paths
function getJsonData(directory) {
    return new Promise((resolve, reject) => {
      fs.readdir(directory, (err, files) => {
        if (err) {
          console.error("Error reading directory:", err);
          return reject(err);
        }
  
        const jsonFiles = files.filter(file => path.extname(file).toLowerCase() === '.json');
  
        const jsonDataArray = [];
  
        jsonFiles.forEach((file, index) => {
          const filePath = path.join(directory, file);
  
          fs.readFile(filePath, 'utf8', (err, data) => {
            if (err) {
              console.error("Error reading JSON file:", err);
              return reject(err);
            }
  
            try {
              const jsonData = JSON.parse(data);
              jsonDataArray.push({
                filename: file,
                path: filePath,
                data: jsonData
              });
  
              // If all files have been read, resolve the promise
              if (jsonDataArray.length === jsonFiles.length) {
                resolve(jsonDataArray);
              }
            } catch (parseErr) {
              console.error("Error parsing JSON file:", parseErr);
              return reject(parseErr);
            }
          });
        });
  
        // If no JSON files were found, resolve with an empty array
        if (jsonFiles.length === 0) {
          resolve([]);
        }
      });
    });
  }
  
  module.exports = { getJsonData };
  