# GameliftManagerLocal


This repository contains a Python-based local implementation of Amazon GameLift APIs. It allows developers to test and debug their GameLift integration code on their local development machines without requiring a running GameLift instance.

## Installation
To use this local implementation, you need to install the following dependencies:

- Java 8 or higher
- Python 3.6 or higher
- boto3
- json

To install the required packages, run the following command:

```
pip install boto3 json
```

## Usage

To run the Gamelift Manager Local server, execute the following command:

```
python run.py -l /path/to/GameLiftLocal.jar -e <ipv4_address> -m <max_players>
```

This will run GameliftLocal.jar and start the service on port 80. You can then make requests to the service using the endpoints described below.

### Endpoints
The following endpoints are available:
- `http://localhost/login`: This endpoint authenticates Gamelift user with `username` and `password`.
- `http://localhost/describeplayers`: This endpoint retrieves information about player sessions for a specified game session ID and status filter.
- `http://localhost/startsession`: This endpoint starts a new game session and creates a player session for a specified player ID.
- `http://localhost/describesessions`: This endpoint retrieves information about game sessions.


## Logging

This implementation uses the Python logging library to log events. The logs are stored in the `GameliftManagerlocal.log` file.

## Contributions

We welcome contributions to this repository. If you find any issues or have any suggestions, please feel free to create an issue or pull request.
