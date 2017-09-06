"""
Boxes, Units and Peers
Let's name the important elements that are relevant to solving a Sudoku.

The individual squares at the intersection of rows and columns will be called boxes.
These boxes will have labels 'A1', 'A2', ..., 'I9'.

The complete rows, columns, and 3x3 squares, will be called units.
Thus, each unit is a set of 9 boxes, and there are 27 units in total.

For each box (e.g 'A1'), its peers will be all other boxes that belong to a common unit
(namely, those that belong to the same row, column, or 3x3 square).
Each box has 20 peers.

"""
import logging

logger = logging.getLogger()
logger.setLevel('DEBUG')
logging.info('Load up utilities')


rows = 'ABCDEFGHI'
cols = '123456789'


def cross(rows: str, cols: str) -> list:
    """ Cross product of elements in A and elements in B. """
    return [row + col for row in rows for col in cols]


boxes = cross(rows, cols)
# List of all coordinates.
# ['A1', 'A2', ..., 'A9', 'B1', ..., 'B9', ..., 'I1', ..., 'I9']


row_units = [cross(r, cols) for r in rows]
# Element example:
# row_units[0] = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
# This is the top most row.


column_units = [cross(rows, c) for c in cols]
# Element example:
# column_units[0] = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
# This is the left most column.


square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
# Element example:
# square_units[0] = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
# This is the top left square.


diagonal_units = [
    [row + col for row, col in zip('ABCDEFGHI', '123456789')],
    [row + col for row, col in zip('ABCDEFGHI', '987654321')]
    ]



units = row_units + column_units + square_units # + diagonal_units
# List of unit constraints. In a typical Sudoku there should be 27.
# Each coordinate should appear in three units: row, column and square.


box_to_unit_peers = dict((b, [[p for p in u if b != p] for u in units if b in u]) for b in boxes)
# dict(str, list(str))
# unit_list per coordinate
# A1 element example:
# [['A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'],
# ['B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1'],
# ['A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]


box_to_all_peers = dict((b, set(sum(box_to_unit_peers[b], []))) for b in boxes)
# dict(str, set)
# other boxes that are peers across all units:
# {'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
# 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1'
# 'B2', 'B3', 'C2', 'C3'}


def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    return {k: '123456789' if v == '.' else v for k, v in zip(boxes, grid)}


def values_grid(values):
    return ''.join([values[box] if len(values[box]) == 1 else '.' for box in boxes])


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in cols))
        if r in 'CF':
            print(line)
    return


def boxes_with_value_len(values, value_len=1):
    """ Returns a list of boxes where the length of value"""
    return [box for box, value in values.items() if len(value) == value_len]


def solved_boxes(values):
    """ Returns a tuple of percentage of Sudoku solved, number of solved boxes, and solved boxes."""
    return boxes_with_value_len(values, value_len=1)


def unsolved_boxes(values):
    """ Returns a tuple of percentage of Sudoku solved, number of solved boxes, and solved boxes."""
    return [box for box, value in values.items() if len(value) > 1]


def invalid_boxes(values):
    """ Returns a list of invalid boxes. An invalid box is one with no available values. """
    list_invalid_boxes = boxes_with_value_len(values, value_len=0)
    if list_invalid_boxes:
        logger.warning('Invalid boxes found: {}'.format(list_invalid_boxes))
    return list_invalid_boxes


def solved_count(values):
    list_solved = solved_boxes(values)
    return len(list_solved)


def solved(values):
    return solved_count(values) == 81


def solve_status(values):
    n_solved = solved_count(values)
    pct_solved = '{:.0f}'.format(100 * n_solved / 81)
    return '{}% solved ({}/81).'.format(pct_solved, n_solved)


if __name__ == '__main__':
    import pprint
    pprint.pprint(box_to_all_peers['A1'])
