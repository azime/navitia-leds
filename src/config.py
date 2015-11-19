# -*- coding: utf-8 -*-

#  Copyright (c) 2001-2014, Canal TP and/or its affiliates. All rights reserved.
#
# This file is part of Navitia,
#     the software to build cool stuff with public transport.
#
# Hope you'll enjoy and contribute to this project,
#     powered by Canal TP (www.canaltp.fr).
# Help us simplify mobility and open public transport:
#     a non ending quest to the responsive locomotion way of traveling!
#
# LICENCE: This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Stay tuned using
# twitter @navitia
# IRC #navitia on freenode
# https://groups.google.com/d/forum/navitia
# www.navitia.io

import logging
import logging.config
import json
import sys


class Config(object):

    def __init__(self):
        self.rabbitmq = None

    def load(self, config_file):
        """
        Initialize from a configuration file.
        If not valid raise an error.
        """
        config_data = json.loads(open(config_file).read())

        if 'logger' in config_data:
            logging.config.dictConfig(config_data['logger'])
        else:  # Default is std out
            handler = logging.StreamHandler(stream=sys.stdout)
            logging.getLogger().addHandler(handler)
            logging.getLogger().setLevel('INFO')

        if 'rabbitmq' in config_data:
            self.rabbitmq = config_data['rabbitmq']
        else:
            raise ValueError("Config is not valid, rabbitmq is needed")
