"""
This file is part of nucypher.

"""


import os

from twisted.internet import protocol
from twisted.internet import reactor
from twisted.logger import globalLogPublisher

from nucypher.utilities.logging import SimpleObserver


FLEET_POPULATION = 5
DEMO_NODE_STARTING_PORT = 11501
TEACHER_URI = f'146.169.205.219:11500'
REST_IP = f'146.169.205.219'


def spin_up_federated_ursulas(quantity: int = FLEET_POPULATION):

    # Logger
    globalLogPublisher.addObserver(SimpleObserver())

    # Ports
    starting_port = DEMO_NODE_STARTING_PORT
    ports = list(map(str, range(starting_port, starting_port + quantity)))

    ursula_processes = list()
    for index, port in enumerate(ports):

        args = ['nucypher',
                'ursula', 'run',
                '--rest-port', port,
                '--rest-host', REST_IP,
                '--teacher-uri', TEACHER_URI,
                '--federated-only',
                '--dev',
                '--debug',
                '--config-root', 'demo-ursula-{}'.format(port)
                ]

        env = {'PATH': os.environ['PATH'],
               'NUCYPHER_SENTRY_LOGS': '0',
               'NUCYPHER_FILE_LOGS': '0',
               'LC_ALL': 'en_US.UTF-8',
               'LANG': 'en_US.UTF-8'}

        childFDs = {0: 0,
                    1: 1,
                    2: 2}

        class UrsulaProcessProtocol(protocol.Protocol):

            def __init__(self, command):
                self.command = command

        processProtocol = UrsulaProcessProtocol(command=args)
        p = reactor.spawnProcess(processProtocol, 'nucypher', args, env=env, childFDs=childFDs)
        ursula_processes.append(p)

    reactor.run()  # GO!


if __name__ == "__main__":
    spin_up_federated_ursulas()

