import socketserver

from worker.utils import django_init

django_init()

from intelhandler.models import LogStatistic, PatternStorage, Feed
from worker.kafka_producer import MultiProducer
from worker.pattern_module import log_text_to_json
from worker.cron_module import CronModule
from intelhandler.script import parse_custom_json
from worker.collector_consumer import feed_creator


def base_field_extractor(data: dict):
    types = ('json', 'stix', 'free_text', 'misp', 'csv', 'txt')
    base_fields = ["name"]

    for field in base_fields:
        if field not in data:
            for key in data:
                if field in key.lower():
                    data[field] = data[key]
                    break
    if 'type' in data and data['type'] in types:
        pass
    else:
        data['type'] = 'json'


def record_to_json(message: str, pattern: str):
    try:
        log = log_text_to_json(message, pattern)
        base_field_extractor(log)
        log_new = {"feed": log, 'link': log.get('link', log.get('URL', '')), 'type': log.get('type', 'json')}
        log_new['feed']['link'] = log_new.get('link')
        log_new['feed']['format_of_feed'] = log_new.get('type').upper()
        return log_new
    except Exception as e:
        print(e)
        return None


class SyslogKafkaCustom(socketserver.BaseRequestHandler):
    def get_pattern(self):
        return PatternStorage.objects.first().data

    def cron(self):
        self.pattern = self.get_pattern()

    def init(self):
        try:
            self.kafka_producer = MultiProducer()
        except:
            pass

        self.pattern = self.get_pattern()
        cron = CronModule()
        cron.add_job(1, self.cron)
        cron.start()

    def handle(self):
        if not hasattr(self, 'pattern'):
            self.init()

        message = str(bytes.decode(self.request[0].strip()))
        message = message[4:]
        message = message[:-1]

        result = record_to_json(message, self.pattern)
        if result is not None:
            try:
                LogStatistic.objects.create(data=result)

                self.kafka_producer.send_data(result)
                self.kafka_producer.flush()
                print('sent')
                print('\n' * 10, 'Сообщение отправлено')
            except Exception as e:
                # print(e)
                pass


if __name__ == '__main__':
    data = """ <IP-адрес> <ПО>|%Category%| 	%Source_IP%	%Source_port%	%Dest_IP%	%Destanation_port%	%User_name%	%URL%	%URL_domain%	%Event_name%	%Log_source%	%Log_source_identifier%	%Log_source_type%	%Source_Net_Name%	%Source_asset_name%	%Src_Net_Name%   %RE_IP%	%RE_DATE%	%ActionableFields%	%MatchedIndicator%	%Confidence%	%RecordContext%	%SourceId%	%Source_IP feed=%Category%	%Event_code%"""
    pattern = PatternStorage.objects.get_or_create(data=data)

    HOST = 'localhost'
    PORT = 8888

    try:
        server = socketserver.UDPServer((HOST, PORT), SyslogKafkaCustom)
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print("Crtl+C Pressed. Shutting down.")
