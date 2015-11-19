#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from src.daemon import Daemon
from src.config import Config
import argparse
import logging


def main():
    reload(sys)
    sys.setdefaultencoding('utf8')
    parser = argparse.ArgumentParser(description="Processing of messages protobuf")
    parser.add_argument('CONFIG_DAEMON', type=str)
    config_file = ""
    try:
        args = parser.parse_args()
        config_file = args.CONFIG_DAEMON
    except argparse.ArgumentTypeError:
        print("Bad usage, learn how to use me with %s -h" % sys.argv[0])
        sys.exit(1)
    config_data = Config()
    config_data.load(config_file)
    daemon = Daemon(config_data)
    daemon.run()

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise
