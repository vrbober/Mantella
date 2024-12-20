import sys
from src.http.http_server import http_server
import traceback
from src.http.routes.routeable import routeable
from src.http.routes.mantella_route import mantella_route
from src.http.routes.stt_route import stt_route
import logging
import src.setup as setup
from src.ui.start_ui import StartUI

# Ensure sys.stdout and sys.stderr use UTF-8 encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Configure logging to use the updated streams
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

def main():
    try:
        config, language_info = setup.initialise(
            config_file='config.ini',
            logging_file='logging.log', 
            language_file='data/language_support.csv')

        mantella_version = '0.12'
        logging.log(24, f'\nMantella v{mantella_version}')
        should_debug_http = config.show_http_debug_messages

        mantella_http_server = http_server()

        #start the http server
        conversation = mantella_route(config, 'GPT_SECRET_KEY.txt', language_info, should_debug_http)
        stt = stt_route(config, 'STT_SECRET_KEY.txt', 'GPT_SECRET_KEY.txt', should_debug_http)
        ui = StartUI(config)
        routes: list[routeable] = [conversation, stt, ui]
            
        #add the UI
        mantella_http_server.start(int(config.port), routes, config.show_http_debug_messages)

    except Exception as e:
        logging.error("".join(traceback.format_exception(e)))
        input("Press Enter to exit.")

if __name__ == '__main__':
    main()
