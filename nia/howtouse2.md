cw18    cw18에 있는 모든 파일을 cw18.txt로 저장
cw18_dup    cw18에 있는 모든 파일을 길이 수 지정하고 중복 제거해서 저장
didi4   cw18_dup.py 로 만들어진 결과물을 json으로 저장. 만약 본문이 이전에 사용되 었다면질문이그 본문 밑으로 붙음..
kakatojson  didi4.py 응용
ratio_split 리스트의 내용물을 특정 비율로 자르는 법
ratio_split2    json 을 특정 비율로 자르는 법
count_answer    마커가 안 되어 있는 거 때문에 만듦. 본문 복제한 다음에 답이 본문에서 몇 번 나오는지 찾고1번 나오면 마커 칠하고 normal에 저장하고  아니면 error 에
count_answer2_old   count_answer.py 를 한 폴더에 대해 실행
count_answer2   count_answer응용
count_answer2_new   count_answer응용
count_answer3   count_answer2와 비슷
count_answer_sw count_answer을 이용해 질문, 육하원칙만 저장.
no_marker_ascending count_answer 의 결과물로 나온 두 파일을 오름차순으로 정렬해서 합침 (key=lambda x: int(x[2])
sum 크웍이 파일 별로 저장해준 데이터를 하나의 json 으로.
check_encoding  인코딩 확인
trim_output output의 길이 다시 하고, 중복제거함.
insert  db 에 본문을 user별로 넣음.
common_tsv  공통 tsv 양식으로 바꿔줌
common_json 공통 json 양식으로 바꿔줌(한 파일로 저장)
common_json_split   공통 json 양식으로 바꿔줌(각 파일로 저장)
read2   엑셀 따옴표 문제로 한 번 처리하기 위해 만든 파일2
read    엑셀 따옴표 문제로 한 번 처리하기 위해 만든 파일1
read3   엑셀 따옴표 문제로 한 번 처리하기 위해 만든 파일3
find_location   마커가 있는 답의 위치를 찾는 것
