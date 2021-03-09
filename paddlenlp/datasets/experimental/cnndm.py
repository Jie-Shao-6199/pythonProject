# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import collections
import os
import warnings

from paddle.io import Dataset
from paddle.dataset.common import md5file
from paddle.utils.download import get_path_from_url
from paddlenlp.utils.env import DATA_HOME
from . import DatasetBuilder

__all__ = ['CnnDm']


class CnnDm(DatasetBuilder):
    URL = "https://ernie-github.cdn.bcebos.com/data-cnndm.tar.gz"
    MD5 = None
    META_INFO = collections.namedtuple('META_INFO', ('file', 'md5'))
    SPLITS = {
        'train': META_INFO(
            os.path.join('cnndm', 'train', '1'),
            '8b10ed0ae31e71e8cd9105a6978d8970'),
        'dev': META_INFO(
            os.path.join('cnndm', 'dev', '1'),
            '7cb22f9cac04a285790a91cebba75260')
    }

    def _get_data(self, mode, **kwargs):
        default_root = os.path.join(DATA_HOME, self.__class__.__name__)
        filename, data_hash = self.SPLITS[mode]
        fullname = os.path.join(default_root, filename)
        if not os.path.exists(fullname) or (data_hash and
                                            not md5file(fullname) == data_hash):

            get_path_from_url(self.URL, default_root, self.MD5)

        return fullname

    def _read(self, filename, *args):
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line_stripped = line.strip().split('\t')
                if not line_stripped:
                    break
                else:
                    tokens = line_stripped[1]
                    labels = line_stripped[2]
                yield {"tokens": tokens, "labels": labels}