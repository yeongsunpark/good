<코드 설명>

ys_logger.py 파일은 로그를 위한 파일

work_sql.py는 83 번 DB 서버에서 데이터를 가져와서 텍스트 파일로 만드는 코드.

work_sql_ut.py 는 work_sql.py 에 사용하는 도구들. insert_str 과 regu 가 있음.

rm_dupli.py 는 a 파일과 b 파일을 비교하여서 특정 부분이 같으면 x 파일에, 다르면 y 파일에 저장하는 코드. (초기 연습용)

check_dupli.py 는 a 파일과 b 파일을 비교해서 특정 부분이 같으면 x 파일에, 다르면 y 파일에 저장하는 코드. 이거 사용함.

rm_dupli_rows.py 는 엑셀의 중복 제거 같은 기능. 나중에 멀티프로세서 써서 속도 높일 예정.

count_category 는 카테고리 가져와서 세는 파일. q_id 가 "1_c3_ent_01-1" 이런 식으로 되어 있을 때 중간 ent 만 꺼내서 셈.

save_as_category.py 는 카테고리 별로 txt 파일 저장해주는 코드.

final_tsv.py 는 카테고리 별로 된 txt 파일을 조금 수정해 주는 코드. q_id 를 없애고 1부터 차례로 채워줌.

<사용 안 하는 코드>

squad2tsv.py json 파일을 tsv 로 바꿔주는 코드. <- 이 코드 사용 안 하고 서버에서 바로 꺼내오기로 수정됨.

answer_extract.py 정답 위치 찾으려고 이거 만들었는데 이렇게 하면 마커 제대로 적용 못해서 안 씀. DB 시작 위치 끝 위치를 사용해서 찾는 걸로 바꿈.

