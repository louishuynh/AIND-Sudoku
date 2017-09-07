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

values (dict: key, value) represent all the boxes to their corresponding value.
value (str) are the potential values that can be assigned to a box. When it's length is 1, it is the correct value.

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


units = row_units + column_units + square_units + diagonal_units
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


logger = logging.getLogger(__name__)
logger.setLevel('INFO')
logging.info('Start Solving Sudoku')


assignments = []


def assign_value(values, box, value):
    """ Assigns a value to a given box. If it updates the board record it. """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        logger.info('{}={}. {}'.format(box, value, solve_status(values)))
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for box in unsolved_boxes(values):
        choices = values[box]
        if len(choices) > 2:
            continue
        for unit in box_to_unit_peers[box]:  # three unit types: row, column, box
            for peer in unit:
                if values[peer] != choices:
                    continue
                for non_twin_peer in unit:
                    if non_twin_peer == peer:
                        continue
                    for ntp_choice in values[non_twin_peer]:
                        if ntp_choice in choices:
                            logger.debug('Found naked twin in box: {}'.format(unit))
                            logger.debug('Box: {}({}), Peer: {}({})'.format(box, choices, peer, values[peer]))
                            logger.debug('Non Twin Peer: {}({})'.format(non_twin_peer, values[non_twin_peer]))
                            msg = 'Removing {} from Non Twin Peers from {} to {}'
                            old_v = values[non_twin_peer]
                            new_v = values[non_twin_peer].replace(ntp_choice, '')
                            logger.debug(msg.format(non_twin_peer, old_v, new_v))
                            values = assign_value(values, non_twin_peer, new_v)


    return values


def eliminate(values):
    """ Eliminate the value of each solved box from all of it's peers values. """
    for solved_box in solved_boxes(values):
        for peer in box_to_all_peers[solved_box]:
            values = assign_value(values, peer, values[peer].replace(values[solved_box], ''))
    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    """
    for box in unsolved_boxes(values):
        choices = values[box]
        found = False
        logger.debug('{}: {}'.format(box, choices))
        for unit in box_to_unit_peers[box]:  # three unit types: row, column, box
            other_choices = ''.join([values[peer] for peer in unit])
            for choice in choices:
                if choice not in other_choices:
                    logger.debug('Peer choices: {} ({})'.format(other_choices, ','.join(unit)))
                    values = assign_value(values, box, choice)
                    found = True
                    break
            if found:
                break
    return values


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the Sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A Sudoku in dictionary form.
    Output: The resulting Sudoku in dictionary form.
    """
    stalled = False
    solved_boxes_before = solved_boxes(values)
    logger.info('Starting Sudoku: {}'.format(solve_status(values)))
    for box in solved_boxes(values):
        logger.info('{}: {}'.format(box, values[box]))
    while not stalled:

        logger.info('========== Run eliminate algo. ==========')
        values = eliminate(values)
        if solved(values):
            logger.info('Sudoku complete.')
            break

        logger.info('========== Run only choice algo. ==========')
        values = only_choice(values)
        if solved(values):
            logger.info('Sudoku complete.')
            break

        logger.info('========== Run naked twins algo. ==========')
        values = naked_twins(values)
        solved_boxes_after = solved_boxes(values)
        if solved(values):
            logger.info('Sudoku complete.')
            break

        else:
            stalled = solved_boxes_before == solved_boxes_after
            if stalled:
                logger.info('Sudoku reducer stalled.')
            else:
                solved_boxes_before = solved_boxes_after
        if invalid_boxes(values):
            return False

    return values


def search(values, mystr=''):
    """ Using depth-first search and propagation, create a search tree and solve the sudoku."""

    unfilled = [(box, values[box], len(values[box])) for box in values if len(values[box]) > 1]
    if unfilled == []:
        return values

    unfilled = sorted(unfilled, key=lambda x: x[2])
    node, choices, _ = unfilled[0]
    for choice in choices:
        logger.debug('tried: {}, choices are {}'.format(mystr, unfilled[:3]))
        t = values.copy()
        t[node] = choice
        recursive_search = search(t, mystr='{}/{}={}'.format(mystr, node, choice))
        if recursive_search is not False:
            logger.debug('Found {} OK!'.format(mystr))
            return recursive_search
    return False


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    values = grid_values(grid)
    values = reduce_puzzle(values)
    if values is False:
        return False
    if not solved(values):
        logger.info('Apply search algorithm.')
        values = search(values)
    return values


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
