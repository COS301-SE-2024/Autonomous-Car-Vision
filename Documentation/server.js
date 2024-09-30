const express = require('express');
const swaggerUi = require('swagger-ui-express');
const YAML = require('yamljs');
const swaggerDocument = YAML.load('./api-contracts/spec.yaml');
const path = require('path');

const HOST_IP = window.electronAPI.getHostIp();

const app = express();
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));


// app.use(express.static(path.join(__dirname, 'public')));

// app.get('*', (req, res) => {
//     res.sendFile(path.join(__dirname, 'public', 'index.html'));
    
// });

app.listen(3000, () => console.log('Server running on http://' + HOST_IP + ':3000/api-docs'));
