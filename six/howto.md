19.6에서 쓰던 코드를 그대로 가져옴.

1. ys_xml.py 파일로 뉴스들을 파싱한다.(노컷 뉴스 기준)

2. ys.py 파일로 벌크로 실행한다. 

3. merge_json 파일로 낱개로 되어 있는 폴더를 하나로 통합한다. 

4. cont_json 파일로 카테고리 별 개수를 센다.

5. split_json 파일로 카테고리 별로 개수를 맞춰 저장한다. IT/과학은 개수가 너무 적어서 다 넣어주었음.