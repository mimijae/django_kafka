from rest_framework import status  # HTTP 상태 코드를 관리하는 status 모듈을 가져옵니다.
from rest_framework.decorators import api_view  # 뷰에 적용할 수 있는 api_view 데코레이터를 가져옵니다.
from rest_framework.response import Response  # 응답을 생성하는데 사용되는 Response 클래스를 가져옵니다.
from .models import Post  # 현재 디렉토리에 있는 models.py 파일에서 Post 모델을 가져옵니다.
from .serializers import PostSerializer  # 현재 디렉토리에 있는 serializers.py 파일에서 PostSerializer를 가져옵니다.
import logging  # 로깅 기능을 제공하는 logging 모듈을 가져옵니다.

logger = logging.getLogger(__name__)  # 로거 인스턴스를 생성합니다. 로그 메시지를 출력하는데 사용됩니다.

@api_view(['POST'])  # 이 뷰가 POST 요청만 처리하도록 지정합니다.
def create_post(request):  # 새로운 게시물을 생성하는 뷰 함수를 정의합니다.
    serializer = PostSerializer(data=request.data)  # 요청 데이터를 PostSerializer로 직렬화합니다.

    if serializer.is_valid():  # 직렬화된 데이터가 유효하면
        serializer.save()  # 직렬화된 데이터를 데이터베이스에 저장합니다.

        logger.info(f"Creating post: {request.data}")  # 로그 메시지를 출력합니다.

        return Response(serializer.data, status=status.HTTP_201_CREATED)  # 요청이 성공적으로 처리되었음을 나타내는 HTTP 201 상태 코드와 함께 응답을 반환합니다.

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 요청이 잘못되었음을 나타내는 HTTP 400 상태 코드와 함께 에러 메시지를 반환합니다.

@api_view(['PUT'])  # 이 뷰가 PUT 요청만 처리하도록 지정합니다.
def update_post(request, post_id):  # 게시물을 업데이트하는 뷰 함수를 정의합니다.
    try:
        post = Post.objects.get(id=post_id)  # 게시물을 찾습니다.
    except Post.DoesNotExist:  # 해당 게시물이 존재하지 않으면
        return Response(status=status.HTTP_404_NOT_FOUND)  # 요청된 리소스를 찾을 수 없음을 나타내는 HTTP 404 상태 코드를 반환합니다.

    serializer = PostSerializer(post, data=request.data)  # 요청 데이터를 PostSerializer로 직렬화합니다.

    if serializer.is_valid():  # 직렬화된 데이터가 유효하면
        serializer.save()  # 직렬화된 데이터를 데이터베이스에 저장합니다.

        logger.info(f"Updating post: {request.data}")  # 로그 메시지를 출력합니다.

        return Response(serializer.data)  # 요청이 성공적으로 처리되었음을 나타내는 HTTP 200 상태 코드와 함께 응답을 반환합니다.

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 요청이 잘못되었음을 나타내는 HTTP 400 상태 코드와 함께 에러 메시지를 반환합니다.

@api_view(['DELETE'])  # 이 뷰가 DELETE 요청만 처리하도록 지정합니다.
def delete_post(request, post_id):  # 게시물을 삭제하는 뷰 함수를 정의합니다.
    try:
        post = Post.objects.get(id=post_id)  # 게시물을 찾습니다.
    except Post.DoesNotExist:  # 해당 게시물이 존재하지 않으면
        return Response(status=status.HTTP_404_NOT_FOUND)  # 요청된 리소스를 찾을 수 없음을 나타내는 HTTP 404 상태 코드를 반환합니다.

    post.delete()  # 게시물을 삭제합니다.

    logger.info(f"Deleting post: {post_id}")  # 로그 메시지를 출력합니다.

    return Response(status=status.HTTP_204_NO_CONTENT)  # 요청이 성공적으로 처리되었지만 응답 본문에 보낼 추가적인 정보가 없음을 나타내는 HTTP 204 상태 코드를 반환합니다.
