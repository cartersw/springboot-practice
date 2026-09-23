"""Export fresh starters plus full grading support, without local build tools."""
from pathlib import Path
import datetime as dt
import shutil
import sys
import uuid
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
import practice

ROOT = Path(__file__).resolve().parents[1]

def export(root=ROOT):
    if sys.version_info < (3, 11):
        raise practice.PracticeError('INVALID_CONFIGURATION', 'Python 3.11+ required')
    manifest = practice.read_json(root / 'pack-manifest.json')
    validated = {}
    for assessment, slug in practice.SLUGS.items():
        grader, bundle = practice.load_manifest(assessment, root)
        archive = manifest['starterArchives'][assessment]
        practice.verify_files(root, {archive['path']: archive['sha256']})
        validated[assessment] = (grader, bundle, archive)
    name = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d-%H%M%S') + '-' + uuid.uuid4().hex[:8]
    container = root / 'transfer' / name
    if not practice.within(container, root):
        raise practice.PracticeError('INVALID_CONFIGURATION', 'Transfer directory escapes the pack')
    container.mkdir(parents=True, exist_ok=False)
    destination = container / 'spring-boot-practice'
    destination.mkdir()

    def copy(relative):
        source = root / relative
        if source.is_symlink() or not practice.within(source, root):
            raise practice.PracticeError('INVALID_CONFIGURATION', f'Unsafe source: {relative}')
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)

    for relative in ('START_HERE.md', 'START_HERE_MAC_LINUX.md', 'practice.code-workspace', 'pack-manifest.json',
                     'tools/practice.py', 'tools/test_practice_tool.py',
                     'tools/export_portable.py', '_authoring/authoritative-manifest.json'):
        copy(relative)
    if (root / 'VERIFICATION_REPORT.md').is_file():
        copy('VERIFICATION_REPORT.md')
    for assessment, slug in practice.SLUGS.items():
        grader, bundle, archive = validated[assessment]
        copy(archive['path'])
        candidate = destination / 'candidate' / slug
        practice.extract_archive(root / archive['path'], candidate)
        practice.verify_files(candidate, archive['sourceHashes'])
        copy('_authoring/' + slug + '/grader-manifest.json')
        for relative in grader['trustedFiles']:
            copy('_authoring/' + slug + '/' + relative)
    (destination / '.gitattributes').write_text(
        '* text=auto eol=lf\n*.cmd text eol=crlf\n*.zip -text\n/_authoring/** -text\n',
        encoding='utf-8', newline='\n')
    (destination / '.gitignore').write_text(
        '**/target/\n**/__pycache__/\n*.pyc\n/.runs/\n/reports/\n'
        '/attempts/**/*-final-verification-*/\n/attempts/**/verification with spaces/\n'
        '/transfer/\n/_authoring/toolchain/\n/_authoring/verification/\n'
        '/_authoring/git-backups/\n.DS_Store\nThumbs.db\n',
        encoding='utf-8', newline='\n')
    for folder in ('attempts', 'reports', '.runs'):
        (destination / folder).mkdir()
    for assessment, slug in practice.SLUGS.items():
        grader, _ = practice.load_manifest(assessment, destination)
        practice.verify_protected(destination / 'candidate' / slug, grader)
    archive_path = container / 'spring-boot-practice-portable.zip'
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(practice.safe_files(destination)):
            info = zipfile.ZipInfo.from_file(path, path.relative_to(container).as_posix())
            info.create_system = 3
            info.external_attr = (0o100755 if path.name == 'mvnw' else 0o100644) << 16
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED)
    receipt = {
        'createdAt': practice.utc(), 'folder': str(destination), 'zip': str(archive_path),
        'zipSha256': practice.digest(archive_path),
        'content': 'Fresh unsolved starters and trusted grading bundle; no saved attempts or solutions',
    }
    practice.write_json(container / 'export-receipt.json', receipt)
    print('Portable folder:', destination)
    print('Portable ZIP:', archive_path)
    print('ZIP SHA-256:', receipt['zipSha256'])
    print('This export starts fresh. Current candidate edits and saved attempts stay in the original pack.')
    return destination, archive_path

if __name__ == '__main__':
    try:
        export()
    except (practice.PracticeError, OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
        print(f'Export failed: {error}', file=sys.stderr)
        sys.exit(2)
