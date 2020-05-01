function gen_changelog(){

    const gitlog = require("gitlog").default;

    const options = {
        repo: __dirname,
        number: 100,
        author: "Umang Gupta",
        fields: ["subject"],
        execOptions: { maxBuffer: 1000 * 1024 },
    };

    var commits = gitlog(options);

    if(commits[0].subject.split(" ")[0] == "Merge"){

        var version = require('./app/gui/package.json');

        var fs = require('file-system');

        const data = fs.readFileSync('CHANGELOG.md')
        const fd = fs.openSync('CHANGELOG.md', 'a+')

        var todayDate = new Date().toISOString().slice(0,10);

        console.log(todayDate)

        var content = ''

        content += '# ' + version + '( ' + todayDate + ')' + '\n\n'

        for (var i = 0; i < commits.length ; i++) {
              content +=  commits[i].subject + '\n'
        }

        const insert = new Buffer(content)
        fs.writeSync(fd, insert, 0, insert.length, 0)
        fs.writeSync(fd, data, 0, data.length, insert.length)
        fs.close(fd, (err) => {
            if (err) throw err;
        });
    }
}

gen_changelog()