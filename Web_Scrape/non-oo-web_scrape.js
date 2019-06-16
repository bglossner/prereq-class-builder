const jssoup = require('jssoup').default;
const XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
const fetch = require("node-fetch");

class Program {
    constructor(combined, name, acronym = "") {
        if (!combined) {
            this.name = name;
            this.acronym = acronym;
        }
        else {
            let parenIndex = name.indexOf('(');
            this.name = name.substring(0, parenIndex - 1);
            this.acronym = name.substring(parenIndex + 1, name.indexOf(')'));
        }
    }
}

function getAllCoursesPerProgram(programList) {
    for (let program of programList) {
        fetch('http://catalog.calpoly.edu/coursesaz/' + program.acronym)
        .then((response) => {
            console.log(response.text());
            let soup = new JSSoup(response.text());
            let courses = soup.findAll('div', 'courseblock');
        });
    }
}

function getAllPrograms() {
    let programList = [];
    var request = new XMLHttpRequest();
    request.open("GET", "http://catalog.calpoly.edu/coursesaz", true);
    request.send(null);
    request.onreadystatechange = function() {
        if (request.readyState == 4) {
            console.log("Text back: " + request.responseText);
            let matchReg = /([A-Z]{1}[a-z']* )+.*\([A-Z]{2,4}\)/g;
            // let result = [...((request.responseText).matchAll(matchReg))];
            do {
                //console.log("NEW\n");
                var res = matchReg.exec(request.responseText);
                if (res) {
                    //console.log(res + " ... " + res[0]);
                    console.log(res[0]);
                    programList.push(new Program(true, res[0]));
                }
            } while (res);
            let len = programList.length;
            for (let i = len / 2; i < len; i++) {
                console.log(i);
                let a = programList.pop();
                console.log(a);
            }
            console.log(programList);
            console.log(programList.length);
        }
    };
}

getAllPrograms();
