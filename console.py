from IPython import embed

import crowdshift

def main():
    app = crowdshift.create_app()

    from crowdshift import rc

    with app.test_request_context():
        embed(display_banner=False)

if __name__ == '__main__':
    main()
