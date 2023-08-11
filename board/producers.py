# Kafka 라이브러리에서 KafkaProducer를 임포트합니다.
from kafka import KafkaProducer
# JSON 형식으로 데이터를 다루기 위한 라이브러리를 임포트합니다.
import json
# 로깅을 위한 라이브러리를 임포트합니다.
import logging

# 싱글턴 디자인 패턴을 구현하기 위한 메타 클래스를 정의합니다.
class SingletonMeta(type):
    # 모든 인스턴스를 저장하기 위한 딕셔너리입니다.
    _instances = {}
    
    # 싱글턴 패턴의 중심인 __call__ 메소드를 재정의합니다.
    # 이 메소드는 클래스가 '호출'되었을 때 실행되는데, 
    # 이때 해당 클래스의 인스턴스가 _instances 딕셔너리에 없으면 새로 생성하고,
    # 이미 존재하면 그것을 반환합니다.
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

# 로깅 설정을 초기화합니다. 이 로거는 로그 메시지를 출력할 때 시간, 로그 레벨, 메시지를 포함합니다.
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# Kafka로 메시지를 전송하는 클래스를 정의합니다. 싱글턴 메타클래스를 사용하여 이 클래스는 하나의 인스턴스만 생성합니다.
class PostKafkaProducer(metaclass=SingletonMeta):
    def __init__(self):
        # KafkaProducer 인스턴스를 생성하고 초기화합니다.
        # bootstrap_servers는 Kafka 서버의 위치입니다.
        # value_serializer는 메시지를 JSON 형식으로 직렬화하는 함수입니다.
        # api_version은 사용할 Kafka의 버전입니다.
        self.producer = KafkaProducer(
            bootstrap_servers=['192.168.0.3:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            api_version=(3, 5, 1),
        )

    # 데이터베이스에서 post가 저장될 때 호출되는 메소드입니다.
    # 이 메소드는 신규 생성된 post의 경우 'create' 액션과 함께,
    # 기존 post가 수정된 경우 'update' 액션과 함께 메시지를 Kafka에 전송합니다.
    def send_post_save(self, sender, instance, created, **kwargs):
        if created:  # 만약 새로 생성된 경우
            action = 'create'       
        else:  # 만약 수정된 경우
            action = 'update'
        message = {'action': action, 'id': str(instance.id), 'title': instance.title, 'content': instance.content}
        self.producer.send('test4', message)
        logging.info(f"Sent message: {message}")  # 로깅으로 메시지 전송 사실을 남깁니다.

    # 데이터베이스에서 post가 삭제될 때 호출되는 메소드입니다.
    # 이 메소드는 'delete' 액션과 함께 메시지를 Kafka에 전송합니다.
    def send_post_delete(self, sender, instance, **kwargs):
        message = {'action': 'delete', 'id': str(instance.id)}
        self.producer.send('test4', message)
        logging.info(f"Sent message: {message}")  # 로깅으로 메시지 전송 사실을 남깁니다.
