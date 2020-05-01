var version = require('./app/gui/package.json');

console.log(version.version)

const gitlog = require("gitlog").default;

const options = {
    repo: __dirname,
    number: 100,
    fields: ["subject"],
    execOptions: { maxBuffer: 1000 * 1024 },
};

var commits = gitlog(options);

if(commits[0].subject.split(" ")[0] == "Merge"){
    parse_version = version.version.split("-")
}