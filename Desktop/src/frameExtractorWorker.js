const { parentPort, workerData } = require('worker_threads');
const ffmpegFluent = require('fluent-ffmpeg');
const path = require('path');
const ffmpegPath = require('ffmpeg-static');
const ffprobePath = require('ffprobe-static').path;

async function extractFramesChunk(videoPath, outputDir, startTime, duration, frameRate, threadIndex) {
    return new Promise((resolve, reject) => {
        const outputPattern = path.join(outputDir, `frame-${threadIndex}-%04d.jpg`);
        ffmpegFluent(videoPath)
            .setFfmpegPath(ffmpegPath)
            .setFfprobePath(ffprobePath)
            .seekInput(startTime)
            .duration(duration)
            .videoBitrate('1000k')
            .size('640x360')
            .outputOptions('-vf', `fps=${frameRate}`)
            .output(outputPattern)
            .on('start', (commandLine) => {
                console.log(`Spawned ffmpeg with command: ${commandLine}`);
            })
            .on('stderr', (stderrLine) => {
                console.error(`ffmpeg stderr: ${stderrLine}`);
            })
            .on('error', (err) => {
                console.error('ffmpeg error:', err);
                reject(err);
            })
            .on('end', () => {
                console.log('ffmpeg process finished for chunk');
                resolve();
            })
            .run();
    });
}

const { videoPath, outputDir, startTime, duration, frameRate, threadIndex } = workerData;

extractFramesChunk(videoPath, outputDir, startTime, duration, frameRate, threadIndex)
    .then(() => parentPort.postMessage('done'))
    .catch((error) => {
        console.error('Error in worker thread:', error);
        parentPort.postMessage({ error: error.message });
    });
