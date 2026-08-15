const fs = require('fs');
const path = require('path');

const indexPath = path.join(__dirname, '..', 'frontend', 'index.html');

let content = fs.readFileSync(indexPath, 'utf8');
const apiUrl = process.env.API_URL || '';

const replaced = content.replace(/<meta name="api-url" content=".*">/, `<meta name="api-url" content="${apiUrl}">`);

fs.writeFileSync(indexPath, replaced, 'utf8');
console.log('inject-api: API_URL set to', apiUrl);
