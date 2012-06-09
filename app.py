from os import environ

import crowdshift

if __name__ == '__main__':
    app = crowdshift.create_app()

    host = environ.get('HOST', '0.0.0.0')
    port = int(environ.get('PORT', 5000))
    debug = environ.get('DEBUG') is not None

    app.run(host=host, port=port, debug=debug)
