#!/usr/bin/python3
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

import requests
import sys
from object_defs import create_object
from utils import ArgData, ConstructorData, ClassData

import global_args


TAG_PREFIX = '@'
COMMENT_PREFIX = '//'
CLASS_TAG =  TAG_PREFIX + 'class'
DESCRIPTION_TAG = TAG_PREFIX + 'description'


# author = sys.argv[1]
# target_path = s1]
# target_path = sysys.argv[2]
author = 'Vladimir Vaskov'
target_path = '/home/rirusha/Downloads/doc'

td_api_url = 'https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/td_api.tl'
api_base = 'https://rdb.altlinux.org/api'
namespace = 'TDLib'

global_args.author = author
global_args.namespace = namespace
global_args.target_path = target_path

# td_api_doc_lines = requests.get(td_api_url).split('\n')




with open('/home/rirusha/Downloads/tdlib.tl', 'r') as f:
    td_api_doc_lines = f.readlines()
    
td_api_doc_lines_format:list[str] = []

for td_api_doc_line in td_api_doc_lines:
    if (td_api_doc_line and td_api_doc_line.strip() != ''):
        td_api_doc_lines_format.append(td_api_doc_line.strip())




classes_datas:dict[str,ClassData] = {}

for line in td_api_doc_lines_format:
    if '---functions---' in line:
        sys.exit(1)

    if line.startswith(COMMENT_PREFIX + CLASS_TAG):
        if class_data is None:
            class_data = ClassData ()

            class_data.descriprion = line.split(DESCRIPTION_TAG)[1].strip()
            class_data.name = line.split(DESCRIPTION_TAG)[0].strip().split(' ')[-1].strip()
            class_data.has_base_construct = False
        else:
            create_object(class_data)
            class_data = None
