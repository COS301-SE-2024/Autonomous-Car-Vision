const { Sequelize, DataTypes } = require('sequelize');
const path = require('path');

const sequelize = new Sequelize({
    dialect: 'sqlite',
    storage: path.join(__dirname, 'database.sqlite')
});

const LookupTable = sequelize.define('LookupTable', {
    mid: {
        type: DataTypes.INTEGER,
        autoIncrement: true,
        primaryKey: true,
        allowNull: false
    },
    mname: {
        type: DataTypes.TEXT,
        allowNull: false
    },
    localurl: {
        type: DataTypes.TEXT,
        allowNull: true
    },
    size: {
        type: DataTypes.REAL,
        allowNull: false
    },
    uid: {
        type: DataTypes.INTEGER,
        allowNull:false
    }
});

const AIModels = sequelize.define('AIModels', {
    id: {
        type: DataTypes.INTEGER,
        autoIncrement: true,
        primaryKey: true,
        allowNull: false
    },
    model_id: {
        type: DataTypes.STRING,
        unique: true,
        allowNull: false
    },
    model_name: {
        type: DataTypes.STRING,
        allowNull: false
    },
    model_description: {
        type: DataTypes.STRING,
        allowNull: false
    },
    model_version: {
        type: DataTypes.STRING,
        allowNull: false
    },
    model_summary: {
        type: DataTypes.STRING,
        allowNull: false
    },
    model_profileimg: {
        type: DataTypes.STRING,
        allowNull: false
    },
    model_img: {
        type: DataTypes.STRING,
        allowNull: false
    },
    creation_date: {
        type: DataTypes.DATE,
        defaultValue: DataTypes.NOW
    }
});

const VideoTable = sequelize.define('VideoTable', {
    videoID: {
        type: DataTypes.INTEGER,
        autoIncrement: true,
        primaryKey: true,
        allowNull: false
    },
    label: {
        type: DataTypes.STRING,
        allowNull: false
    },
    profileImgURL: {
        type: DataTypes.STRING,
        allowNull: false
    },
    videoURL: {
        type: DataTypes.STRING,
        allowNull: false
    },
    originalVidID: {
        type: DataTypes.INTEGER,
        allowNull: false
    },
    creation_date: {
        type: DataTypes.DATE,
        defaultValue: DataTypes.NOW
    }
});

sequelize.sync().then(async () => {
    const count = await AIModels.count();
    if (count === 0) {
        await AIModels.bulkCreate([
            {
                model_id: '1',
                model_name: 'yolov8n',
                model_description: 'The YOLOv8n (You Only Look Once version 8 nano) model is a lightweight, real-time object detection model designed for high-speed and efficiency.',
                model_version: '1.0',
                model_summary: 'The smallest version of the Yolov8 models.',
                model_profileimg: 'https://cdn.pixabay.com/photo/2024/03/11/19/15/ai-generated-8627457_960_720.png',
                model_img: 'https://cdn.pixabay.com/photo/2024/03/11/19/15/ai-generated-8627457_960_720.png'
            },
            {
                model_id: '2',
                model_name: 'yolov8s',
                model_description: 'The YOLOv8s model is a slightly larger and more accurate version of YOLOv8n, optimized for better performance while maintaining efficiency.',
                model_version: '1.0',
                model_summary: 'The small version of the Yolov8 models.',
                model_profileimg: 'https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExN2RoNjVydWczOGZnN3E5bHhtMWs3ZWlydngzeGNuczNlMjM5Y2JscSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/M9MaCQV4CsWWIhYv7S/giphy.webp',
                model_img: 'https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExN2RoNjVydWczOGZnN3E5bHhtMWs3ZWlydngzeGNuczNlMjM5Y2JscSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/M9MaCQV4CsWWIhYv7S/giphy.webp'
            },
            {
                model_id: '3',
                model_name: 'yolov8n-seg',
                model_description: 'A lightweight model to segment detected objects in a video stream.',
                model_version: '1.0',
                model_summary: 'Segmentation model',
                model_profileimg: 'https://images.unsplash.com/flagged/photo-1554042329-269abab49dc9?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
                model_img: 'https://media1.tenor.com/m/GqOoWCxt5DEAAAAC/fast-car.gif'
            },
            {
                model_id: '4',
                model_name: 'HV1',
                model_description: 'HV1 is an advanced model under development, focused on high-velocity object detection and tracking.',
                model_version: '1.0',
                model_summary: 'Work in progress.',
                model_profileimg: 'https://images.unsplash.com/flagged/photo-1554042329-269abab49dc9?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
                model_img: 'https://media1.tenor.com/m/GqOoWCxt5DEAAAAC/fast-car.gif'
            }
        ]);
    }
});

module.exports = { sequelize, LookupTable, AIModels, VideoTable  };
