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
    serverurl: {
        type: DataTypes.TEXT,
        allowNull: true
    }
});

sequelize.sync();

module.exports = { sequelize, LookupTable };
