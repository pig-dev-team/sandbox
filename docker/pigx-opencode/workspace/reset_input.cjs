const fs = require('node:fs');
const path = require('node:path');

const workspace = process.argv[2];
for (const relative of ['.agents/skills', 'attachments']) {
    const target = path.join(workspace, relative);
    for (let parent = path.dirname(target); parent !== '/'; parent = path.dirname(parent)) {
        const info = fs.lstatSync(parent, { throwIfNoEntry: false });
        if (info && !info.isDirectory()) throw new Error('invalid directory');
    }
    fs.rmSync(target, { recursive: true, force: true });
}
