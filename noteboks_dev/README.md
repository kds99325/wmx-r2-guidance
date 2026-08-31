# Workspace for Notebooks (Experimentation / Debugging Space)

- The `notebooks` folder is the actual runtime environment, so its original
  files must be kept intact.
- To avoid corrupting the originals while trying out new features or
  debugging, changes are tested here first, and only verified code is moved
  into `notebooks`.

## Required Dependency Files

The notebooks in the `notebooks` folder require the following files to run:

- **`wmx_utils.py`**: Handles communication with WMX.
- **`wmx_motion_utils.py`**: Handles WMX motion control functionality.

Without these two files, the notebooks will not run properly.

If you also need these files while working in this folder, link them with symbolic links.

```bash
# Example symbolic links (stay in sync with the originals)
ln -s ../notebooks/wmx_utils.py wmx_utils.py
ln -s ../notebooks/wmx_motion_utils.py wmx_motion_utils.py
```

## Notes

- Changes made in this folder are not merged into `notebooks` until verified.
- If `wmx_utils.py` or `wmx_motion_utils.py` is being modified independently

# Korean

# Workspace for Notebooks (실험/디버깅 공간)

- `notebooks` 폴더는 실제 구동 환경이므로 원본을 그대로 유지해야 합니다.
- 새로운 기능을 시도하거나 디버깅하는 과정에서 원본이 손상되지 않도록,
  이 폴더에서 먼저 테스트한 뒤 검증된 코드만 `notebooks`로 옮깁니다.

## 필수 의존 파일

`notebooks` 폴더의 노트북을 구동하려면 아래 파일이 반드시 필요합니다:

- **`wmx_utils.py`**: WMX와 통신하는 역할을 하는 파일입니다.
- **`wmx_motion_utils.py`**: WMX의 모션 제어 관련 기능을 담당하는 파일입니다.

이 두 파일이 없으면 노트북이 정상적으로 구동되지 않습니다.
이 폴더에서 작업할 때에는 심볼릭 링크로 연결해서 사용하세요.

```bash
# 심볼릭 링크 예시 (원본과 항상 동기화됨)
ln -s ../notebooks/wmx_utils.py wmx_utils.py
ln -s ../notebooks/wmx_motion_utils.py wmx_motion_utils.py
```

## 주의사항

- 이 폴더에서 수정한 내용은 검증 전까지 `notebooks`에 반영하지 않습니다.