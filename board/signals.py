# 이 코드는 Django의 시그널을 사용하여 Post 모델의 저장 및 삭제 이벤트가 발생하면 Kafka로 메시지를 전송하는 것입니다.

# Django의 데이터베이스 모델이 저장 및 삭제된 후에 실행되는 시그널을 임포트합니다.
from django.db.models.signals import post_save, post_delete
# 시그널과 함수를 연결하기 위한 장식자를 임포트합니다.
from django.dispatch import receiver
# Post 모델을 임포트합니다.
from .models import Post
# 위에서 정의한 Kafka 메시지 전송 클래스를 임포트합니다.
from .producers import PostKafkaProducer

# PostKafkaProducer의 인스턴스를 생성합니다. 
# 이 클래스는 싱글턴 패턴을 사용하므로 이후에 같은 클래스로 생성하는 인스턴스는 이 인스턴스와 같습니다.
producer_instance = PostKafkaProducer()

# post_save 시그널이 발생하면 post_saved 함수를 실행하도록 연결합니다.
# 이 함수는 Post 모델 인스턴스가 데이터베이스에 저장된 후에 호출됩니다.
@receiver(post_save, sender=Post)
def post_saved(sender, instance, created, **kwargs):
    # 생성된 인스턴스와 인스턴스가 새로 생성되었는지 여부를 파라미터로 하여 Kafka로 메시지를 전송합니다.
    producer_instance.send_post_save(sender, instance, created, **kwargs)

# post_delete 시그널이 발생하면 post_deleted 함수를 실행하도록 연결합니다.
# 이 함수는 Post 모델 인스턴스가 데이터베이스에서 삭제된 후에 호출됩니다.
@receiver(post_delete, sender=Post)
def post_deleted(sender, instance, **kwargs):
    # 삭제된 인스턴스 정보를 파라미터로 하여 Kafka로 메시지를 전송합니다.
    producer_instance.send_post_delete(sender, instance, **kwargs)


