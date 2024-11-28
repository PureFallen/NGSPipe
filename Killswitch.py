import os
import requests
from sys import exit
import time
import toml

from lib.colors import BColors
from lib import prints

VERSION = '3.0.1'


if __name__ == '__main__':
    try:
        # Enable ANSI codes (required for Prints/Color)
        os.system('')
        prints.print_info(f'Running Version {VERSION}')

        prints.print_info('Hold up! You are about to killswitch the Webhooks provided in config.toml,')
        prints.print_info('which will cause the script to stop functioning for all members!')
        prints.print_info('You should only do this if you assume that someone is abusing the Webhooks')
        prints.print_info('to damage the Discord Server.')
        prints.print_info('Do you want to continue? (Enter "KILLSWITCH" to continue)')

        choice = input()
        if choice != 'KILLSWITCH':
            exit(0)

        # Read configuration file
        config = toml.load('./config.toml')
        webhook_urls = {config['webhook_url']}
        for command in config['commands']:
            if config['commands'][command]["override_webhook"]:
                webhook_urls.add(config['commands'][command]["override_webhook"])

        # Try to delete Webhooks
        for webhook_url in webhook_urls:
            while True:
                try:
                    response = requests.delete(webhook_url)

                    match response.status_code:
                        # Deletion was successful
                        case 204:
                            prints.print_info(BColors.GREEN + 'Webhook deleted successfully.')
                            break
                        # Webhook not exists or was already deleted
                        case 404:
                            prints.print_error('Webhook not exists or was already deleted.')
                            break
                        # Unknown HTML Status Code
                        case _:
                            prints.print_error(f'Unexpected HTTP Status Code. ({response.status_code})')
                            break
                # Unknown connection error
                except requests.exceptions.ConnectionError as e:
                    prints.print_error(e)
                    time.sleep(5)
        prints.print_info('All Webhooks have been processed.')
        input()

    except KeyboardInterrupt:
        prints.print_info(BColors.YELLOW + 'Program closed by user (CTRL+C)')
        exit(0)
