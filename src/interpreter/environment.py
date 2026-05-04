"""Runtime environment for GenZ/Brainrot interpreter.

Manages variable storage, function definitions, and call stack.
"""

from typing import Any, Optional
from dataclasses import dataclass, field


@dataclass
class RuntimeValue:
    """A value in the runtime."""
    value: Any
    type_name: str  # 'num', 'txt', 'array', 'function'

    def as_py(self) -> Any:
        """Convert to Python value."""
        return self.value


@dataclass
class UserFunction:
    """A user-defined function."""
    name: str
    params: list[str]
    body: 'Block'  # AST node
    closure: 'Environment'

    def call(self, arguments: list[Any], interpreter: 'Interpreter') -> Any:
        """Execute the function."""
        from src.parser.ast import Block

        # Create new environment for function scope
        func_env = Environment(parent=self.closure)
        for param_name, arg_value in zip(self.params, arguments):
            func_env.define(param_name, RuntimeValue(arg_value, self._infer_type(arg_value)))

        # Save current environment
        old_env = interpreter.environment
        interpreter.environment = func_env

        try:
            result = None
            for stmt in self.body.statements:
                result = interpreter.execute_statement(stmt)
                if isinstance(result, ReturnValue):
                    result = result.value
                    break
            return result
        finally:
            interpreter.environment = old_env

    @staticmethod
    def _infer_type(value: Any) -> str:
        if isinstance(value, (int, float)):
            return "num"
        elif isinstance(value, str):
            return "txt"
        elif isinstance(value, list):
            return "array"
        return "num"


@dataclass
class ReturnValue:
    """Used to unwrap from functions."""
    value: Any


@dataclass
class BreakException:
    """Used to break from loops."""
    pass


@dataclass
class ContinueException:
    """Used to continue in loops."""
    pass


class Environment:
    """Runtime environment for variables."""

    def __init__(self, parent: Optional['Environment'] = None):
        self.parent = parent
        self.variables: dict[str, RuntimeValue] = {}

    def define(self, name: str, value: RuntimeValue) -> None:
        """Define a variable in this scope."""
        self.variables[name] = value

    def get(self, name: str) -> RuntimeValue:
        """Get a variable value."""
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        raise RuntimeError(f"Undefined variable: '{name}'")

    def set(self, name: str, value: RuntimeValue) -> None:
        """Set a variable value (must exist)."""
        if name in self.variables:
            self.variables[name] = value
        elif self.parent:
            self.parent.set(name, value)
        else:
            raise RuntimeError(f"Undefined variable: '{name}'")

    def has(self, name: str) -> bool:
        """Check if variable exists."""
        if name in self.variables:
            return True
        if self.parent:
            return self.parent.has(name)
        return False


class BuiltinFunction:
    """A built-in function callable from GenZ."""

    def __init__(self, name: str, func):
        self.name = name
        self.func = func

    def call(self, arguments: list[Any], interpreter: 'Interpreter') -> Any:
        return self.func(arguments, interpreter)


class Builtins:
    """Container for all built-in functions."""

    @staticmethod
    def print_fn(args: list, interpreter: 'Interpreter') -> None:
        """spill_tea -> print"""
        output = []
        for arg in args:
            output.append(str(arg))
        print(' '.join(output))

    @staticmethod
    def input_fn(args: list, interpreter: 'Interpreter') -> str:
        """Get user input"""
        if args:
            print(args[0], end='')
        return input()

    @staticmethod
    def len_fn(args: list, interpreter: 'Interpreter') -> int:
        """Get length of array or string"""
        if len(args) == 0:
            return 0
        val = args[0]
        if isinstance(val, str) or isinstance(val, list):
            return len(val)
        return 1

    @staticmethod
    def str_fn(args: list, interpreter: 'Interpreter') -> str:
        """Convert to string"""
        if len(args) == 0:
            return ""
        return str(args[0])

    @staticmethod
    def num_fn(args: list, interpreter: 'Interpreter') -> float:
        """Convert to number"""
        if len(args) == 0:
            return 0
        try:
            return float(args[0])
        except (ValueError, TypeError):
            return 0

    @staticmethod
    def range_fn(args: list, interpreter: 'Interpreter') -> list:
        """Generate range of numbers"""
        if len(args) == 1:
            return list(range(int(args[0])))
        elif len(args) == 2:
            return list(range(int(args[0]), int(args[1])))
        elif len(args) >= 3:
            return list(range(int(args[0]), int(args[1]), int(args[2])))
        return []

    @staticmethod
    def abs_fn(args: list, interpreter: 'Interpreter') -> float:
        """Absolute value"""
        return abs(float(args[0])) if args else 0

    @staticmethod
    def pow_fn(args: list, interpreter: 'Interpreter') -> float:
        """Power function"""
        if len(args) >= 2:
            return float(args[0]) ** float(args[1])
        return 0

    @staticmethod
    def sqrt_fn(args: list, interpreter: 'Interpreter') -> float:
        """Square root"""
        import math
        return math.sqrt(float(args[0])) if args else 0

    FUNCTIONS = {
        'print': BuiltinFunction('print', print_fn),
        'input': BuiltinFunction('input', input_fn),
        'len': BuiltinFunction('len', len_fn),
        'str': BuiltinFunction('str', str_fn),
        'num': BuiltinFunction('num', num_fn),
        'range': BuiltinFunction('range', range_fn),
        'abs': BuiltinFunction('abs', abs_fn),
        'pow': BuiltinFunction('pow', pow_fn),
        'sqrt': BuiltinFunction('sqrt', sqrt_fn),
    }

    @classmethod
    def get_function(cls, name: str) -> Optional[BuiltinFunction]:
        return cls.FUNCTIONS.get(name)