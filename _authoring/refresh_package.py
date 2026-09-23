"""Refresh integrity metadata after an authorized author-side repair."""
from pathlib import Path
import sys
import zipfile
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import practice as p
pack=p.read_json(ROOT/'pack-manifest.json')
index=p.read_json(ROOT/'_authoring/authoritative-manifest.json')
for assessment,slug in p.SLUGS.items():
    candidate=ROOT/'candidate'/slug
    base=ROOT/'_authoring'/slug
    manifest=p.read_json(base/'grader-manifest.json')
    manifest['protectedFiles']={name:p.digest(candidate/name) for name in manifest['protectedFiles']}
    manifest['trustedFiles']={name:p.digest(base/name) for name in manifest['trustedFiles']}
    p.validate_manifest(manifest)
    p.write_json(base/'grader-manifest.json',manifest)
    index['assessments'][assessment]['sha256']=p.digest(base/'grader-manifest.json')
    entry=pack['starterArchives'][assessment]
    entry['sourceHashes']={name:p.digest(candidate/name) for name in entry['sourceHashes']}
    with zipfile.ZipFile(ROOT/entry['path'],'w',zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(entry['sourceHashes']):
            info=zipfile.ZipInfo(name)
            info.create_system=3
            info.external_attr=(0o100755 if name=='mvnw' else 0o100644)<<16
            archive.writestr(info,(candidate/name).read_bytes(),compress_type=zipfile.ZIP_DEFLATED)
    entry['sha256']=p.digest(ROOT/entry['path'])
pack['status']='VERIFICATION_IN_PROGRESS'
p.write_json(ROOT/'pack-manifest.json',pack)
p.write_json(ROOT/'_authoring/authoritative-manifest.json',index)
print('Updated trusted/public hashes and executable starter archives.')
