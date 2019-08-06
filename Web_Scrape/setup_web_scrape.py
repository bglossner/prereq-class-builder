import re
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def get_majors():
    url = 'http://catalog.calpoly.edu/coursesaz/#text'
    response = simple_get(url)
    courses = {}
    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        for td in html.find_all('td'):
            course = re.search("(([\w][a-z']+\s?)+)\(([A-Z]+)\)", td.text)
            courses[course.group(1).rstrip()] = course.group(3)
    else:
        print("Response was null")
    print(courses)
    return courses

def getCourses(majorName):
    url = "http://catalog.calpoly.edu" + majorName
    response = simple_get(url)
    print(url)
    if response:
        html = BeautifulSoup(response, 'html.parser')
        table =  html.find('table', attrs={"class": "sc_courselist"})
        for tr in table.find_all('tr'):
            if tr.text == "MAJOR COURSES":
                major = True
            elif tr.text == "SUPPORT COURSES":
                support = True
                major = False
            elif major:
                rows = tr.findAll('td')
                course = {}
                course['cid'] = rows[0].text
                course['name'] = rows[1].text
                try:
                    course['units'] = rows[2].text
                    print(course)
                except:
                    if re.search("^or.*$", rows[0].text):
                        course['units'] = None
                        print(course)
                    else:
                        print("Not a course")

    else:
        print("Invalid URL")

def getMajors():
    url = 'http://catalog.calpoly.edu/programsaz/'
    response = simple_get(url)
    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        for p in html.find_all('p'):
            match = re.search("^([\w\s]+), (BS|BArch|BFA|BA|BLA)", p.text)
            if (match):
                url = p.find('a')['href']
                majorName = match.group(1)
                print("For: ", majorName, url)
                getCourses(url)

getCourses("/collegesandprograms/collegeofengineering/generalengineering/bsgeneralengineering/")
