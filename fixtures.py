from os import environ
import sys

import requests

def main():
    root = environ.get('API_ROOT', 'http://localhost:5000')
    key = environ['API_KEY']
    event = environ['API_EVENT']

    _, start, end, num = sys.argv

    num = int(num)

    data = {'start': start, 'end': end}
    headers = {'authorization': 'bearer %s' % key}

    for _ in xrange(num):
        r = requests.post('%s/event/%s/commitment' % (root, event), data=data, headers=headers)


if __name__ == '__main__':
    main()
