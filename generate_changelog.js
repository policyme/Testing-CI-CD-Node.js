const gitlog = require("gitlog").default;

const options = {
    repo: '/Users/umanggupta/Desktop' + "/Testing-CI-CD-Node.js",
    number: 10,
    author: "Umang Gupta",
    fields: ["hash", "abbrevHash", "subject", "authorName", "authorDateRel"],
    execOptions: { maxBuffer: 1000 * 1024 },
  };

const commits = gitlog(options);
console.log(commits);