import os
from pathlib import Path
import logging
import configparser

# Format logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                            format = '%(asctime)s - %(levelname)s - %(name)s -   %(message)s')


def get_repo_dir():
    """Get repository root directory"""
    root_dir = './'
    if os.path.isdir(Path(__file__).parent.parent / 'src'):
        root_dir = f"{(Path(__file__).parent.parent).resolve()}/"
    elif os.path.isdir('../src'):
        root_dir = '../'
    elif os.path.isdir('./src'):
        root_dir = './'
    else:
        log.warning('Root repository directory not found. This may \
            be an issue when trying to load from /assets or the local config.ini.')
    return root_dir

def get_config(section = None):
    """Load local config file"""
    run_config = configparser.ConfigParser()
    run_config.read(get_repo_dir() + 'config.ini')
    if len(run_config) == 1:
        run_config = None
    elif section is not None:
        run_config = run_config[section]
    return run_config

def get_secret(name, section = None):
    """Get secret or environment variable"""
    config = get_config(section = section)
    value = None

    if config is not None and name in config:
        # Get secret from local config
        log.info(f'Getting secret from config: {name}')
        value = config[name]
    elif name in os.environ:
        # Get secret from environment variable
        log.info(f'Getting secret from environment: {name}')
        value = os.environ[name]

    if value is None:
        raise Exception(f'The secret {name} was not found via utils.get_secret().')

    return value