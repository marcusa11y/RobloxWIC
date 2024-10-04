import os as _0
import shutil as _1
import subprocess as _2
from zipfile import ZipFile as _3

def _4():
    if not _0.path.exists('Update.zip'):
        print('Update.zip not found.')
        return

    print("Extracting Update.zip...")
    try:
        with _3('Update.zip', 'r') as _5:
            _5.extractall()
            _6 = _5.filelist[0].filename.removesuffix('/')
    except Exception as _7:
        print(f"Failed to extract Update.zip: {_7}")
        return
    print("Moving files...")
    try:
        for _8 in _0.listdir(_6):
            _9 = _0.path.join(_0.getcwd(), _8)
            if _0.path.exists(_9):
                if _0.path.isdir(_9):
                    _1.rmtree(_9)
                else:
                    _0.remove(_9)
            _1.move(_0.path.join(_6, _8), _0.getcwd())
    except Exception as _A:
        print(f"Failed to move files: {_A}")
        return
    finally:
        print("Cleaning up...")
        _1.rmtree(_6)
        _0.remove('Update.zip')
        print("Update complete.")
        print("Restarting...")

if __name__ == '__main__':
    _4()