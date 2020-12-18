#!/usr/bin/python3
from aws_sec_graph.analyze import analyze

import argparse
import sys


__version__ = 'v0.0.1'


class AwsSecGraph(object):

    def __init__(self):
        parser = argparse.ArgumentParser(description='')

        # Optional
        parser.add_argument(
            '--command',
            dest='command',
            action='store',
            type=str,
            help='The command to run the analyze',
            choices=['analyze']
        )

        # Optional
        parser.add_argument('--version', '-v',
                            action='store_true',
                            help='The version of this package')

        args = parser.parse_args(sys.argv[1:2])

        if hasattr(args, 'version') and args.version is not False:
            self.version()
            exit(0)

        if hasattr(args, 'command') and args.command is None:
            print('Unrecognized command')
            parser.print_help()
            exit(1)

        command = args.command.replace('-', '_')

        getattr(self, command)()

    @staticmethod
    def version():
        print(__version__)

    @staticmethod
    def analyze():
        parser = argparse.ArgumentParser(
            description=''
        )

        parser.add_argument('--profile',
                            dest='profile',
                            action='store',
                            type=str,
                            default='default',
                            help='AWS Profile to authenticate, will use the \
                            profiles available on .aws/credentials. \
                            Default: default'
                            )

        parser.add_argument('--filter',
                            dest='filter',
                            action='store',
                            type=str,
                            required=False,
                            default='',
                            help='This is the filter of EC2 instances, \
                            this field used the AWS JSON standard filter. \n \
                            Example: [{"Name": "tag:environment","Values": ["staging"]}]',

                            )

        parser.add_argument('--format',
                            dest='format',
                            action='store',
                            type=str,
                            required=False,
                            default='xdot',
                            help='The format for the file of graph output',
                            choices=['xdot', 'png', 'jpeg', 'pdf', 'svg']
                            )

        parser.add_argument('--port-filter',
                            dest='port_filter',
                            action='store',
                            type=str,
                            required=False,
                            help='Port or port range to generate output graph. \
                                 Example: --port-filter=22 or \
                                 --port-filter=20:22'
                            )
        args = parser.parse_args(sys.argv[2:])

        analyze(args)


def main():
    AwsSecGraph()


if __name__ == '__main__':
    main()
