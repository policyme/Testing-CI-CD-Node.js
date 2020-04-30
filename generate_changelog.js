const gitlog = require("gitlog").default;

const options = {
    repo: __dirname,
    number: 10,
    author: "Umang Gupta",
    fields: ["subject"],
    execOptions: { maxBuffer: 1000 * 1024 },
  };

const commits = gitlog(options);
var fs = require('file-system');

const data = fs.readFileSync('CHANGELOG.md')
const fd = fs.openSync('CHANGELOG.md', 'a+')

var content = ''

for (var i = 0; i < commits.length ; i++) {
    console.log(commits[i].subject)
    content +=  commits[i].subject
}

const insert = new Buffer(content)
fs.writeSync(fd, insert, 0, insert.length, 0)
fs.writeSync(fd, data, 0, data.length, insert.length)
fs.close(fd, (err) => {
    if (err) throw err;
  });