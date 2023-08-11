from kafka import KafkaConsumer    # 카프카 컨슈머 라이브러리를 가져옵니다.
import json                        # JSON 처리 라이브러리를 가져옵니다.
import logging                     # 로깅 라이브러리를 가져옵니다.
from .serializers import PostSerializer  # PostSerializer를 가져옵니다.
from .models import Post           # Post 모델을 가져옵니다.



# 로그 설정 추가
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

class PostKafkaConsumer:
    def __init__(self):
        # 카프카 관련 로그 레벨 설정 추가
        kafka_logger = logging.getLogger('kafka')
        kafka_logger.setLevel(logging.WARNING)

        # KafkaConsumer 인스턴스를 생성합니다.
        self.consumer = KafkaConsumer(
            'test2',  # 토픽 이름을 입력합니다.
            bootstrap_servers=['192.168.0.3:9092'],  # 카프카 서버의 위치를 입력합니다.
            group_id='foo',  # 그룹 아이디를 입력합니다.
            auto_offset_reset='latest',  # 가장 최근에 생성된 메시지부터 가져옵니다.
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # JSON 형식의 메시지를 파싱합니다.
            api_version=(3, 5, 1),  # 카프카 서버의 버전을 입력합니다.
        )

    def run(self):
        # 카프카 서버에 연결할 수 있는지 확인합니다.
        try:
            self.consumer.poll(timeout_ms=1000)  # 서버와의 연결을 확인하기 위해 폴링을 시도합니다.
            logging.info("카프카 서버에 성공적으로 연결되었습니다.")  # 로그 추가
        except Exception as ex:
            logging.error(f"카프카에 연결하는 중 예외 발생: {ex}")  # 예외가 발생하면 오류 로그를 출력합니다.

        # 메시지 처리 루프
        while True:
            try:
                # 카프카 컨슈머에서 메시지를 가져옵니다.
                for message in self.consumer:
                    data = message.value  # 메시지의 값에 대한 데이터를 얻습니다.
                    
                    # 콘솔에 메시지 데이터를 출력합니다.
                    print(f"수신한 메시지: {data}")

                    # 동작에 따라 처리합니다.
                    if data['action'] == 'create':  # 'create' 동작의 경우
                        serializer = PostSerializer(data=data)  # 데이터를 PostSerializer에 입력합니다.
                        if serializer.is_valid():  # 입력한 데이터가 유효하면
                            serializer.save()  # 데이터를 저장합니다.
                    elif data['action'] == 'update':  # 'update' 동작의 경우
                        try:
                            post = Post.objects.get(id=data['id'])  # 데이터의 'id'에 해당하는 포스트를 가져옵니다.
                            serializer = PostSerializer(post, data=data)  # 가져온 포스트와 데이터를 PostSerializer에 입력합니다.
                            if serializer.is_valid():  # 입력한 데이터가 유효하면
                                serializer.save()  # 데이터를 저장합니다.
                        except Post.DoesNotExist:  # 해당하는 포스트가 없으면
                            pass  # 무시하고 넘어갑니다.
                    elif data['action'] == 'delete':  # 'delete' 동작의 경우
                        try:
                            post = Post.objects.get(id=data['id'])  # 데이터의 'id'에 해당하는 포스트를 가져옵니다.
                            post.delete()  # 가져온 포스트를 삭제합니다.
                        except Post.DoesNotExist:  # 해당하는 포스트가 없으면
                            pass  # 무시하고 넘어갑니다.
            except KeyboardInterrupt:  # 키보드 인터럽트가 발생하면
                logging.warning("중단됨")  # 경고 로그를 출력합니다.
                break  # 루프를 종료합니다.
            except Exception as ex:  # 예외가 발생하면
                logging.error(f"메시지를 소비하는 도중 예외 발생: {ex}")  # 오류 로그를 출력합니다.
