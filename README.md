# IT 기사 매거진

## 프로세스

1. <http://www.itworld.co.kr/main/>에서 기사 크롤링하여 서버에 저장
2. 각 기사별 키워드 추출하여 저장
3. 장고에서 api로 기사 제공



## 개선사항

- 기사 내용도 포함시켜서 서비스화 (핵심 요구사항이 검색 알고리즘이므로 우선순위 낮다고 생각했습니다.)
- 웹페이지에 서빙 (Vue 등 이용)



## Google 검색 알고리즘의 원리

1. 단어 분석
   - 철자 오류 해석
   - 문맥 파악
2. 검색어를 페이지와 맞추기
   - 페이지에서 검색어의 중요도 파악
3. 유용한 페이지 순위 매기기
   - 최신성
   - 검색어 등장 빈도
   - 같은 검색어로 검색한 유저의 방문 빈도
   - 유해 사이트 필터링
4. 최상의 결과를 제공
   - 검색 결과가 다양한 주제로 유저에게 다양한 정보를 제공
5. 문맥 고려하기
   - 위치, 이전 검색 기록 등을 활용하여 사용자에게 연관있는 검색결과 제공
