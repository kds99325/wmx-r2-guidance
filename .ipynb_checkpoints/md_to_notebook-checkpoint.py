# md_to_notebook.py
import nbformat as nbf
import re

def convert_md_to_ipynb(md_path, ipynb_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 정규표현식으로 ```python ... ``` 코드 블록과 나머지 텍스트 분리
    pattern = re.compile(r'(```python\n.*?```)', re.DOTALL)
    chunks = pattern.split(content)

    nb = nbf.v4.new_notebook()
    cells = []

    for chunk in chunks:
        if not chunk.strip():
            continue
        
        # 코드 블록인 경우
        if chunk.startswith('```python'):
            # 앞뒤의 ```python 과 ``` 제거
            code_text = chunk.replace('```python\n', '').replace('\n```', '')
            cells.append(nbf.v4.new_code_cell(code_text.strip()))
        else:
            # 일반 마크다운 텍스트인 경우
            cells.append(nbf.v4.new_markdown_cell(chunk.strip()))

    nb['cells'] = cells

    with open(ipynb_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"변환 완료: {ipynb_path}")