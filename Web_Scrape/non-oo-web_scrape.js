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

class Course {
    constructor(title, depts, num, terms, prereqs, units = "4") {
        this.title = title;
        this.depts = depts;
        this.num = num;
        this.terms = terms;
        this.prereqs = prereqs;
        this.units = units;
    }

    toString() {
        let cur = "";
        if (this.depts.length > 1)
            cur += `${this.depts[0]}\${this.depts[1]} `;
        else
            cur += this.depts[0] + " ";
        cur += this.num + " with";
        for (let prereq of this.prereqs) {
            cur += ` ${prereq},`;
        }
        cur += " required";
    }
}

function getAllMatched(regStr, str) {
    let matchesList = [];
    do {
        var res = regStr.exec(str);
        if (res) {
            //console.log(res + " ... " + res[0]);
            //console.log("Course found: " + res[0]);
            matchesList.push(res[0]);
        }
    } while (res);
    return matchesList;
}

var tmp = 0;
let regMatch = /[A-Z]{2,4}(\/[A-Z]{2,4})* [0-9]{3}/g;

function parseSplitPartReqs(splitPart) {
    /*var andCount = (splitPart.match(/and/g) || []).length;
    var count = (temp.match(/is/g) || []).length;*/
    let andSplit = splitPart.split("and ");
    let coursesList = [];
    for (let andS of andSplit) {
        //console.log("andS: " + andS);
        if (andS.length > 1) {
            let orIndex = andS.indexOf("or ");
            let orCount = (andS.match(/or/g) || []).length;
            if (andS.indexOf("or ") >= 0) {
                let matches = getAllMatched(regMatch, andS);
                if (matches.length != orCount + 1) {
                    let orSplit = splitPart.split("or ");
                    let orCourses = [];
                    for (let orS of orSplit) {
                        if (orS.search(regMatch) == -1) {
                            orCourses.push(orS);
                        }
                    }
                    coursesList.push(orCourses);
                }
                else {
                    coursesList.push(matches);
                }
            }
            else {
                coursesList.push([andS]);
            }
        }
    }
    // console.log(coursesList);
    let actualCoursesList = [];
    for (let courses of coursesList) {
        // console.log(courses);
        if (courses.length == 1) {
            actualCoursesList.push(courses[0]);
        }
        else {
            actualCoursesList.push(courses);
        }
    }

    return actualCoursesList;
}

function parsePrereqs(reqsStr) {
    let coursesMatched = [];
    let splitReqs = reqsStr.split("; ");
    /*for (let reqs of splitReqs) {
        do {
            var res = regMatch.exec(reqsStr);
            if (res) {
                //console.log(res + " ... " + res[0]);
                console.log("Course found: " + res[0]);
                courseMatched.push(res[0]);
            }
        } while (res);
    }*/
    for (let req of splitReqs) {
        let courses = parseSplitPartReqs(req);
        for (let course of courses) {
            coursesMatched.push(course);
        }
    }

    return coursesMatched;
}

function getAllCoursesPerProgram(programList) {
    for (let program of programList) {
        var request = new XMLHttpRequest();
        //console.log("Looking at acronym: " + program.acronym);
        request.open("GET", "http://catalog.calpoly.edu/coursesaz/" + program.acronym.toLowerCase(), true);
        request.send(null);
        request.onreadystatechange = function() {
            if (request.readyState == 4) {
                console.log("NEW COURSE...!")
                if (tmp > 2) {
                    console.log("LEAVING");
                    process.exit(1);
                }
                let soup = new jssoup(request.responseText);
                let courses = soup.findAll('div', 'courseblock');
                for (let course of courses) {
                    let desc = course.descendants;
                    /*console.log(desc.length);
                    for (let i = 0; i < desc.length - 1; i++) {
                        if (desc[i].attrs !== undefined) {
                            console.log("i" + " ... " + desc[i].attrs.class + " " + desc[i].name);
                        }
                    }*/
                    let newText = desc[0].text.replace("&#160;", " ");
                    // console.log(desc[0].name + " ... " + desc[0].nextSibling.name + " " + desc[0].nextSibling.attrs.class);
                    let periodIndex = newText.indexOf(".");
                    let lastPeriodIndex = newText.lastIndexOf(".");
                    let spaceIndex = newText.indexOf(" ");
                    console.log(newText.substring(0, spaceIndex) + " " + newText.substring(spaceIndex + 1, periodIndex) + " " + newText.substring(periodIndex + 2, lastPeriodIndex));
                    console.log("Units: " + newText.substring(newText.indexOf("\n") + 1, newText.length));
                    let newText2 = desc[0].nextSibling.text;
                    let reqIndex = newText2.indexOf("Prereq");
                    let termsText = reqIndex == -1 ? newText2 : newText2.substring(0, reqIndex);
                    let terms = termsText.substring(termsText.indexOf(": ") + 2).replace(" ", "").split(",");
                    let prereqs = reqIndex == -1 ? null : newText2.substring(reqIndex + 14).replace(/&#160;/g, " ");
                    let parsedPrereqs = prereqs;
                    console.log("B4 PARSE: " + prereqs);
                    if (parsedPrereqs != null) {
                        parsedPrereqs = parsePrereqs(prereqs);
                    }
                    console.log("Parsed prereqs");
                    console.log(parsedPrereqs);
                }
                tmp++;
            }
        };
    }
}

function getAllPrograms() {
    let programList = [];
    var request = new XMLHttpRequest();
    request.open("GET", "http://catalog.calpoly.edu/coursesaz", true);
    request.send(null);
    request.onreadystatechange = function() {
        if (request.readyState == 4) {
            // console.log("Text back: " + request.responseText);
            let matchReg = /([A-Z]{1}[a-z']* )+.*\([A-Z]{2,4}\)/g;
            // let result = [...((request.responseText).matchAll(matchReg))];
            do {
                //console.log("NEW\n");
                var res = matchReg.exec(request.responseText);
                if (res) {
                    //console.log(res + " ... " + res[0]);
                    //console.log(res[0]);
                    programList.push(new Program(true, res[0]));
                }
            } while (res);
            let len = programList.length;
            for (let i = len / 2; i < len; i++) {
                // console.log(i);
                let a = programList.pop();
                // console.log(a);
            }
            /*console.log(programList);
            console.log(programList.length);*/
            getAllCoursesPerProgram(programList);
        }
    };
}

//getAllPrograms();
getAllCoursesPerProgram([new Program(false, "Comp Sci", "csc")]);
