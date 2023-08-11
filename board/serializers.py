from rest_framework import serializers  # 장고 REST 프레임워크에서 제공하는 serializers 모듈을 가져옵니다.
from .models import Post  # 현재 디렉토리에 있는 models.py 파일에서 Post 모델을 가져옵니다.

class PostSerializer(serializers.ModelSerializer):  # serializers.ModelSerializer를 상속받아 PostSerializer 클래스를 정의합니다.
    class Meta:  # Serializer의 메타 데이터를 정의하는 클래스입니다.
        model = Post  # 이 Serializer가 사용할 모델을 지정합니다. 여기서는 Post 모델을 사용합니다.
        fields = ['id', 'title', 'content']  # Serializer가 처리할 필드들을 지정합니다. Post 모델의 'id', 'title', 'content' 필드를 사용합니다.
