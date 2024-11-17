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

import global_args


author = sys.argv[1]
target_path = sys.argv[2]

td_api_url = 'https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/td_api.tl'
api_base = 'https://rdb.altlinux.org/api'
namespace = 'TDLib'

global_args.author = author
global_args.namespace = namespace
global_args.target_path = target_path

td_api_doc = requests.get(td_api_url).text
