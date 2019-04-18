import glob
import re
import zlib

directory = '/home/txtsd/.local/share/Steam/steamapps/common/IdleChampions/IdleDragons_Data/StreamingAssets/downloaded_files/'

filelist = glob.glob(directory + '*')

for file in filelist:
    filename_segments = file.split('.')
    if (not 'json' in filename_segments) and (not 'txt' in filename_segments):
        with open(file, 'rb') as f:
            print('opened', file)
            loaded_file = f.read()
        res = re.search(b'(\\x89\\x50\\x4e\\x47\\x0d\\x0a\\x1a\\x0a.*)', loaded_file, re.MULTILINE|re.DOTALL)
        if res is not None:
            with open(file + '.png', 'wb') as g:
                g.write(res.group())
        else:
            data = zlib.decompress(loaded_file)
            res = re.search(b'(\\x89\\x50\\x4e\\x47\\x0d\\x0a\\x1a\\x0a.*)', data, re.MULTILINE|re.DOTALL)
            with open(file + '.png', 'wb') as g:
                g.write(res.group())
