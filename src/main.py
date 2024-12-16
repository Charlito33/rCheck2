import os
import sys
import parser
from colors import Color

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(f"{Color.RED}Usage: rcheck2 <program path> (rules path){Color.RESET}", file=sys.stderr)
        exit(1)
    program_path = sys.argv[1]
    rules_path = "rcheck.json"
    if len(sys.argv) == 3:
        rules_path = sys.argv[2]
    if not os.path.exists(rules_path):
        print(f"{Color.RED}{rules_path}: File not found.{Color.RESET}", file=sys.stderr)
        exit(1)
    rules = parser.Rules(rules_path)
    success, error_message = rules.parse()
    if not success:
        print(error_message, file=sys.stderr)
        exit(1)
    success, used_functions, error_message = parser.get_used_functions(program_path)
    if not success:
        print(f"{Color.RED}{program_path}: {error_message}{Color.RESET}", file=sys.stderr)
        exit(1)
    banned_functions_count = 0
    for function in used_functions:
        function_name = function[0]
        library_name = function[1]
        is_banned, error_message = rules.is_banned(function_name, library_name)
        if is_banned:
            banned_functions_count += 1
            if library_name is None:
                print(f"{Color.RED}=> {function_name}, rule(s): {error_message}{Color.RESET}")
            else:
                print(f"{Color.RED}=> {function_name} from {library_name}, rule(s): {error_message}{Color.RESET}")
    if banned_functions_count == 0:
        print(f"\n{Color.GREEN}Found 0 banned function.{Color.RESET}")
    else:
        print(f"\n{Color.RED}Found {banned_functions_count} banned function(s).{Color.RESET}")
