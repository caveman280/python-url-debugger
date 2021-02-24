import sys
import json
import argparse

from fetch import FetchUrl  # noqa

class CLI(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="A CLI utility to debug URLs",
            usage = '''url_debugger <command> [<args>]
            The most commonly used cli commands are:
               fetch       From a given list of URLs, make a request and describe the responses
            '''.format(msg="NOT_CURRENTLY_SUPPORTED")
        )

        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])

        if not hasattr(self, args.command):
            print('Unrecognised command')
            parser.print_help()
            exit(1)

        getattr(self, args.command)()

    def _load(self, filename):
        with open(filename, "r") as f:
            return f.read()


    def fetch(self):
        self.urls = []  # an empty list which will be filled with instances of FetchUrl
        parser = argparse.ArgumentParser(description="From a given list of URLs, make a request and describe the responses")
        parser.add_argument('-u', action='append', help="A single URL to test", nargs="+")
        parser.add_argument('-f', action='append', help="A path to a file of URLs seperated by a new line")
        parser.add_argument('-l', action='store_false', help="Dont follow redirects")

        # First check valid arguments have been passed
        try:
            _args = parser.parse_args(sys.argv[2:])
            if _args.u is None and _args.f is None:
                raise Exception
        except:
            print('Unrecognised command')
            parser.print_help()
            exit(1)
        
        # Then, formulate our list of URLs
        if _args.u is not None:
            for url in _args.u:
                self.urls.append(
                    FetchUrl(
                        url[0].strip(),  # strip any whitespaces
                        follow_redirects=_args.l
                    )
                )
        if _args.f is not None:
            try:
                file_urls = self._load(_args.f[0])
            except (OSError, IOError):
                print('The file does not exist or could not be read. Please check the file path.')
                parser.print_help()
                exit(1)
            
            for line in file_urls.splitlines():
                self.urls.append(
                    FetchUrl(
                        line.strip().split()[0],  # split at any whitespace and take the first argument
                        follow_redirects=_args.l
                    )
                )

        for request in self.urls:
            request.fetch()
        
        for result in self.urls:
            print(json.dumps(result.as_dict()))