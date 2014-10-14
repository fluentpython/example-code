
"""
=============
Row tests
=============

    >>> row = Row([1, 2, 3, 4])
    >>> row[1]
    2
    >>> row[1:3]
    Row([2, 3])

=============
Table tests
=============

Create an empty table

    >>> t3x4 = Table.blank(3, 4)
    >>> t3x4
    Table(Row([None, None, None, None]),
          Row([None, None, None, None]),
          Row([None, None, None, None]))
    >>> for i in range(3):
    ...     for j in range(4):
    ...         t3x4[i][j] = chr(65 + i * 4 + j)
    ...
    >>> t3x4
    Table(Row(['A', 'B', 'C', 'D']),
          Row(['E', 'F', 'G', 'H']),
          Row(['I', 'J', 'K', 'L']))
    >>> t3x4[1]
    Row(['E', 'F', 'G', 'H'])
    >>> t3x4[1:]
    Table(Row(['E', 'F', 'G', 'H']),
          Row(['I', 'J', 'K', 'L']))

    >>> t3x4[1][2]
    'G'
    >>> t3x4[1, 2]
    'G'

Slicing returns a table, so index 2 below would be trying to get row index 2
of a table that has only rows 0 and 1:

    >>> t3x4[1:][2]
    Traceback (most recent call last):
      ...
    IndexError: no row at index 2 of 2-row table

    >>> t3x4[:, 2]
    Table(Row(['C']),
          Row(['G']),
          Row(['K']))

    >>> t3x4[1:, 2]
    Table(Row(['G']),
          Row(['K']))

    >>> t3x4[1, 2:]
    Row(['G', 'H'])

    >>> t3x4[:, 1:3]
    Table(Row(['B', 'C']),
          Row(['F', 'G']),
          Row(['J', 'K']))

    >>> t3x4[:, :]
    Table(Row(['A', 'B', 'C', 'D']),
          Row(['E', 'F', 'G', 'H']),
          Row(['I', 'J', 'K', 'L']))

    >>> t3x4[:, :] == t3x4
    True

===============
Error handling
===============

    >>> t3x4[5]
    Traceback (most recent call last):
      ...
    IndexError: no row at index 5 of 3-row table
    >>> t3x4[1,]
    Traceback (most recent call last):
      ...
    IndexError: index must be [i] or [i, j]
    >>> t3x4[1, 2, 3]
    Traceback (most recent call last):
      ...
    IndexError: index must be [i] or [i, j]
    >>> t3x4[10:, 2]
    Traceback (most recent call last):
      ...
    ValueError: Table must have at least one row.
    >>> t3x4[1, 20:]
    Traceback (most recent call last):
      ...
    ValueError: Row must have at least one cell.
"""

import collections


class Row(collections.UserList):

    def __init__(self, cells):
        super().__init__(cells)
        if len(self) < 1:
            raise ValueError('Row must have at least one cell.')

    def __getitem__(self, position):
        if isinstance(position, slice):
            return Row(self.data[position])  # build sub-row
        else:
            return self.data[position]  # return cell value

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.data)


class Table(collections.UserList):
    """A table with rows, all of the same width"""

    def __init__(self, rows):
        super().__init__(Row(r) for r in rows)
        if len(self) < 1:
            raise ValueError('Table must have at least one row.')
        self.width = self.check_width()

    def check_width(self):
        row_widths = {len(row) for row in self.data}
        if len(row_widths) > 1:
            raise ValueError('All rows must have equal length.')
        return row_widths.pop()

    @classmethod
    def blank(class_, rows, columns, filler=None):
        return class_([[filler] * columns for i in range(rows)])

    def __repr__(self):
        prefix = '%s(' % self.__class__.__name__
        indent = ' ' * len(prefix)
        rows = (',\n' + indent).join(
                repr(row) for row in self.data)
        return prefix + rows + ')'

    def _get_indexes(self, position):
        if isinstance(position, tuple):  # multiple indexes
            if len(position) == 2:  # two indexes: t[i, j]
                return position
            else:
                raise IndexError('index must be [i] or [i, j]')
        else:  # one index: t[i]
            return position, None

    def __getitem__(self, position):
        i, j = self._get_indexes(position)
        if isinstance(i, slice):
            if j is None:  # build sub-table w/ full rows
                return Table(self.data[position])
            else:  # build sub-table w/ sub-rows
                return Table(cells[j] for cells in self.data[i])
        else:  # i is number
            try:
                row = self.data[i]
            except IndexError:
                msg = 'no row at index %r of %d-row table'
                raise IndexError(msg % (position, len(self)))
            if j is None:  # return row at table[i]
                return row
            else:
                return row[j]  # return row[j] or row[a:b]
