from settings import *
import commands
import page

class Parse:
    def __init__(self, inpt):
        Verbose("VERBOSE: Inside Begin Block: parser/Parse_Input/__init__")
        self.inpt = inpt
        if len(self.inpt) <= 1: pass
        self.time_i = datetime.now()
        self.parse()

    def parse(self):
        Verbose("VERBOSE: Inside Process Block: parser/Parse_Input/parse")
        if self.inpt.find(" ") != -1:
            cmd = self.inpt[1:self.inpt.find(" ")]
        else:
            cmd = self.inpt[1:]

        if self.inpt[0] == "$":
            args = self.inpt[len(cmd) + 2:].split()
            Verbose("VERBOSE: Executing Run_Command: parser/Parse_Input/parse")
            Run_Command(cmd, args, self.time_i)
        else:
            Verbose("VERBOSE: [ERROR] Invalid Symbol")


class Run_Command:
    def __init__(self, cmd, args, time_i):
        self.time_i = time_i
        self.cmd = cmd
        self.args = args
        self.found = False
        Verbose("VERBOSE: Inside Begin Block: parser/Run_Command/__init__")
        self.run(cmd, args)

    def run(self, cmd, args):
        Verbose("VERBOSE: Inside Process Block: parser/Run_Command/run")
        for i in range(0, len(cmds)):
            if cmd == cmds[i]["chr"] or cmd == cmds[i]["name"]:
                commands.setIntTime(self.time_i)
                # CASE  -- NO ARGUMENTS TO PARSE
                if cmds[i]["args"] == "\[none]" or (cmds[i]["args"] == "\[mix]" and args == []) or (cmds[i]["args"] == "\[nmix]" and args == []):
                    Verbose("VERBOSE: Evaluating Command: parser/Run_Command/run")
                    eval(cmds[i]["function"]+"()")
                # CASE  -- NO ARGUMENTS WHEN THERE SHOULD BE
                elif cmds[i]["args"] != "\[none]" and args == []:
                    Verbose(f"VREBOSE: [ERROR] No arguments given, expected, {cmds[i]['args']}: parser/Run_Command/run")
                    InvalidArgumentCount(args, cmds[i]["args"])
                    return False
                # CASE -- ARGUMENTS TO PARSE
                else:
                    Verbose("VERBOSE: Executing parse_args: parser/Run_Command/run")
                    if self.parse_args(cmds[i], args):
                        Verbose("VERBOSE: Begin Command Execution Block: parser/Run_Command/run")
                        eval(cmds[i]["function"]+"("+"args=args"+")")
                self.found = True
        if not self.found:
            Verbose("VERBOSE: Inside End Block: parser/Run_Command/run")
            Verbose("VERBOSE: [ERROR] Command does not exist: parser/Run_Command/run")
            CommandNotFound(cmd)

    @staticmethod
    def arg_count(cmd, args):
        if len(args) == str(cmd["args"]).count("[") and args[0] != "":
            return True
        else:
            Verbose("VERBOSE: [ERROR] Argument count does not mach expected argument count: parser/Run_Command/arg_count")
            Verbose("VERBOSE: Return False: parser/Run_Command/arg_count")
            InvalidArgumentCount(args, cmd["args"])
            return False

    def parse_args(self, cmd, args):
        Verbose("VERBOSE: Inside Process Block: parser/Run_Command/parse_args")
        for i in range(0, len(args)):
            arg = args[i]
            arg_type = cmd["args"].split(",")
            arg_i = arg_type[i][2:len(arg_type[i]) - 1]

            Verbose("VERBOSE: Evaluating argument type: parser/Run_Command/parse_args")
            try: arg = int(arg)
            except ValueError:
                try: arg = float(arg)
                except ValueError:
                    try:
                        if arg.lower() in ["true", "t", "false", "f"]: arg = bool(arg)
                    except ValueError:
                        pass

            Verbose("VERBOSE: Comparing expected and provided argument types: parser/Run_Command/parse_args")
            if arg_i == "int" and type(arg) == int:
                if self.arg_count(cmd, args): continue
                else: return False

            elif arg_i == "float" and type(arg) == float:
                if self.arg_count(cmd, args): continue
                else: return False

            elif arg_i == "bool" and type(arg) == bool:
                if self.arg_count(cmd, args): continue
                else: return False

            elif arg_i == "str" and type(arg) == str:
                if self.arg_count(cmd, args): continue
                else: return False

            elif arg_i == "mix":
                if (len(args) == str(cmd["args"]).count("[") and args[0] != "") and (type(arg) == str or arg is None): continue
                else:
                    Verbose("VERBOSE: [ERROR] Argument count does not mach expected argument count: parser/Run_Command/parse_args")
                    Verbose("VERBOSE: Return False: parser/Run_Command/parse_args")
                    InvalidArgumentCount(args, cmd["args"])
                    return False

            elif arg_i == "nmix":
                if (len(args) == str(cmd["args"]).count("[") and args[0] != "" and type(arg) == int) or arg is None: continue
                else:
                    Verbose("VERBOSE: [ERROR] Argument count does not mach expected argument count: parser/Run_Command/parse_args")
                    Verbose("VERBOSE: Return False: parser/Run_Command/parse_args")
                    InvalidArgumentCount(args, cmd["args"])
                    return False
            else:
                Verbose("VERBOSE: [ERROR] Argument type does not match expected argument type: parser/Run_Command/parse_args")
                Verbose("VERBOSE: Return False: parser/Run_Command/parse_args")
                InvalidArgument(arg, arg_i)
                return False
        Verbose("VERBOSE: Inside End Block: parser/Run_Command/parse_args")
        Verbose("VERBOSE: Return True: parser/Run_Command/parse_args")
        return True
