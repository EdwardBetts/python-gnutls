#!/usr/bin/python

import sys, os
script_path = os.path.realpath(os.path.dirname(sys.argv[0]))
gnutls_path = os.path.realpath(os.path.join(script_path, '..'))
sys.path[0:0] = [gnutls_path]

from gnutls.crypto import *
from gnutls.connection import *
from gnutls.errors import *
from gnutls.interfaces.twisted import Credentials

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineOnlyReceiver
from twisted.internet.error import CannotListenError, ConnectionDone
from twisted.internet import reactor

class EchoProtocol(LineOnlyReceiver):
    delimiter = '\n'

    def connectionMade(self):
        print 'New connection from:', self.transport.getPeerCertificate().subject

    def lineReceived(self, line):
        if line == 'quit':
            self.transport.loseConnection()
            return
        self.sendLine(line)

    def connectionLost(self, reason):
        if reason.type != ConnectionDone:
            print "Connection was lost:", str(reason.value)

class EchoFactory(Factory):
    protocol = EchoProtocol


certs_path = os.path.join(script_path, 'certs')

cert = X509Certificate(open(certs_path + '/valid.crt').read())
key = X509PrivateKey(open(certs_path + '/valid.key').read())
ca = X509Certificate(open(certs_path + '/ca.pem').read())
crl = X509CRL(open(certs_path + '/crl.pem').read())
cred = Credentials(cert, key, [ca], [crl])

reactor.listenTLS(10000, EchoFactory(), cred)
reactor.run()

