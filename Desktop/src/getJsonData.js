const fs = require('fs');
const path = require('path');

function getJsonData(directory) {
    return new Promise((resolve, reject) => {
        fs.readdir(directory, (err, files) => {
            if (err) {
                console.error("Error reading directory:", err);
                return reject(err);
            }

            const jsonFiles = files.filter(file => path.extname(file).toLowerCase() === '.json');

            const readPromises = jsonFiles.map(file => {
                const filePath = path.join(directory, file);
                return new Promise((resolve, reject) => {
                    fs.readFile(filePath, 'utf8', (err, data) => {
                        if (err) {
                            console.error("Error reading JSON file:", err);
                            return reject(err);
                        }

                        try {
                            const jsonData = JSON.parse(data);
                            resolve({
                                filename: file,
                                path: filePath,
                                data: jsonData
                            });
                        } catch (parseErr) {
                            console.error("Error parsing JSON file:", parseErr);
                            reject(parseErr);
                        }
                    });
                });
            });

            Promise.all(readPromises)
                .then(results => resolve(results))
                .catch(err => reject(err));
        });
    });
}

module.exports = { getJsonData };