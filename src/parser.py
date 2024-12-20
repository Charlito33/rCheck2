import json
import os
import re
import subprocess
import sys


def _is_function_in_dict(library_function_dict: dict[str | None, list[str]], function: str, library: str | None) \
        -> tuple[bool, list[str]]:
    regex_list = []
    for library_regex in library_function_dict:
        library_name = library
        if library_regex[1] is None:
            if library_name is None:
                for function_regex in library_function_dict[library_regex]:
                    if re.match(function_regex[1], function):
                        regex_list.append((library_regex[0], function_regex[0]))
            continue
        if library_name is None:
            library_name = ""
        if re.match(library_regex[1], library_name):
            for function_regex in library_function_dict[library_regex]:
                if re.match(function_regex[1], function):
                    regex_list.append((library_regex[0], function_regex[0]))
    return len(regex_list) > 0, regex_list

def _get_pretty_regex_str(regex_list: list[str]) -> str:
    output = ""
    prefix = ""
    for regex in regex_list:
        library_regex = regex[0]
        function_regex = regex[1]
        output += prefix
        prefix = ", "
        if library_regex is None:
            output += function_regex
        else:
            output += f"{library_regex}: {function_regex}"
    return output


class Rules:
    def __init__(self, file: str) -> None:
        self._file: str = file
        self._data: dict = None
        self._executables: list[str] = []
        self._banned_functions: dict = {}
        self._allowed_functions: dict = {}

    def parse(self) -> tuple[bool, str]:
        with open(self._file) as f:
            self._data = json.load(f)
        extended_regex = False
        if "config" in self._data:
            if type(self._data["config"]) is dict:
                if "extended_regex" in self._data["config"]:
                    if type(self._data["config"]["extended_regex"]) is bool:
                        extended_regex = self._data["config"]["extended_regex"]
                    else:
                        print("Warning: skipping extended regex configuration: wrong type.", file=sys.stderr)
                if "executables" in self._data["config"]:
                    if type(self._data["config"]["executables"]) is list:
                        self._executables = self._data["config"]["executables"]
                    else:
                        print("Warning: skipping custom executables configuration: wrong type.", file=sys.stderr)
            else:
                print("Warning: skipping configuration section: wrong type.", file=sys.stderr)
        if "rules" in self._data:
            if type(self._data["rules"]) is list:
                for entry in self._data["rules"]:
                    if type(entry) is not dict:
                        print("Warning: skipping rule entry: wrong type.", file=sys.stderr)
                        continue
                    library = None
                    library_regex = None
                    if "library" in entry:
                        if type(entry["library"]) is str:
                            library = entry["library"]
                            if extended_regex:
                                library_regex = library
                            else:
                                library_regex = f"^{library}$"
                        else:
                            print("Warning: skipping rule library entry: wrong type.", file=sys.stderr)
                            continue
                    if not library_regex in self._banned_functions:
                        self._banned_functions[(library, library_regex)] = []
                    if not library_regex in self._allowed_functions:
                        self._allowed_functions[(library, library_regex)] = []
                    if "ban" in entry:
                        if type(entry["ban"]) is not list:
                            print("Warning: skipping rule ban entry: wrong type.", file=sys.stderr)
                            continue
                        for ban in entry["ban"]:
                            if type(ban) is not str:
                                print("Warning: skipping entry in rule ban entry: wrong type.", file=sys.stderr)
                                continue
                            if len(ban) == 0:
                                print("Warning: skipping empty ban entry.", file=sys.stderr)
                                continue
                            if extended_regex:
                                ban_regex = ban
                            else:
                                ban_regex = f"^{ban}$"
                            self._banned_functions[(library, library_regex)].append((ban, ban_regex))
                    if "allow" in entry:
                        if type(entry["allow"]) is not list:
                            print("Warning: skipping rule allow entry: wrong type.", file=sys.stderr)
                            continue
                        for allow in entry["allow"]:
                            if type(allow) is not str:
                                print("Warning: skipping entry in rule allow entry: wrong type.", file=sys.stderr)
                                continue
                            if len(allow) == 0:
                                print("Warning: skipping empty allow entry.", file=sys.stderr)
                                continue
                            if extended_regex:
                                allow_regex = allow
                            else:
                                allow_regex = f"^{allow}$"
                            if (allow, allow_regex) in self._banned_functions[(library, library_regex)]:
                                if library_regex is None:
                                    print(f"Warning: skipping opposing entries, function "
                                          f"({allow}) is marked as banned.", file=sys.stderr)
                                else:
                                    print(f"Warning: skipping opposing entries, function "
                                          f"({library}: {allow}) is marked as banned.", file=sys.stderr)
                                continue
                            self._allowed_functions[(library, library_regex)].append((allow, allow_regex))
            else:
                print("Warning: skipping rules section: wrong type.", file=sys.stderr)
        return True, ""

    def is_banned(self, function_name: str, library_name: str | None) -> tuple[bool, str]:
        is_ban, ban_rules = _is_function_in_dict(self._banned_functions, function_name, library_name)
        if is_ban:
            is_allow, allow_rules = _is_function_in_dict(self._allowed_functions, function_name, library_name)
            if is_allow:
                return False, _get_pretty_regex_str(allow_rules)
            return True, _get_pretty_regex_str(ban_rules)
        return False, ""


def get_used_functions(file: str) -> tuple[bool, list[str, str], str]:
    functions = []

    if not os.path.exists(file):
        return False, [], "File not found"
    p = subprocess.Popen(["nm", file], stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if stdout is not None:
        stdout = stdout.decode()
    if stderr is not None:
        stderr = stderr.decode()
    status = p.wait()
    if status != 0:
        return False, [], ""
    for f in stdout.split("\n"):
        reg = re.search("^[0-9a-f]* *[A-Za-z]? ?([0-9A-Za-z_]+)(?:@(.*))?$", f)
        if reg is None:
            continue
        functions.append((reg.group(1), reg.group(2)))
    return True, functions, ""
