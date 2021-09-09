import sys

from flask import session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


# 멤버(회원관리)
class Member(db.Model):
    id = db.Column(db.String(30), primary_key=True)
    pwd = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)


class MemService:
    def join(self, m: Member):  # 회원가입
        db.session.add(m)
        db.session.commit()

    def login(self, id: str, pwd: str):  # 로그인
        mem = Member.query.get(id)
        if mem is not None:
            if pwd == mem.pwd:
                session['login_id'] = id
                session['flag'] = True
                return True

        return False

    def myInfo(self):  # 로그인한 id로 검색한 객체 반환
        id = session['login_id']
        return Member.query.get(id)

    def editMyInfo(self, name: str, pwd: str, email: str, mobile: str):  # 새 pwd 받아서 현재 로그인 중인 id로 검색하여 수정
        mem = self.myInfo()
        mem.name = name
        mem.pwd = pwd
        mem.email = email
        mem.mobile = mobile
        db.session.commit()

    def logout(self):  # session에서 id 삭제 및 flag = False로 변환
        session.pop('login_id')
        session['flag'] = False

    def out(self):  # 로그인한 id를 db에서 삭제. 로그아웃 처리.
        mem = self.myInfo()
        db.session.delete(mem)
        db.session.commit()
        self.logout()

    def findId(self, name: str, email: str):   # name, email 값 입력 후 아이디 반환
        # print('service', Member.query.filter(Member.email == email).all())    # <Member user01> 로 출력됨
        # return Member.query.filter(Member.email == email).all()
        user = Member.query.filter((Member.name == name)&(Member.email == email)).first()
        return user.id if hasattr(user, 'id') else None

    def checkCode(self, id: str, email: str):   # id, email값 입력 후 email 반환
        user = Member.query.filter((Member.id == id)&(Member.email == email)).first()
        return user.id if hasattr(user, 'id') else None

    def resetPwd(self, id: str, pwd: str):  # 새 pwd 받아서 현재 로그인 중인 id로 검색하여 수정
        mem = Member.query.get(id)
        print(mem)
        print('pwd:', pwd)
        print('mem.pwd:', mem.pwd)
        mem.pwd = pwd
        db.session.commit()

    def KakaoLogin(self, id: str):  # 카카오로그인 성공한 경우 session 값 입력
        session['login_id'] = id
        print('service', session['login_id'])
        session['flag'] = True
        return True

