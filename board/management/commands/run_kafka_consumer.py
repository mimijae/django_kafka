from django.core.management.base import BaseCommand  # 장고의 관리 커맨드를 실행하기 위한 베이스 커맨드를 가져옵니다.
from board.consumers import PostKafkaConsumer  # 게시판 앱에서 정의된 Kafka Consumer를 가져옵니다.

class Command(BaseCommand):  # BaseCommand를 상속받아 새로운 Command 클래스를 만듭니다.
    help = "Runs the Kafka Consumer for Posts."  # 이 커맨드에 대한 도움말 설명을 정의합니다.

    def handle(self, *args, **options):  # 명령어가 호출되면 실행되는 메서드입니다.
        try:
            post_consumer = PostKafkaConsumer()  # PostKafkaConsumer 인스턴스를 생성합니다.
            post_consumer.run()  # PostKafkaConsumer의 run 메서드를 실행하여 Kafka에서 메시지를 받아 처리합니다.
        except Exception as e:  # 메시지 처리 중 예외가 발생하면
            self.stdout.write(self.style.ERROR(f'An error occurred while consuming messages: {e}'))  # 오류 메시지를 출력합니다.
