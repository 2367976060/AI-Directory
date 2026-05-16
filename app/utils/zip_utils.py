import zipfile
from pathlib import Path


def create_zip(source_dir, output_path, exclude_dirs=None):
    if exclude_dirs is None:
        exclude_dirs = {'__pycache__', '.git', 'node_modules'}

    source_dir = Path(source_dir)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in source_dir.rglob('*'):
            if file_path.is_file():
                should_exclude = False
                for part in file_path.relative_to(source_dir).parts:
                    if part in exclude_dirs:
                        should_exclude = True
                        break
                if should_exclude:
                    continue
                arcname = file_path.relative_to(source_dir)
                zf.write(file_path, arcname)

    return output_path
