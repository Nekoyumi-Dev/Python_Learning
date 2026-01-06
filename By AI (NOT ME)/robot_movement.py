# Robot Movement Simulator
# Start at (0,0) facing north
# Commands: L (turn left then move 1), R (turn right then move 1), G (go forward 1), B (turn around then move 1)

from typing import List, Tuple, Set

def simulate_movement(commands: str):
    # Starting position and direction
    x, y = 0, 0
    # Directions: 0=North, 1=East, 2=South, 3=West
    direction = 0
    
    # Direction vectors
    directions = {
        0: (0, 1),    # North: (dx, dy)
        1: (1, 0),    # East
        2: (0, -1),   # South
        3: (-1, 0)    # West
    }
    
    direction_names = {
        0: "North",
        1: "East",
        2: "South",
        3: "West"
    }
    
    positions = [(x, y)]
    
    print(f"Start: ({x}, {y}) facing {direction_names[direction]}")
    print(f"\nExecuting commands: {commands}\n")
    
    for i, cmd in enumerate(commands, 1):
        if cmd == 'L':  # Turn left and go forward
            direction = (direction - 1) % 4
            dx, dy = directions[direction]
            x += dx
            y += dy
            positions.append((x, y))
            print(f"Step {i}: {cmd} - Turn left to {direction_names[direction]}, move forward to ({x}, {y})")
        elif cmd == 'R':  # Turn right and go forward
            direction = (direction + 1) % 4
            dx, dy = directions[direction]
            x += dx
            y += dy
            positions.append((x, y))
            print(f"Step {i}: {cmd} - Turn right to {direction_names[direction]}, move forward to ({x}, {y})")
        elif cmd == 'G':  # Go forward
            dx, dy = directions[direction]
            x += dx
            y += dy
            positions.append((x, y))
            print(f"Step {i}: {cmd} - Move forward to ({x}, {y})")
        elif cmd == 'B':  # Turn around and go forward
            direction = (direction + 2) % 4  # Turn 180 degrees
            dx, dy = directions[direction]
            x += dx
            y += dy
            positions.append((x, y))
            print(f"Step {i}: {cmd} - Turn around to {direction_names[direction]}, move forward to ({x}, {y})")
    
    print(f"\n{'='*50}")
    print(f"Final position: ({x}, {y})")
    print(f"Final direction: {direction_names[direction]}")
    print(f"Total positions visited: {len(positions)}")
    print(f"All positions: {positions}")
    
    # Draw the map
    print(f"\n{'='*50}")
    print("MAP:")
    print(f"{'='*50}\n")
    
    # Find boundaries
    all_x = [p[0] for p in positions]
    all_y = [p[1] for p in positions]
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)
    
    # Create map
    for row_y in range(max_y, min_y - 1, -1):
        line = ""
        for col_x in range(min_x, max_x + 1):
            if (col_x, row_y) == (0, 0):
                line += "S "  # Start
            elif (col_x, row_y) == positions[-1]:
                line += "E "  # End
            elif (col_x, row_y) in positions:
                line += "* "  # Path
            else:
                line += ". "
        print(f"{row_y:2d} | {line}")
    
    print("    +" + "-" * (2 * (max_x - min_x + 1)))
    print("    ", end="")
    for col_x in range(min_x, max_x + 1):
        print(f"{col_x%10} ", end="")
    print()
    
    return x, y, direction, positions

# ------------------------------
# Heart outline command generator
# ------------------------------
Dir = int  # 0=N,1=E,2=S,3=W

DIR_VECS = {
    0: (0, 1),
    1: (1, 0),
    2: (0, -1),
    3: (-1, 0),
}

LEFT = {0:3, 1:0, 2:1, 3:2}
RIGHT = {0:1, 1:2, 2:3, 3:0}
OPP = {0:2, 1:3, 2:0, 3:1}

def heart_mask(scale: int = 7) -> Set[Tuple[int,int]]:
    """
    Build a set of integer grid cells (x,y) inside a heart shape using the implicit
    equation (x^2 + y^2 - 1)^3 - x^2 y^3 <= 0, scaled to desired size.
    """
    inside = set()
    # Choose grid bounds proportional to scale
    r = int(1.6 * scale)
    for y in range(-r, r+1):
        for x in range(-r, r+1):
            X = x / float(scale)
            Y = y / float(scale)
            v = (X*X + Y*Y - 1)**3 - (X*X)*(Y**3)
            if v <= 0:
                inside.add((x, y))
    return inside

def border_from_mask(inside: Set[Tuple[int,int]]) -> Set[Tuple[int,int]]:
    border = set()
    for (x, y) in inside:
        for dx, dy in DIR_VECS.values():
            if (x+dx, y+dy) not in inside:
                border.add((x, y))
                break
    return border

def trace_perimeter(border: Set[Tuple[int,int]]) -> List[Tuple[int,int]]:
    """Trace a single 4-connected perimeter of the border using a right-hand rule."""
    if not border:
        return []
    # Start at the topmost, then leftmost point
    start = max(border, key=lambda p: (p[1], -p[0]))
    curr = start
    # Start heading East along the top edge
    d: Dir = 1
    path = [curr]
    seen_first = False
    # Safety bound
    for _ in range(len(border) * 10):
        # Prefer to keep the wall on the right (clockwise trace)
        for nd in (RIGHT[d], d, LEFT[d], OPP[d]):
            dx, dy = DIR_VECS[nd]
            nxt = (curr[0]+dx, curr[1]+dy)
            if nxt in border:
                curr = nxt
                d = nd
                path.append(curr)
                break
        if curr == start:
            if seen_first:
                break
            seen_first = True
    # Deduplicate consecutive duplicates
    dedup = [path[0]]
    for p in path[1:]:
        if p != dedup[-1]:
            dedup.append(p)
    # Remove closing duplicate
    if len(dedup) > 1 and dedup[0] == dedup[-1]:
        dedup.pop()
    return dedup

def path_to_commands(points: List[Tuple[int,int]]) -> str:
    if not points:
        return ""
    # Robot starts at (0,0) facing North. We need to move from (0,0) to points[0] first.
    cmds = []
    x, y = 0, 0
    d: Dir = 0  # North

    def step_towards(tx: int, ty: int):
        nonlocal x, y, d, cmds
        while (x, y) != (tx, ty):
            if x < tx:
                desired = 1
            elif x > tx:
                desired = 3
            elif y < ty:
                desired = 0
            else:
                desired = 2
            # Emit a move in desired direction using minimal turn semantics
            if desired == d:
                cmds.append('G')
            elif desired == LEFT[d]:
                cmds.append('L')
            elif desired == RIGHT[d]:
                cmds.append('R')
            else:
                cmds.append('B')
            # Apply move
            dx, dy = DIR_VECS[desired]
            x += dx
            y += dy
            d = desired

    # Move to first point
    step_towards(*points[0])
    # Traverse along perimeter
    for a, b in zip(points, points[1:]+points[:1]):
        tx, ty = b
        # b should be a 4-neighbor; step one cell
        step_towards(tx, ty)
    return ''.join(cmds)

def generate_heart_commands(scale: int = 7) -> str:
    inside = heart_mask(scale)
    border = border_from_mask(inside)
    perimeter = trace_perimeter(border)
    return path_to_commands(perimeter)


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Robot Movement Simulator")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-c", "--commands", type=str,
        help="Command string composed of letters L, R, G, B"
    )
    group.add_argument(
        "--heart", type=int, nargs="?", const=7, metavar="SCALE",
        help="Generate commands to trace a heart outline at given SCALE (default 7)"
    )
    parser.add_argument(
        "--print-commands", action="store_true",
        help="Print the command sequence before simulation"
    )

    args = parser.parse_args()

    if args.heart is not None:
        cmds = generate_heart_commands(args.heart)
    elif args.commands:
        cmds = args.commands.upper()
        allowed = set("LRGB")
        cmds = ''.join(ch for ch in cmds if ch in allowed)
        if not cmds:
            print("No valid commands after filtering. Use only L, R, G, B.")
            sys.exit(1)
    else:
        try:
            cmds = input("Enter commands (L/R/G/B), or leave empty to quit: ").strip().upper()
        except EOFError:
            cmds = ""
        allowed = set("LRGB")
        cmds = ''.join(ch for ch in cmds if ch in allowed)
        if not cmds:
            print("No commands entered. Exiting.")
            sys.exit(0)

    if args.print_commands:
        print(f"Commands: {cmds}")

    simulate_movement(cmds)
