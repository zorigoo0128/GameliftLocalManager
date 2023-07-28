import boto3
import json
import logging

logging.basicConfig(
    filename='GameliftManagerlocal.log', 
    level=logging.INFO,
    format='%(asctime)s:    %(name)s:   %(message)s')

# enter USER_POOL_APP_CLIENT_ID here 
USER_POOL_APP_CLIENT_ID = ""

class Gamelift_Local:

    def __init__(self) -> None:
        self.gamelift_client = boto3.client('gamelift', endpoint_url=f'http://127.0.0.1:9080')
        self.cognito_client = client = boto3.client("cognito-idp")
        logging.info('Gamelift Local Init')
        

    def login(self, username : str, password : str):
        if not username or not password:
            logging.info(f'Gamelift Local:   Request login called with failed')
            return json.loads({'ErrorMessage','Please enter username and password'})
        logging.info(f'Gamelift Local:   Request login called with parameters: \n\tusername {username}, \n\tpassword: {password}')
        response = self.cognito_client.initiate_auth(
            ClientId=USER_POOL_APP_CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": username, "PASSWORD": password},
        )
        return json.loads(json.dumps(response))


    def create_game_session(self, map_name : str = '', max_player_count : int = 16, fleet_id : str = 'fleet-123'):
        logging.info(f'Gamelift Local:   Request create_game_session called with parameters: \n\tmap_name: {map_name} , \n\tmax_player_count: {max_player_count}, \n\tfleet_id: {max_player_count}')
        response = self.gamelift_client.create_game_session(
            FleetId=fleet_id,
            MaximumPlayerSessionCount=max_player_count,
            Name=map_name
        )        
        return json.loads(json.dumps(response))


    def describe_game_sessions(self, fleet_id : str = 'fleet-123', status_filter : str = None):
        logging.info(f'Gamelift Local:   Request describe_game_sessions called with parameters:  \n\tfleet_id: {fleet_id}')
        if status_filter:

            response = self.gamelift_client.describe_game_sessions(
                FleetId=fleet_id,
                StatusFilter = status_filter
            )
        else:
            response = self.gamelift_client.describe_game_sessions(
                FleetId=fleet_id
            )
        return json.loads(json.dumps(response))

    def create_player_session(self, player_id : str = '', game_session_id : str = ''):
        logging.info(f'Gamelift Local:   Request create_player_session called with parameters:  \n\tplayer_id: {player_id}, \n\tgame_session_id: {game_session_id}')
        response = self.gamelift_client.create_player_session(
            GameSessionId=game_session_id,
            PlayerId=player_id
        )
        return json.loads(json.dumps(response, indent=4, sort_keys=True, default=str))
    

    def describe_player_sessions(self, game_session_id : str = '', filter : str =''):
        logging.info(f'Gamelift Local:   Request describe_player_sessions called with parameters:  \n\tgame_session_id: {game_session_id}, \n\tfilter: {filter}')
        if filter:
            response = self.gamelift_client.describe_player_sessions(
                GameSessionId=game_session_id,
                PlayerSessionStatusFilter=filter
            )
        else:
            response = self.gamelift_client.describe_player_sessions(
                GameSessionId=game_session_id
            )
        return json.loads(json.dumps(response, indent=4, sort_keys=True, default=str))


    def get_number_of_players(self, game_session_id : str) -> int:
        logging.info(f'Gamelift Local:   Request describe_player_sessions called with parameters:  \n\tgame_session_id: {game_session_id}, \n\tfilter: {filter}')

        player_sessions = self.describe_player_sessions(game_session_id=game_session_id)

        number = 0
        if 'PlayerSessions' in player_sessions:
            for player_info in player_sessions['PlayerSessions']:
                if 'Status' in player_info and (player_info['Status'] == 'ACTIVE' or player_info['Status'] == 'RESERVED'):
                    number += 1

        return number
    
