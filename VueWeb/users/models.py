# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from sc_common.sc_choice import LEVEL_CHOICES


# 1. UserManager 설정
class UserManager(BaseUserManager):
    # 1) 일반 user 생성
    def create_user(self, user_id, password, email, hp, name, auth, **extra_fields):
        # (1) id check(value exist)
        if not user_id: raise ValueError('user_id Required!')

        # (2) user 객체 생성 및 저장
        user = self.model(user_id=user_id, email=email, hp=hp, name=name, auth=auth, **extra_fields)
        user.set_password(password)  # 암호를 암호화해서 password 필드에 저장함(save함수 미 호출)
        user.save(using=self._db)  # 디폴트 DB로 저장함
        return user

    # 2) superuser 생성
    def create_superuser(self, user_id, password, email=None, hp=None, name=None, auth=None):
        # (1) user 기본정보 설정
        user = self.create_user(user_id, password, email, hp, name, auth)

        # (2) superuser 권한 설정
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.level = 0
        user.save(using=self._db)
        return user


# 2. [User] model 설정
class User(AbstractBaseUser, PermissionsMixin):
    # 1) [User] model 관리객체 설정
    objects = UserManager()

    # 2) 사용자 필드 설정
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=17, verbose_name="아이디", unique=True)
    password = models.CharField(max_length=256, verbose_name="비밀번호")
    ##########################################################################################################
    email = models.EmailField(max_length=128, verbose_name="이메일", null=True, unique=True)  # 배포환경
    # email = models.EmailField(max_length=128, verbose_name="이메일",null=True, unique=False)     #개발환경(X)
    ##########################################################################################################
    hp = models.IntegerField(verbose_name="핸드폰번호", null=True, unique=True)
    name = models.CharField(max_length=8, verbose_name="이름", null=True)
    level = models.CharField(choices=LEVEL_CHOICES, max_length=18, verbose_name="등급", default='4')
    auth = models.CharField(max_length=10, verbose_name="인증번호", null=True)
    jdate = models.DateTimeField(auto_now_add=True, verbose_name='가입일', null=True, blank=True)

    # 3) 사용자 기본권한 설정
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # 4) 환경변수 설정 : cf) AUTH_USER_MODEL = "users.User" in [sc_web/settings.py]
    ##############################################################################################
    USERNAME_FIELD = 'user_id'  # designate [username] field of [User] model of Django
    REQUIRED_FIELDS = ['email']  # 필수입력 항목으로 설정
    ##############################################################################################

    def __str__(self):
        #return self.user_id
        return "%s(%s)" % (self.user_id, self.name)

    class Meta:
        db_table = "users_tbl"
        verbose_name = "사용자"
        verbose_name_plural = "사용자"


# 3. [User Login Log] model 설정
class UserLoginLog(models.Model):
    # 1) 필드 설정
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=17, verbose_name="ID", null=True, blank=True)
    user_name = models.CharField(max_length=8, verbose_name="이름", null=True, blank=True)
    user_ip = models.CharField(max_length=20, verbose_name="IP", null=True, blank=True)
    loginout = models.CharField(max_length=30, verbose_name="로그인아웃", null=True, blank=True)

    # 2) 모델 문자열 반환 메소드 설정
    def __str__(self):
        return "%s(%s) : %s" % (self.user_id, self.user_name, self.loginout)

    # 3) 메타정보 설정
    class Meta:
        db_table = 'userloginlog'
        verbose_name = '로그-인아웃'
        verbose_name_plural = '로그-인아웃'
