"""
values (dict: key, value) represent all the boxes to their corresponding value.
value (str) are the potential values that can be assigned to a box. When it's length is 1, it is the correct value.

"""
import logging
from utils import *

logger = logging.getLogger()
logger.setLevel('DEBUG')
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
    return values


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
    for box, choices in unsolved_boxes(values):
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
    values = {'I6': '4', 'H9': '3', 'I2': '6', 'E8': '1', 'H3': '5', 'H7': '8', 'I7': '1', 'I4': '8',
              'H5': '6', 'F9': '7', 'G7': '6', 'G6': '3', 'G5': '2', 'E1': '8', 'G3': '1', 'G2': '8',
              'G1': '7', 'I1': '23', 'C8': '5', 'I3': '23', 'E5': '347', 'I5': '5', 'C9': '1', 'G9': '5',
              'G8': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9', 'A4': '2357', 'A7': '27',
              'A6': '257', 'C3': '8', 'C2': '237', 'C1': '23', 'E6': '579', 'C7': '9', 'C6': '6',
              'C5': '37', 'C4': '4', 'I9': '9', 'D8': '8', 'I8': '7', 'E4': '6', 'D9': '6', 'H8': '2',
              'F6': '125', 'A9': '8', 'G4': '9', 'A8': '6', 'E7': '345', 'E3': '379', 'F1': '6',
              'F2': '4', 'F3': '23', 'F4': '1235', 'F5': '8', 'E2': '37', 'F7': '35', 'F8': '9',
              'D2': '1', 'H1': '4', 'H6': '17', 'H2': '9', 'H4': '17', 'D3': '2379', 'B4': '27',
              'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6', 'D6': '279',
              'D7': '34', 'D4': '237', 'D5': '347', 'B8': '3', 'B9': '4', 'D1': '5'}
    values = reduce_puzzle(values)
    values = naked_twins(values)
    if values is False:
        return False
    if not solved(values):
        logger.info('Apply search algorithm.')
        values = search(values)
    return values


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    # try:
    #     from visualize import visualize_assignments
    #     visualize_assignments(assignments)
    #
    # except SystemExit:
    #     pass
    # except:
    #     print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
