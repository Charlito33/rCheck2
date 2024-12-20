import os
import sys
import parser
from colors import Color

def parse_executable(rules: parser.Rules, used_functions: list[str]) -> None:
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

def main(auto_mode: bool = False) -> None:
    if auto_mode == False:
        program_path = sys.argv[1]
    else:
        program_path = None
    if auto_mode == False and len(sys.argv) == 3:
        rules_path = sys.argv[2]
    else:
        rules_path = ".rcheck/ruleset.json"

    if not os.path.exists(rules_path):
        print(f"{Color.RED}{rules_path}: File not found.\nAborting.{Color.RESET}", file=sys.stderr)
        exit(1)
    rules = parser.Rules(rules_path)
    success, error_message = rules.parse()
    if not success:
        print(error_message, file=sys.stderr)
        exit(1)

    if auto_mode == True:
        print("Executing multiple file scan from configuration file.")
        i: int = 1
        for executable in rules._executables:
            print("")
            print(f"Scanning [{i}] '{Color.YELLOW}{executable}{Color.RESET}'")
            success, used_functions, error_message = parser.get_used_functions(executable)
            if not success:
                print(f"{Color.RED}{executable}: {error_message}{Color.RESET}\n"
                      f"{Color.YELLOW}Ignoring file.{Color.RESET}", file=sys.stderr)
            else:
                parse_executable(rules, used_functions)
            i += 1
    else:
        print("Executing simple file scan from command line.")
        success, used_functions, error_message = parser.get_used_functions(program_path)
        if not success:
            print(f"{Color.RED}{program_path}: {error_message}{Color.RESET}", file=sys.stderr)
            exit(1)
        parse_executable(rules, used_functions)
    exit(0)

if __name__ == "__main__":
    if len(sys.argv) == 1 and os.path.exists(".rcheck/ruleset.json") == False:
        print(f"{Color.RED}Usage: rcheck2 <program path> (rules path){Color.RESET}", file=sys.stderr)
        print(f"{Color.YELLOW}Note: To use rcheck2 without arguments (automatic mode), you need a '.rcheck' "
                f"folder with a correct 'ruleset.json' file {Color.RESET}", file=sys.stderr)
        exit(1)
    if len(sys.argv) == 1 and os.path.exists(".rcheck/ruleset.json") == True:
        main(auto_mode=True)
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(f"{Color.RED}Usage: rcheck2 <program path> (rules path){Color.RESET}", file=sys.stderr)
        exit(1)
    main()
