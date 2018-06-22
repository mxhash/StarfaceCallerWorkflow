import hashlib
import os
import logging
import sys
import xmlrpclib
import ssl


class StarfaceConfig():
    def __init__(self, file):
        self.file = file

        self.__items = ['url', 'user', 'password', 'preferred_device']
        self.url = None
        self.user = None
        self.password = None
        self.preferred_device = None

        self.__load(self.file)

    def __load(self, file):
        with open(file, 'r') as f:
            for item in self.__items:
                setattr(self, item, f.readline().rstrip())

        index = 0
        for item in self.__items[:-1]:
            index+=1
            if not getattr(self, item):
                raise RuntimeError('Config item "{0}" missing (line number {1})'.format(item, index))


class StarfaceCaller():
    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password

        self.proxy = xmlrpclib.ServerProxy(self.uri, verbose=False, use_datetime=True,
                                           context=ssl._create_unverified_context())

    @property
    def uri(self):
        return '{0}/xml-rpc?de.vertico.starface.auth={1}'.format(self.url, self.auth)

    @property
    def auth(self):
        password = hashlib.sha512()
        password.update(self.password)

        auth = hashlib.sha512()
        auth.update(self.user)
        auth.update('*')
        auth.update(password.hexdigest().lower())

        return '{0}:{1}'.format(self.user, auth.hexdigest())

    def get_version(self):
        return self.proxy.ucp.v30.requests.system.getServerVersion()

    def place_call(self, number, preferred_device=''):
        login = self.proxy.ucp.v20.server.connection.login()
        if login:
            self.proxy.ucp.v20.server.communication.call.placeCall(number, preferred_device, '')
            self.proxy.ucp.v20.server.connection.logout()
        else:
            raise RuntimeError('Could not call login on starface')


def main():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    import argparse

    name = os.path.basename(sys.argv[0])

    parser = argparse.ArgumentParser(prog=name,
                                     usage='%(prog)s -n +49911777-777 [ -d SIP/dev ] [ -h ]')

    parser.add_argument('-n', '--number', dest='number', help='Call number')
    parser.add_argument('-d', '--device', dest='device', help='Place call on device, e.g. SIP/mydevice')
    parser.add_argument('-c', '--credential', dest='credential', help='Credential file',
                        default='~/.starface_credentials')

    args = parser.parse_args()

    if not args.number:
        print('{0}: No argument "number" given'.format(name))
        parser.print_usage()
        return 1

    credential = os.path.expanduser(args.credential)
    logger.debug('Using credential file %s', credential)

    config = StarfaceConfig(credential)
    caller = StarfaceCaller(url=config.url, user=config.user, password=config.password)

    logger.debug('Starface Version: %s', caller.get_version())

    preferred_device = ''
    if args.device:
        preferred_device = args.device
    elif config.preferred_device:
        preferred_device = config.preferred_device

    caller.place_call(args.number, preferred_device)

    return 0;


if __name__ == '__main__':
    sys.exit(main())
