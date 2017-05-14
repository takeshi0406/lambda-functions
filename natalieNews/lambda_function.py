import os
import yaml
import natalie_to_twitter as nt


CONFIG_PATH = './config.yaml'
API_ENV_KEY = ['TOKEN', 'TOKEN_SECRET', 'CONSUMER_KEY', 'CONSUMER_SECRET']


def lambda_handler(event, context):
    config = _read_config()
    tw_conf = {k.lower(): os.environ[k] for k in API_ENV_KEY}
    oauth = nt.OAuth(**tw_conf)
    bot = nt.NatalieBot(
            oauth, exec_span=int(os.environ['EXEC_SPAN']),
            target_tags=config['target_tags'])
    bot.run()


def _read_config():
    with open(CONFIG_PATH) as f:
        conf = yaml.load(f)
    return conf
