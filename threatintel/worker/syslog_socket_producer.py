import http.server
import json
import socketserver

from intelhandler.models import LogStatistic
from worker.kafka_producer import MultiProducer

SPLIT_WORD = '|threat|'


def record_to_json(message):
    pattern = {"indicator": "", "config": "", "supplier_name": "", "confidence": ""}
    if SPLIT_WORD in message:
        message = message.split(SPLIT_WORD, maxsplit=1)[1].strip()
        message_dct: dict = json.loads(message)
        return message_dct
    return None


class SyslogKafkaCustom(http.server.BaseHTTPRequestHandler):
    def __init__(self, test_mode=False, *args, **kwargs):
        if test_mode:
            self.messages = []
        self.test_mode = test_mode

        try:
            self.kafka_producer = MultiProducer()
        except:
            pass
        super(SyslogKafkaCustom, self).__init__(*args, **kwargs)

    def handle(self) -> None:
        record = str(self.request.recv(1024), 'ascii')
        if self.test_mode:
            self.messages.append(record)

        result = record_to_json(record)
        if result is not None:
            try:
                LogStatistic.objects.create(data=result)

                self.kafka_producer.send_data(result)
                self.kafka_producer.flush()
            except Exception as e:
                print(e)

        return super(SyslogKafkaCustom, self).handle()


if __name__ == '__main__':
    PORT = 8002
    handler = SyslogKafkaCustom()

    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
