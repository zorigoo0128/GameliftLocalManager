from functools import partial
from request_handler import RequestHandler
from http.server import HTTPServer
import logging
import subprocess
import argparse
import os
import sys

logging.basicConfig(
    filename='GameliftManagerlocal.log', 
    level=logging.INFO,
    format='%(asctime)s:    %(name)s:   %(message)s')


def main():

    try:
        parser = argparse.ArgumentParser(description="GameliftManagerLocal")
        parser.add_argument('-l', '--gameliftlocal', type=str, default=None, required=True)
        parser.add_argument('-e', '--endpoint', type=str, default="127.0.0.1", required=False)
        parser.add_argument('-m', '--maxplayers', type=int, default=16, required=False)
        args, leftovers = parser.parse_known_args()

        if not args.gameliftlocal or not os.path.isfile(args.gameliftlocal) or not args.endpoint:
            print("Please enter following parameters: -l/--gameliftlocal and -e/--endpoint")
            return

        logging.info(f'Starting GameliftLocal from directory {args.gameliftlocal}')
        logging.info(f'Starting GameliftManagerLocal with endpoint {args.endpoint}')   
        gamelift_process = subprocess.Popen(['java', '-jar', args.gameliftlocal, '-p', '9080'])


        port = 80
        print(f'Starting server on port {port}...')
        logging.info(f'Starting server on port {port}...')         

        handler = partial(RequestHandler, args.endpoint, args.maxplayers)
        httpd =HTTPServer(('', port), handler)
        httpd.serve_forever()


    except KeyboardInterrupt:
        logging.info('Interrupted by keyboard...')  
        print("Exiting...")
        gamelift_process.kill()

        sys.exit(0)


    except Exception as e:
        logging.info('An error occurred:', e)  
        gamelift_process.kill()
        print("An error occurred:", e)

if __name__ == '__main__':
    main()