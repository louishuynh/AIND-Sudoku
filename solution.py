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
stream_handler = logging.StreamHandler()  # Handler for the logger
logger.addHandler(stream_handler)
stream_handler.setFormatter(logging.Formatter('[%(levelname)s] %(funcName)s: %(message)s'))


class SudokuBoard():
    """
    A representation of (9 x 9) Soduku board and collection of board attributes.
    Attributes:
        rows = str. 'ABCDEFGHI'
        cols = str. '123456789'
        boxes = list[str]. List of all co-ordinates on board
            e.g. ['A1', ..., 'A9', 'B1', ..., 'I9']
        row_units = list[str]. List of all row units.
            e.g. row_units[0] = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
        column_units = list[str]. List of all column units.
            e.g. column_units[0] = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
        square_units = list[str]. List of all square units.
            e.g. square_units[0] = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
        diagonal_units = list[str]. List of all diagonal units.
            e.g. diagonal_units[0] = ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']
        units = list[str]. List of unit constraints. In a typical Sudoku there are 27 constraints
            Each coordinate should appear in three units: row, column and square.
        unit_peers_map = dict(str, list(str)). Dictionary of unit peers for each box.
            e.g. A1 element example:
            [['A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'],
            ['B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1'],
            ['A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
        all_peers_map = dict(str, set(str)). Dictionary of all peers for each box.
            e.g. A1 element example:
            {'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
            'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1'
            'B2', 'B3', 'C2', 'C3'}
    """

    def __init__(self):
        self.rows = 'ABCDEFGHI'
        self.cols = '123456789'
        self.boxes = self.cross(self.rows, self.cols)
        self.row_units = [self.cross(r, self.cols) for r in self.rows]
        self.column_units = [self.cross(self.rows, c) for c in self.cols]
        self.square_units = [self.cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
        self._diag_1 = [row + col for row, col in zip(self.rows, self.cols)]
        self._diag_2 = [row + col for row, col in zip(self.rows, self.cols[::-1])]
        self.diagonal_units = [self._diag_1, self._diag_2]
        self.units = self.row_units + self.column_units + self.square_units + self.diagonal_units
        self.unit_peers_map = dict((b, [[p for p in u if b != p] for u in self.units if b in u]) for b in self.boxes)
        self.all_peers_map = dict((b, set(sum(self.unit_peers_map[b], []))) for b in self.boxes)

    @staticmethod
    def cross(rows: str, cols: str) -> list:
        """ Cross product of elements in A and elements in B. """
        return [row + col for row in rows for col in cols]

    def unit_peers(self, box: str) -> list:
        """ Returns a list of unit peers for a given box. """
        return self.unit_peers_map[box]

    def all_peers(self, box: str) -> set:
        """ Returns a list of all peers for a given box. """
        return self.all_peers_map[box]


board = SudokuBoard()


def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    return {k: '123456789' if v == '.' else v for k, v in zip(board.boxes, grid)}


def values_grid(values: dict) -> str or bool:
    """ Convert values [dict(str, str)], a dictionary representation of Sudoku to a string representation."""
    if values is False:
        return values
    return ''.join([values[box] if len(values[box]) == 1 else '.' for box in board.boxes])


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in board.boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in board.rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in board.cols))
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
        return True
    complete = solved_count(values) == 81
    if complete is True and is_valid(values) is False:
        return False
    return False


def solved_count(values):
    """ Returns the number of solved boxes. """
    list_solved = solved_boxes(values)
    return len(list_solved)


def check_complete(values):
    """ Returns tuple of solved status and values if False."""
    if invalid_boxes(values):
        return False, False
    complete = solved_count(values) == 81
    if complete:
        if is_valid(values) is False:
            values = False
        if values is False:
            logger.info('Sudoku complete but not valid solution!')
        elif values is not False:
            logger.info('Sudoku complete and valid.')
    return complete, values


def solve_status(values):
    """ Returns a string containing the completion status of Sudoku for logging."""
    n_solved = solved_count(values)
    pct_solved = '{:.0f}'.format(100 * n_solved / 81)
    return '{}% solved ({}/81).'.format(pct_solved, n_solved)


def is_valid(values):
    """
    Checks to see if Sudoku is valid.
    Checks to see that each box contains the numbers 1 through to 9.
    :param values: dict(keys, values).
    :return: bool. True if valid. False if not.
    """
    """ Checks to see if a Sudoku"""
    evalues = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    for i, unit in enumerate(board.units):
        unit_check = sorted([values[box] for box in unit])
        # print('{}: {}'.format(i, unit_check))
        if (unit_check == evalues) is False:
            # print('Not valid unit {}. {}'.format(i, unit_check))
            return False
    return True


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
        for unit in board.unit_peers(box):  # three unit types: row, column, box
            for peer in unit:
                if values[peer] != choices:
                    continue
                msg1 = 'Found naked twin in boxes: {}({}) and {}({}) from unit: [{}]'
                msg2 = msg1.format(box, choices, peer, values[peer], ','.join(unit))
                for non_twin_peer in unit:
                    if non_twin_peer == peer:
                        continue
                    # logger.debug('Found Non Twin Peer: {}({})'.format(non_twin_peer, values[non_twin_peer]))
                    for ntp_choice in values[non_twin_peer]:
                        msg3 = '{} and Removing {} from Non Twin Peer from {} to {}.'
                        old_v = values[non_twin_peer]
                        if ntp_choice in choices:
                            new_v = values[non_twin_peer].replace(ntp_choice, '')
                            values = assign_value(values, non_twin_peer, new_v)
                            logger.debug(msg3.format(msg2, ntp_choice, non_twin_peer, old_v, new_v))
    return values


def eliminate(values):
    """ Eliminate the value of each solved box from all of it's peers values. """
    for solved_box in solved_boxes(values):
        for peer in board.all_peers(solved_box):
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
        # logger.debug('{}: {}'.format(box, choices))
        for unit in board.unit_peers(box):  # three unit types: row, column, box
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
    while not stalled:

        logger.debug('========== Run eliminate algo. ==========')
        values = eliminate(values)
        complete, values = check_complete(values)
        if complete or values is False:
            break

        logger.debug('========== Run only choice algo. ==========')
        values = only_choice(values)
        complete, values = check_complete(values)
        if complete or values is False:
            break

        logger.debug('========== Run naked twins algo. ==========')
        values = naked_twins(values)
        solved_boxes_after = solved_boxes(values)
        complete, values = check_complete(values)
        if complete or values is False:
            break

        else:
            stalled = solved_boxes_before == solved_boxes_after
            if stalled:
                logger.debug('Sudoku reducer stalled.')
            else:
                solved_boxes_before = solved_boxes_after
        if invalid_boxes(values):
            return False

    return values


def search(values, mystr='.'):
    """ Using depth-first search and propagation, create a search tree and solve the sudoku."""

    complete_status, values = check_complete(values)
    if complete_status:
        return values

    unfilled = [(box, values[box], len(values[box])) for box in values if len(values[box]) > 1]
    unfilled = sorted(unfilled, key=lambda x: x[2])

    node, choices, _ = unfilled[0]
    for choice in choices:
        t = values.copy()
        t[node] = choice
        logger.debug('Trying: {}={} assuming {} from options {}.'.format(node, choice, mystr, unfilled[:4]))
        t = reduce_puzzle(t)
        if t is False:
            continue
        recursive_search = search(t, mystr='{},{}={}'.format(mystr, node, choice))
        if recursive_search is not False:
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
    starting_sudoku = ','.join(['{}={}'.format(box, values[box]) for box in solved_boxes(values)])
    logger.info('Starting Sudoku: {} {}'.format(solve_status(values), starting_sudoku))
    values = reduce_puzzle(values)
    if values is False:
        logger.info('Sudoku has no valid solutions. Returning False.')
        return False
    logger.info('Checking if Sudoku is complete and solved.')
    complete, values = check_complete(values)
    logger.info('Sudoku complete status: {}. Values are: {}.'.format(complete, values))
    if complete is False or values is False:
        logger.info('===== ATTEMPTING TO SOLVE USING SEARCH ALGORITHM =====.')
        values = search(values)
        if values is False:
            logger.info('Unable to find valid solution. Returning False.')
            return values
        logger.info('Values={}'.format(values_grid(values)))
        for box in values:
            values = assign_value(values, box, values[box])
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
