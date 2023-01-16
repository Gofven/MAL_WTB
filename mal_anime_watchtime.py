import asyncio
import sys
import getopt
from scrapers import get_mal_user_watchtime


def main(argv):
    opts, args = getopt.getopt(argv, "hu:ams", ['help', 'username', 'anime', 'manga', 'save'])
    args = {}

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print("""Usage:
    {-h --help}                      Help menu
    {-u --username}                  MAL Username (Required)
    {-a --anime} OR {-m --manga}     Select relevant watch-time info (default: anime)
    {-s --save}                      Saves to local SQLite database""")
            return

        if opt in ('-u', '--username'):
            args['username'] = arg

        if opt in ('-a', '--anime'):
            args['is_anime'] = True

        if opt in ('-m', '--manga'):
            args['is_anime'] = False

        if opt in ('-s', '--save'):
            args['store_data'] = True

    if 'username' in args.keys():
        asyncio.run(get_mal_user_watchtime(**args))

    else:
        raise Exception('Missing required argument username')


if __name__ == '__main__':
    main(sys.argv[1:])
