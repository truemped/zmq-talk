#
# Copyright (c) 2008 Daniel Truemper truemped@googlemail.com
#
# setup.py 04-Jan-2011
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# under the License.
#
#

from setuptools import setup, find_packages
import re

tests_require = ['coverage>=3.4']

setup(
    name = "zmqexamples",
    version = "1.0",
    description = "Examples from my ZeroMQ Talk",
    author = "Daniel Truemper",
    author_email = "truemped@googlemail.com",
    url = "",
    license = "Apache 2.0",
    package_dir = { '' : 'src' },
    packages = find_packages('src'),
    include_package_data = True,
    test_suite = 'nose.collector',
    install_requires = [
        'pyzmq>=2.1.7',
    ],
    tests_require = tests_require,
    extras_require = {'test': tests_require},
    entry_points = {
        'console_scripts' : [
            'req = zmqexamples:req',
            'rep = zmqexamples:rep',
            'lruqueue = zmqexamples:lru_queue',
            'lruworker = zmqexamples:lru_worker',
            'lruqueue2 = zmqexamples:lru_queue2',
            'lruworker2 = zmqexamples:lru_worker2',
            'clientquit = zmqexamples:quit_client',
            'device = zmqexamples:device',
            'deviceworker = zmqexamples:device_worker',
        ]
    }
)
