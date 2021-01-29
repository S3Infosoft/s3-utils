import argparse
from requests import Session
from pathlib import Path
from datetime import datetime
from html import unescape
from json2html import *


# Gets all security hotspots for a project
def get_hot_spots(api_base, project, sq_session, hotspots_file_name):
    # Determines number of results returned per page
    num_of_results = '500'
    page = 1

    # get hotspot keys for a project where ps = number of results per page, p = page index
    # The 'p' value is passed in the while loop
    hotspots_url = api_base + '/hotspots/search?' + 'projectKey=' + project + '&ps=' + num_of_results + '&p='

    # gets information for specific a hotspot
    hotspot_key_search = api_base + '/hotspots/show?hotspot='

    # stores all hotspot keys for later retrieval
    hotspot_key_list = []
    while True:
        response = sq_session.get(hotspots_url+str(page)).json()
        if len(response['hotspots']) == 0:
            break
        # push all keys inside the list
        for hotspot in response['hotspots']:
            hotspot_key_list.append(hotspot['key'])
        page = page + 1

    print('Creating security hotspots report for {}...'.format(project))
    output_html = open(hotspots_file_name, 'w')
    output_html.write('<html><head><link rel="stylesheet" href="style.css"></head><body>')
    for key in hotspot_key_list:
        response = sq_session.get(hotspot_key_search + key).json()
        # the unescape function HTML decodes tags which were encoded by json2html
        raw_html = unescape(json2html.convert(json=response))
        output_html.write(raw_html)
    output_html.write('</body></html>')
    output_html.close()
    print('Done')


# Gets all issues for a projects (Non-security included)
def get_issues(api_base, project, sq_session, issues_file_name):
    # Determines number of results returned per page
    num_of_results = '500'
    page = 1
    # Get issues for a project ps = number of results per page, p = page index & componentKeys is the project name
    issues_url = api_base + '/issues/search?componentKeys=' + project + '&ps=' + num_of_results + '&p='

    print('Creating issues report for {}...'.format(project))
    output_html = open(issues_file_name, 'w')
    output_html.write('<html><head><link rel="stylesheet" href="style.css"></head><body>')
    while True:
        response = sq_session.get(issues_url + str(page)).json()
        if len(response['issues']) == 0:
            break
        raw_html = unescape(json2html.convert(json=response['issues']))
        output_html.write(raw_html)
        page = page + 1
    output_html.write('</body></html>')
    output_html.close()
    print('Done')


def main():
    parser = argparse.ArgumentParser(
        description='Simple script to export all issues & security hotspots from Sonarqube to HTML.'
                    'Optionally place a file named style.css in the SonarqubeOutpout folder.')
    parser.add_argument('token', type=str, metavar='abc2abe8c136563e20bde39e43503f6dd7e8e9f6a',
                        help='Token required to authenticate with the server.Can be obtained from the admin.')
    parser.add_argument('projects', type=str, metavar='NodejsProj,MyApp',
                        help='Comma separated list of project names.(Case sensitive, no spaces)')
    # TO IMPLEMENT LATER
    # Split output into multiple files since a large number of issues will cause a huge final report file
    parser.add_argument('-p', '--paginate', type=int, metavar='100', required=False,
                        help='Splits output into multiple files', default=None)
    args = parser.parse_args()

    projects = args.projects.split(',')
    api_base_url = 'http://localhost:9000/api'
    output_directory = 'SonarqubeOutput'
    Path(output_directory).mkdir(parents=True, exist_ok=True)

    # Authenticates with the Sonarqube WebAPI using basic auth
    # pass token in the username, leaving the password blank
    sonarqube_session = Session()
    sonarqube_session.auth = args.token, ''

    for project in projects:
        current_dt = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
        hotspots_file_name = output_directory + '/' + project + '_sec-hotspot_' + current_dt + '.html'
        issues_file_name = output_directory + '/' + project + '_issues_' + current_dt + '.html'
        get_hot_spots(api_base_url, project, sonarqube_session, hotspots_file_name)
        get_issues(api_base_url, project, sonarqube_session, issues_file_name)


if __name__ == '__main__':
    main()
