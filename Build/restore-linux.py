from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

root = Path(__file__).resolve().parent.parent
packages = [(p.attrib['id'], p.attrib['version']) for p in ET.parse(root / 'RBX Alt Manager/packages.config').getroot()]
packages += [('Microsoft.NETFramework.ReferenceAssemblies.net472', '1.0.3'), ('Interop.IWshRuntimeLibrary', '1.0.1'), ('System.Resources.Extensions', '4.7.1')]
cache = root / '.build-cache'
cache.mkdir(parents=True, exist_ok=True)

def restore(package):
    name, version = package
    dest = root / 'packages' / f'{name}.{version}'
    if (dest / '.restored').exists():
        return
    url = f'https://api.nuget.org/v3-flatcontainer/{name.lower()}/{version}/{name.lower()}.{version}.nupkg'
    archive = cache / f'{name}.{version}.nupkg'
    urllib.request.urlretrieve(url, archive)
    with zipfile.ZipFile(archive) as z:
        z.extractall(dest)
    (dest / '.restored').touch()
    print(f'Restored {name} {version}', flush=True)

with ThreadPoolExecutor(max_workers=6) as pool:
    list(pool.map(restore, packages))
