#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-05-06


def extans(context, answer):
    answer_s = context.find(answer)
    answer_e = answer_s + len(answer)
    return answer_s, answer_e

if __name__ == "__main__":
    cont = """[IMG1] 걸그룹 애프터스쿨 리지가 7월 26일 오후 서울 광진구 광장동에 위치한 쉐라톤 워커힐 리버파크에서 열린 K-collection with Supermodel Vol.1 ‘Basket Poolside Party’에 참석해 멋진 무대를 선보이고 있다. 이 행사는 K-POP 콘서트와 슈퍼모델 패션쇼가 결합된 신개념 패션 축제인 ‘K컬렉션’의 일환으로 SBS 남녀 슈퍼모델들의 써머 패션쇼와 SBS MTV의 The SHOW의 여름 특집으로 K-POP 스타들의 화려한 공연으로 꾸며졌다. 장우영(2PM), 버벌진트, 애프터스쿨(정아, 주연, 유이, 레이나, 나나, 리지, 이영, 가은), 글램(미소, TRINITY, 박지연, 다희, ZINNI), 제국의아이들(문준영, 시완, 케빈, 황광희, 김태헌, 정희철, 하민우, 박형식, 김동준), 마이티마우스(상추, 쇼리J), 지나, 주석, B.A.P(방용국, 힘찬, 대현, 영재, 종업, 젤로), 써니힐(주비, 승아, 코타, 미성), 핸섬피플(테이, 영호, 엄주혁), 김형준, 크레용팝(엘린, 소율, 금미, 초아, 웨이), 몬스터즈(SIC, 원샷, 코모), 빅스타(필독, 바람, 래환, 주드, 성학), 헬로비너스(유아라, 앨리스, 나라, 윤조, 라임, 유영), 뉴이스트(JR, Aron, 백호, 민현, 렌), NS윤지, 일렉트로보이즈(마부스, 원카인, 차쿤), 타히티(지수, E.J, 정빈, 민재, 다솜, 예은), 배치기(무웅, 탁) 등이 참여해 재밌고 HOT한 써머 풀사이드 페스티벌을 선사했다. 또한 SK플래닛이 운영하는 쇼핑 포털 서비스 Basket(바스켓)과 함께 패션브랜드 톰앤래빗, Redopin(레드오핀), 설탕공장, Tisvin(티스빈)은 슈퍼모델과 함께하는 여름 비치 웨어 패션쇼를 공연 중 선보이며 K-POP스타의 화려한 무대는 물론 최신 패션 트렌드를 소개하는 무대도 선보였다. 한편 K-Collection with Supermodel Vol.1 ‘Basket Poolside Party’는 SBS MTV에서 오는 8월 3일, 8월 10일 밤 10시 1-2부로 나누어 방송된다. [연예부 송재원기자]"""
    ans = """걸그룹 애프터스쿨 리지"""
    print (extans(cont, ans))
