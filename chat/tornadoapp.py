import json
import logging
import os
import signal
import time
import uuid

from urlparse import urlparse
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired

from redis import Redis
from tornado.ioloop import IOLoop
from tornado.options import define, parse_command_line, options
from tornado.web import Application, RequestHandler
from tornado.websocket import WebSocketHandler, WebSocketClosedError
from tornado.httpserver import HTTPServer
from tornadoredis import Client
from tornadoredis.pubsub import BaseSubscriber

define('debug', default=False, type=bool, help='Run in debug mode')
define('port', default=8080, type=int, help='Server port')
define('allow_hosts', default="localhost:8080", multiple=True,
    help='Allow hosts for cross demain connections')


class RedisSubscriber(BaseSubscriber):

    def on_message(self, msg):
        """Trata nova mensagem no canal Redis"""
        if msg and msg.kind == 'message':
            subscribers = list(self.subscribers[msg.channel].keys())
            for subscriber in subscribers:
                try:
                    subscriber.write_message(msg.body)
                except WebSocketClosedError:
                    # remove peer inativo
                    self.unsubscribe(msg.channel, subscriber)
        super().on_message()


class ChatHandler(WebSocketHandler):
    """Trata atualizacoes de tempo real no chat"""

    def check_origin(self, origin):
        allow = super().check_origin(origin)
        parsed = urlparse(origin.lower())
        matched = any(parsed.netloc == host for host in options.allow_hosts)
        return options.debug or allow or matched

    def open(self):
        """" Registra-se para receber atualizacoes"""
        self.chat = None
        channel = self.get_argument('channel', None)
        if not channel:
            self.close()
        else:
            try:
                self.chat = self.application.signer.unsign(
                    channel, max_age=60 * 30)
            except (BadSignature, SignatureExpired):
                self.close()
            else:
                self.uid = uuid.uuid4().hex
                self.application.add_subscriber(self.chat, self)

    def on_message(self, message):
        """Faz o broadcast das atualizacoes para outros clientes"""
        if self.chat is not None:
            self.application.broadcast(message, channel=self.chat, sender=self)

    def on_close(self, chat):
        """Remove o registro"""
        if self.chat is not None:
            self.application.remove_subscriber(self.chat, self)


class UpdateHandler(RequestHandler):
    """Tratar atualizacoes da aplicacao Django"""

    def post(self, pk):
        self._broadcast(pk, 'add')

    def put(self, pk):
        self._broadcast(pk, 'update')

    def delete(self, pk):
        self._broadcast(pk, 'remove')

    def _broadcast(self, pk, action):
        try:
            body = json.loads(self.request.body.decode('utf-8'))
        except ValueError:
            body = None

        message = json.dumps({
            'id': pk,
            'action': action,
            'body': body,
        })
        self.application.broadcast(message, channel=pk)
        self.write("Ok")


class ChatApplication(Application):

    def __init__(self, **kwargs):

        routes = [
            (r'/api/socket', ChatHandler),
            (r'/chat/(?P<pk>[0-9]+)', UpdateHandler),
        ]
        super(ChatApplication, self).__init__(routes, **kwargs)
        self.subscriber = RedisSubscriber(Client())
        self.publisher = Redis()
        self._key = os.environ.get('TORNADOAPP_SECRET',
            'TAfs7y8ajbahvct5r56465avhdsadsg')
        self.signer = TimestampSigner(self._key)

    def add_subscriber(self, channel, subscriber):
        self.subscriber.subscribe(['all', channel], subscriber)

    def remove_subscriber(self, channel, subscriber):
        self.subscriber.unsubscribe(channel, subscriber)
        self.subscriber.unsubscribe('all', subscriber)

    def broadcast(self, message, channel=None, sender=None):
        channel = 'all' if channel is None else channel
        self.publisher.publish(channel, message)


def shutdown(server):
    ioloop = IOLoop.instance()
    logging.info('Stopping server.')
    server.stop()

    def finalize():
        ioloop.stop()
        logging.info('Stopped.')

    ioloop.add_timeout(time.time() + 1.5, finalize)

if __name__ == "__main__":
    parse_command_line()
    application = ChatApplication(debug=options.debug)
    server = HTTPServer(application)
    server.listen(options.port)
    signal.signal(signal.SIGINT, lambda sig, frame: shutdown(server))
    logging.info('Starting server on localhost:{}'.format(options.port))
    IOLoop.instance().start()
