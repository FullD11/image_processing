const { spawn } = require('child_process');
const fs = require('fs');

const imagePath = './image.jpg';

const python = spawn('python', ['process_image.py', imagePath]);

let dataString = '';

python.stdout.on('data', (data) => {
  dataString += data.toString();
});

python.stderr.on('data', (data) => {
  console.error('Error:', data.toString());
});

python.on('close', (code) => {
  if (code !== 0) {
    console.error('Python failed');
    return;
  }

  const contours = JSON.parse(dataString);
  console.log(`Found ${contours.length} contours`);

  const html = `<!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.0/dist/katex.min.css">
    </head>
    <body>
        <h1>Contours: ${contours.length}</h1>
        <pre>${JSON.stringify(contours, null, 2)}</pre>
    </body>
    </html>`;

  fs.writeFileSync('output.html', html);
  console.log('Done! Open output.html');
});
