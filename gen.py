#!/usr/bin/env python3

import sys
import re

CTYPESGEN_PATH = '/home/tomba/work/ctypesgen/'

INCLUDE_PATH = '/usr/include'

INCLUDES = (
    f'{INCLUDE_PATH}/drm/drm.h',
    f'{INCLUDE_PATH}/drm/drm_mode.h',
    f'{INCLUDE_PATH}/drm/drm_fourcc.h',
)

OUT = 'kms/uapi/kms.py'

CTYPESGEN_OPTS = (
    '--no-embed-preamble',
    '--no-macro-try-except',
    '--no-source-comments',
    '-D__volatile__=',
    '-D__signed__=',
    '-U__SIZEOF_INT128__',
)

sys.path.insert(0, CTYPESGEN_PATH)
from ctypesgen.__main__ import main  # pylint: disable=E,C # type: ignore  # noqa: E402

sys.argv = ['ctypesgen', *CTYPESGEN_OPTS, f'-I{INCLUDE_PATH}', f'-o{OUT}', *INCLUDES]

main()

def replace(filename, replaces):
    for r in replaces:
        pat = r[0]
        repl = r[1]

        with open(filename, encoding='utf-8') as f:
            content = f.read()

        content = re.sub(pat, repl, content, count=1, flags=re.MULTILINE)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

# Fix _IOC by using ord(type)

replace(OUT, [
        (re.escape('return ((((dir << _IOC_DIRSHIFT) | (type << _IOC_TYPESHIFT)) | (nr << _IOC_NRSHIFT)) | (size << _IOC_SIZESHIFT))'),
         'return ((((dir << _IOC_DIRSHIFT) | (ord(type) << _IOC_TYPESHIFT)) | (nr << _IOC_NRSHIFT)) | (size << _IOC_SIZESHIFT))'),
        ])

# Add pylint ignore comment

replace('kms/uapi/ctypes_preamble.py', [
        (r'^def POINTER\(obj\):$',
         'def POINTER(obj): # pylint: disable=function-redefined:')
        ])
