# Workspace for Notebooks (Experimentation / Debugging Space)

This folder is a separate workspace created to **preserve the original files**
in the `notebooks` folder. When building new notebooks or modifying existing
logic, experiment and debug freely here, and only merge verified changes back
into the `notebooks` folder.


## Why the Folders Are Separated

- The `notebooks` folder is the actual runtime environment, so its original
  files must be kept intact.
- To avoid corrupting the originals while trying out new features or
  debugging, changes are tested here first, and only verified code is moved
  into `notebooks`.

## Required Dependency File

The notebooks in the `notebooks` folder require the following file to run:

- **`utils.py`**: Handles communication with WMX. Without this file, the
  notebooks will not run properly.

If you also need `utils.py` while working in this folder, copy it from
`notebooks/utils.py` or link it with a symbolic link.

```bash
# Example symbolic link (stays in sync with the original)
ln -s ../notebooks/utils.py utils.py
```

## Notes

- Changes made in this folder are not merged into `notebooks` until verified.
- If `utils.py` is being modified independently in this folder, it may
  diverge from the original in `notebooks` — always check the diff before
  merging.

---

# Workspace for Notebooks (실험/디버깅 공간)

이 폴더는 `notebooks` 폴더의 **원본을 보존**하기 위해 만든 별도의 작업 공간입니다.
노트북을 새로 만들거나 기존 로직을 수정할 때, 여기서 자유롭게 테스트하고 디버깅한 뒤
검증이 끝난 내용만 `notebooks` 폴더에 반영합니다.

## 왜 폴더를 분리했나

- `notebooks` 폴더는 실제 구동 환경이므로 원본을 그대로 유지해야 합니다.
- 새로운 기능을 시도하거나 디버깅하는 과정에서 원본이 손상되지 않도록,
  이 폴더에서 먼저 테스트한 뒤 검증된 코드만 `notebooks`로 옮깁니다.

## 필수 의존 파일

`notebooks` 폴더의 노트북을 구동하려면 아래 파일이 반드시 필요합니다:

- **`utils.py`**: WMX와 통신하는 역할을 하는 파일입니다. 이 파일이 없으면 노트북이 정상적으로 구동되지 않습니다.

이 폴더에서 작업할 때도 동일한 `utils.py`가 필요하다면,
`notebooks/utils.py`를 복사하거나 심볼릭 링크로 연결해서 사용하세요.

```bash
# 심볼릭 링크 예시 (원본과 항상 동기화됨)
ln -s ../notebooks/utils.py utils.py
```

## 주의사항

- 이 폴더에서 수정한 내용은 검증 전까지 `notebooks`에 반영하지 않습니다.
- `utils.py`를 이 폴더에서 독립적으로 수정 중이라면, `notebooks`의 원본과
  다를 수 있으니 병합 시 반드시 diff를 확인하세요.