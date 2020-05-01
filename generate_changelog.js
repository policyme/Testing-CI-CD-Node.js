function is_pull_request(commit){
    parse_array = commit.split(" ")
        if(parse_array[0] == 'Merge' && parse_array[1] == 'pull' && parse_array[2] == 'request'){
            return true
        }
    return false
}

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
    let ticket_set = new Set()

    if(commits[0].subject.split(" ")[0] == "Merge"){

        var version = require('./app/gui/package.json');

        var fs = require('file-system');

        const data = fs.readFileSync('CHANGELOG.md')
        const fd = fs.openSync('CHANGELOG.md', 'a+')

        var todayDate = new Date().toISOString().slice(0,10).toString();

        var content = ''

        content += '# ' + version + '(' + todayDate + ')' + '\n\n'

        for (var i = 0; i < commits.length ; i++) {
            if (commits[i].subject != "Updating the CHANGELOG.md and the _version file"){
                if(is_pull_request(commits[i].subject)){
                    ticketNumber = commits[0].subject.split(" ")[5].split("/")[2].split("-")
                    ticketNumber = ticketNumber.slice(0,2).join("-")
                    ticket_set.add(ticketNumber)
                }
            }
        }

        console.log(ticket_set)

        

        const insert = new Buffer(content)
        fs.writeSync(fd, insert, 0, insert.length, 0)
        fs.writeSync(fd, data, 0, data.length, insert.length)
        fs.close(fd, (err) => {
            if (err) throw err;
        });
    }
}

gen_changelog()