import sys

def generate_nusmv_model(n, m):
    # Begin model with parameterized ranges for x and y
    model = f"""
MODULE main
  VAR
    x : 0..{n};  -- Number of people on the right shore
    y : 0..{m};  -- Number of ghosts on the right shore
    boat : {{left, right}};

  DEFINE
    delta := next(x) - x + next(y) - y;

  TRANS
    -- Boat must carry 1 or 2 passengers at a time, valid moves only
    (boat = left & 1 <= delta & delta <= 2) |
    (boat = right & -2 <= delta & delta <= -1);

  ASSIGN
    init(x) := 0;
    init(y) := 0;
    init(boat) := left;

    next(boat) := case
      (boat = left) : right;
      (boat = right) : left;
    esac;

    -- Generate all valid next(x) cases
    next(x) := case
"""
    # Define transitions for next(x) based on the current value of x and the boat's location
    for curr_x in range(n + 1):
        model += f"      (boat = left) & (x = {curr_x}) : {curr_x}..{min(curr_x + 2, n)};\n"
        model += f"      (boat = right) & (x = {curr_x}) : {max(curr_x - 2, 0)}..{curr_x};\n"
    model += f"    esac;\n"

    # Generate all valid next(y) cases
    model += "    next(y) := case\n"
    for curr_y in range(m + 1):
        model += f"      (boat = left) & (y = {curr_y}) : {curr_y}..{min(curr_y + 2, m)};\n"
        model += f"      (boat = right) & (y = {curr_y}) : {max(curr_y - 2, 0)}..{curr_y};\n"
    model += f"    esac;\n"
    
    # Define the invariant for safety (people >= ghosts if people > 0)
    model += f"""
  INVAR
    ((x = 0) | (x >= y)) & (({n} - x = 0) | ({n} - x >= {m} - y));
    -- Either no people, or #people >= #ghosts

  CTLSPEC
    AG !((x = {n}) & (y = {m}));
"""
    print(model)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python river_gen.py <n> <m>")
        sys.exit(1)

    n = int(sys.argv[1])
    m = int(sys.argv[2])
    generate_nusmv_model(n, m)