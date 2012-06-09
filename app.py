from os import environ

import crowdshift

def main():
    app = crowdshift.create_app()

    host = environ.get('HOST', '0.0.0.0')
    port = int(environ.get('PORT', 5000))
    debug = environ.get('DEBUG') is not None

    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    main()
