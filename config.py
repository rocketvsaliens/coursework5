from configparser import ConfigParser


employer_ids = [1124351, 49357, 247279, 3529, 80, 157215, 2180, 84585, 64174, 9498112]


def config(filename="database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    if parser.has_section(section):
        params = parser.items(section)
        db = dict(params)
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db
