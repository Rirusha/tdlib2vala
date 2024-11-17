# Copyright (C) 2024 Vladimir Vaskov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from datetime import datetime

from structures import ARG, HEADER, METHOD, DEPRICATED
import global_args

types_conversion = {
    'double': 'double',
    'string': 'string',
    'int32': 'int32',
    'int53': 'int64',
    'int64': 'int64',
    'bytes': 'Bytes',
    'Bool': 'bool',
}


class Obj ():
    class_descriprion:str
    type_:str
    


def pascal_to_kebeb(camel_string:str) -> str:
    builder = []
    for (i, char) in enumerate(camel_string):
        if char.isupper() and i != 0:
            builder.append("-")

        builder.append(char.lower())

    return ''.join(builder)

def format_description(description:list[str]|str) -> str:
    out = ['    /**']

    if type(description) is str:
        out.append(f'     * {description}')
    elif type(description) is list:
        for line in description:
            out.append(f'     * {line}')
    else:
        raise TypeError()

    out.append('     */')

    return '\n'.join(out)

def format_method(return_type:str, name:str, argv:list[str], body:list[str], async_:bool, depricated_version:str|None):
    return METHOD.format(
        type_='async ' if async_ else '',
        return_type=return_type,
        name=name,
        argvn=',\n        '.join(argv),
        body='\n        '.join(body)
    )

def format_header () -> str:
    return HEADER.format(year=str(datetime.now().year), author=global_args.author)
