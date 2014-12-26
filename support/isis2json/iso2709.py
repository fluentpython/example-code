#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# ISO-2709 file reader
#
# Copyright (C) 2010 BIREME/PAHO/WHO
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 2.1 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from struct import unpack

CR =  '\x0D' # \r
LF =  '\x0A' # \n
IS1 = '\x1F' # ECMA-48 Unit Separator
IS2 = '\x1E' # ECMA-48 Record Separator / ISO-2709 field separator
IS3 = '\x1D' # ECMA-48 Group Separator / ISO-2709 record separator
LABEL_LEN = 24
LABEL_FORMAT = '5s c 4s c c 5s 3s c c c c'
TAG_LEN = 3
DEFAULT_ENCODING = 'ASCII'
SUBFIELD_DELIMITER = '^'

class IsoFile(object):

    def __init__(self, filename, encoding = DEFAULT_ENCODING):
        self.file = open(filename, 'rb')
        self.encoding = encoding

    def __iter__(self):
        return self

    def next(self):
        return IsoRecord(self)

    __next__ = next # Python 3 compatibility

    def read(self, size):
        ''' read and drop all CR and LF characters '''
        # TODO: this is inneficient but works, patches accepted!
        # NOTE: our fixtures include files which have no linebreaks,
        # files with CR-LF linebreaks and files with LF linebreaks
        chunks = []
        count = 0
        while count < size:
            chunk = self.file.read(size-count)
            if len(chunk) == 0:
                break
            chunk = chunk.replace(CR+LF,'')
            if CR in chunk:
                chunk = chunk.replace(CR,'')
            if LF in chunk:
                chunk = chunk.replace(LF,'')
            count += len(chunk)
            chunks.append(chunk)
        return ''.join(chunks)

    def close(self):
        self.file.close()

class IsoRecord(object):
    label_part_names = ('rec_len rec_status impl_codes indicator_len identifier_len'
                        ' base_addr user_defined'
                        # directory map:
                        ' fld_len_len start_len impl_len reserved').split()
    rec_len = 0

    def __init__(self, iso_file=None):
        self.iso_file = iso_file
        self.load_label()
        self.load_directory()
        self.load_fields()

    def __len__(self):
        return self.rec_len

    def load_label(self):
        label = self.iso_file.read(LABEL_LEN)
        if len(label) == 0:
            raise StopIteration
        elif len(label) != 24:
            raise ValueError('Invalid record label: "%s"' % label)
        parts = unpack(LABEL_FORMAT, label)
        for name, part in zip(self.label_part_names, parts):
            if name.endswith('_len') or name.endswith('_addr'):
                part = int(part)
            setattr(self, name, part)

    def show_label(self):
        for name in self.label_part_names:
            print('%15s : %r' % (name, getattr(self, name)))

    def load_directory(self):
        fmt_dir = '3s %ss %ss %ss' % (self.fld_len_len, self.start_len, self.impl_len)
        entry_len = TAG_LEN + self.fld_len_len + self.start_len + self.impl_len
        self.directory = []
        while True:
            char = self.iso_file.read(1)
            if char.isdigit():
                entry = char + self.iso_file.read(entry_len-1)
                entry = Field(* unpack(fmt_dir, entry))
                self.directory.append(entry)
            else:
                break

    def load_fields(self):
        for field in self.directory:
            if self.indicator_len > 0:
                field.indicator = self.iso_file.read(self.indicator_len)
            # XXX: lilacs30.iso has an identifier_len == 2,
            # but we need to ignore it to succesfully read the field contents
            # TODO: find out when to ignore the idenfier_len,
            # or fix the lilacs30.iso fixture
            #
            ##if self.identifier_len > 0: #
            ##    field.identifier = self.iso_file.read(self.identifier_len)
            value = self.iso_file.read(len(field))
            assert len(value) == len(field)
            field.value = value[:-1] # remove trailing field separator
        self.iso_file.read(1) # discard record separator

    def __iter__(self):
        return self

    def next(self):
        for field in self.directory:
            yield(field)

    __next__ = next # Python 3 compatibility

    def dump(self):
        for field in self.directory:
            print('%3s %r' % (field.tag, field.value))

class Field(object):

    def __init__(self, tag, len, start, impl):
        self.tag = tag
        self.len = int(len)
        self.start = int(start)
        self.impl = impl

    def show(self):
        for name in 'tag len start impl'.split():
            print('%15s : %r' % (name, getattr(self, name)))

    def __len__(self):
        return self.len

def test():
    import doctest
    doctest.testfile('iso2709_test.txt')


if __name__=='__main__':
    test()

