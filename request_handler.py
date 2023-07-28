import json
import gamelift_manager_local
from http.server import BaseHTTPRequestHandler
import cgi
import logging

logging.basicConfig(
    filename='GameliftManagerlocal.log', 
    level=logging.INFO,
    format='%(asctime)s:    %(name)s:   %(message)s')


class RequestHandler(BaseHTTPRequestHandler):
    
    def __init__(self, endpoint, maxplayers, *args, **kwargs):
        self.endpoint = endpoint
        self.maxplayers = maxplayers
        logging.info(f'Entrypoint is: {self.endpoint}')
        super().__init__(*args, **kwargs)


    def do_POST(self):
        logging.warning(f'RequestHandler:   Request from {self.client_address[0]}')        
        if self.path == '/describeplayers':
            logging.info('RequestHandler:   Called /describeplayers')
            self.handle_describe_player_sessions()
        elif self.path == '/startsession':
            logging.info('RequestHandler:   Called /startsession')
            self.handle_start_session()
        elif self.path == '/describesessions':
            logging.info('RequestHandler:   Called /describesessions')
            self.handle_describe_game_sessions()
        elif self.path == '/login':
            self.handle_login()
        else:
            logging.info('RequestHandler:   Called 404')
            self.send_error(404)

    def handle_login(self) -> None:
        # Get the request body as bytes and decode it to a string
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = post_data.decode('utf-8')

        # Parse the request body as JSON
        request_data = json.loads(post_data)


        # Inits Gamelift object
        gamelift = gamelift_manager_local.Gamelift_Local()

        # Check if game session already created
        response = gamelift.login(username=request_data['username'], password=request_data['password'])

        response['tokens'] = response['AuthenticationResult']

        # Send the response
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response_json = json.dumps(response)
        self.wfile.write(response_json.encode('utf-8'))

    def handle_describe_game_sessions(self) -> None:
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type'],
            }
        )
        status_filter = form.getvalue('status_filter')

        # Inits Gamelift object
        gamelift = gamelift_manager_local.Gamelift_Local()

        # Check if game session already created
        describe_game_session_result = gamelift.describe_game_sessions(status_filter=status_filter)

        # Send the response
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response_json = json.dumps(describe_game_session_result)
        self.wfile.write(response_json.encode('utf-8'))

    def handle_describe_player_sessions(self) -> None:
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type'],
            }
        )
        game_session_id_request = form.getvalue('game_session_id')
        status_filter = form.getvalue('status_filter')

        # Inits Gamelift object
        gamelift = gamelift_manager_local.Gamelift_Local()

        # Check if game session already created
        describe_game_session_result = gamelift.describe_game_sessions()
        valid_game_session_id = False
        for game_session_obj in describe_game_session_result['GameSessions']:
            if game_session_obj['GameSessionId'] == game_session_id_request:
                valid_game_session_id = True

        # test
        if not valid_game_session_id or len(describe_game_session_result['GameSessions']) == 0:
            response_json = {'Error':'game_session_id is invalid or No available game session'}
        else:
            response_json = gamelift.describe_player_sessions(game_session_id=game_session_id_request, filter=status_filter)

        
        # Send the response
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response_json = json.dumps(response_json)
        self.wfile.write(response_json.encode('utf-8'))


    def handle_start_session(self) -> None:

        # Get the request body as bytes and decode it to a string
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = post_data.decode('utf-8')

        # Parse the request body as JSON
        request_data = json.loads(post_data)


        # Inits Gamelift object
        gamelift = gamelift_manager_local.Gamelift_Local()

        # Check if game session already created
        describe_game_session_result = gamelift.describe_game_sessions(status_filter='ACTIVE')

        available_game_sessions = describe_game_session_result['GameSessions']

        if len(available_game_sessions) == 0:
            create_game_session_result = gamelift.create_game_session(map_name=request_data['gameSessionName'], max_player_count = self.maxplayers)
            game_session_id = create_game_session_result['GameSession']['GameSessionId']
        else:
            game_session_id = describe_game_session_result['GameSessions'][0]['GameSessionId']

        # Create player session
        create_player_session_result = gamelift.create_player_session(player_id=request_data['playerId'], game_session_id=game_session_id)
        if 'PlayerSession' in create_player_session_result:
            logging.info(f'Modifying DnsName with {self.endpoint}')
            create_player_session_result['PlayerSession']['DnsName'] = self.endpoint

        # Send the response
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response_json = json.dumps(create_player_session_result)
        self.wfile.write(response_json.encode('utf-8'))


