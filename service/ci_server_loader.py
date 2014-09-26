import ConfigParser as config

def get_ci_servers():
    config_parser = config.SafeConfigParser(allow_no_value=True)
    config_parser.readfp(open('ci_screen.cfg'))

    sections = config_parser.get('ci_servers', 'sections')
    ci_servers = []
    for section in sections.split(','):

        username = None
        if config_parser.has_option(section, 'username'):
            username = config_parser.get(section, 'username')

        token = None
        if config_parser.has_option(section, 'token'):
            token = config_parser.get(section, 'token')

        ci_servers.append({ 
            'url': config_parser.get(section, 'url'),
            'username': username,
            'token': token })

    return ci_servers


