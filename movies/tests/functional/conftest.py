import sys

sys.path
sys.path.append('/tests/')
sys.path.append('/fixtures/')

pytest_plugins = [
    "fixtures.http_client_fixtures",
    "fixtures.elastic_fixtures",
    "fixtures.event_loop"]
