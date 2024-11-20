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

from structures import ARG, CASE, HEADER, INIT_BODY, METHOD
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


class ArgData ():
    name:str
    description:list[str]
    type_:str
    tdlib_value:str|None
    nullable:bool
    
    def __init__(self):
        self.name = ''
        self.description = []
        self.type_ = ''
        self.nullable = False
        self.tdlib_value = None


class ConstructorData ():
    name:str
    description:list[str]
    args:dict[str,ArgData]
    
    def __init__(self):
        self.name = ''
        self.description = []
        self.args = {}


class ClassData ():
    name:str
    description:list[str]
    constructors:dict[str,ConstructorData]
    
    def __init__(self):
        self.name = ''
        self.description = []
        self.constructors = {}
        
        
class FuncData ():
    name:str
    constructor:ConstructorData
    return_type:str
    can_be_sync:bool
    
    def __init__(self):
        self.name = ''
        self.constructor = None
        self.return_type = ''
        self.can_be_sync = False


def format_args_const(args:list[ArgData]) -> list[str]:
    out:list[str] = []
    for arg in args:
        out.append(f'{arg.type_}{'?' if arg.nullable else ''} {arg.name}')

    return out

def format_args_desc(args:list[ArgData]) -> list[str]:
    out:list[str] = []
    for arg in args:
        out.append(f'@param {arg.name} {" ".join(arg.description)}')

    return out
    
def format_args_obj(args:list[ArgData]) -> list[str]:
    out:list[str] = []
    for arg in args:
        out.append(f'{arg.name}: {arg.name if not arg.tdlib_value else arg.tdlib_value}')

    return out

def pascal_to_kebeb(camel_string:str) -> str:
    builder = []
    for (i, char) in enumerate(camel_string):
        if char.isupper() and i != 0:
            builder.append("-")

        builder.append(char.lower())

    return ''.join(builder)

def camel_to_kebeb(camel_string:str) -> str:
    return pascal_to_kebeb(camel_to_pascal(camel_string))

def camel_to_snake(camel_string:str) -> str:
    builder = []
    for (i, char) in enumerate(camel_string):
        if char.isupper() and i != 0:
            builder.append("_")

        builder.append(char.lower())

    return ''.join(builder)

def snake_to_pascal(snake_string:str) -> str:
    return snake_string.replace('_', ' ').title().replace(' ', '')

def camel_to_pascal(camel_string:str) -> str:
    return camel_string[0].upper() + camel_string[1:]

def snake_to_kebab(snake_string:str) -> str:
    return snake_string.replace('_', '-')

def resolve_type (type_:str) -> str:
    if type_ in types_conversion:
        return types_conversion[type_]
    
    if type_.startswith('vector'):
        return f'Gee.ArrayList<{resolve_type(type_.replace('vector', '').strip('<>'))}?>'

    return camel_to_pascal(type_)


def escape_name(type_:str) -> str:
    if type_ == 'object_type' or type_ == 'id':
        return type_ + '_'

    return type_

def format_description(description:list[str], tab_c:int = 1) -> str:
    MAX_SIZE = 70
    
    new_desc:list[str] = []
    for line in description:
        new_desc_line = ''

        lines_splitted = line.split(' ')
        for line_splitted in lines_splitted:
            if len(new_desc_line) + len(line_splitted) <= MAX_SIZE:
                new_desc_line += line_splitted + ' '
            else:
                new_desc.append(new_desc_line.strip())
                new_desc_line = line_splitted + ' '

        new_desc.append(new_desc_line.strip())
    description = new_desc
    
    out = ['    ' * tab_c + '/**']

    for line in description:
        out.append('    ' * tab_c + f' * {line}')

    out.append('    ' * tab_c + ' */')

    return '\n'.join(out)

def format_cases(constructor_name:str, return_type:str) -> str:
    return CASE.format(
        return_type=return_type,
        case=constructor_name
    )

def format_method(return_type:str, name:str, argv:list[str], body:list[str], async_:bool, errors:list[str] = ['BadStatusCodeError']):
    arg = ',\n        '.join(argv)
    b = '\n        '.join(body)
    e = f'throws {', '.join(errors)} ' if len(errors) > 0 else ''

    return METHOD.format(
        type_='async ' if async_ else '',
        return_type=return_type,
        name=name + '_sync' if not async_ else name,
        argvn='\n        ' + arg + '\n    ' if len(argv) > 0 else '',
        body=body + '    ',
        errors=e
    )
    
def format_init_method():
    return METHOD.format(
        type_='',
        return_type='void',
        name='init',
        argvn='',
        body=INIT_BODY + '    ',
        errors=''
    )

def format_header () -> str:
    return HEADER.format(year=str(datetime.now().year), author=global_args.author)
