import os
import uuid

from django.db import models
from django.contrib.auth.models import User

# auto_now=True : 수정일자
# django model 이 save 될 때마다 현재날짜(date.today()) 로 갱신
# 주로 최종수정일자 field option 으로 주로 사용됨

# auto_now_add=True : 생성일자
# django model 이 최초 저장(insert) 시에만 현재날짜(date.today()) 를 적용함.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # 클래스가 추상클래스가 됨
    class Meta:
        abstract = True


class Content(BaseModel):
    # cascade= 특정모델이 연관되게 해줌, 모델 A, B에서 연관되어있는 부분의 모델이있을때,
    # 모델 B를 삭제하면 그 부분에 대한 A의 내용도 삭제
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default='')

    class Meta:
        # 생성일의 역순
        ordering = ['-created_at']
        #
        verbose_name_plural = "컨텐츠"


def image_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    # 16자리 고유한 아이디 생성(import uuid)
    return os.path.join(instance.UPLOAD_PATH, "%s.%s" % (uuid.uuid4(), ext))

# python -m pip install Pillow(이미지사용에 필요한 라이브러리)


class Image(BaseModel):
    UPLOAD_PATH = "user-upload"

    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_to)
    # 이미지파일 넘버링(순서)
    order = models.SmallIntegerField()

    class Meta:
        #
        unique_together = ['content', 'order']
        # - => 내림차순
        ordering = ['order']


class FollowRelation(BaseModel):
    # 글쓰기(1명이 여러개의 글을 쓰지만, 다른사람이 그 사람글을 수정 할 수 없다)
    follower = models.OneToOneField(User, on_delete=models.CASCADE)
    # 팔로우(x가 y,z를 팔로우할 수 있다)
    followee = models.ManyToManyField(User, related_name='followee')


# 다 끝났으면 makemigrations, migrate(DB sqlite에 저장)
