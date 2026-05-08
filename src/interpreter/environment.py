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
        except ReturnValue as e:
            return e.value
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


class ReturnValue(Exception):
    """Used to unwrap from functions."""
    def __init__(self, value: Any):
        self.value = value
        super().__init__()


class BreakException(Exception):
    """Used to break from loops."""
    pass


class ContinueException(Exception):
    """Used to continue in loops."""
    pass


class InterpreterError(Exception):
    """Raised when runtime error occurs."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(f"Runtime error: {message}")


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
        raise InterpreterError(f"Undefined variable: '{name}'")

    def set(self, name: str, value: RuntimeValue) -> None:
        """Set a variable value (must exist)."""
        if name in self.variables:
            self.variables[name] = value
        elif self.parent:
            self.parent.set(name, value)
        else:
            raise InterpreterError(f"Undefined variable: '{name}'")

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

    @staticmethod
    def ohio_fn(args: list, interpreter: 'Interpreter') -> None:
        """Triggers a chaotic state or error condition."""
        raise InterpreterError("Down in Ohio, swag like Ohio. Chaotic state detected!")

    @staticmethod
    def grimace_shake_fn(args: list, interpreter: 'Interpreter') -> None:
        """Triggers a fatal error or crash."""
        raise InterpreterError("Code poisoned by Grimace Shake! Fatal crash...")

    @staticmethod
    def mewing_fn(args: list, interpreter: 'Interpreter') -> None:
        """Silences output or pauses execution."""
        import time
        sleep_ms = float(args[0]) if args else 1000.0
        time.sleep(sleep_ms / 1000.0)

    @staticmethod
    def fanum_tax_fn(args: list, interpreter: 'Interpreter') -> float:
        """Steals a percentage of a variable's value."""
        val = float(args[0]) if args else 0.0
        return val * 0.8  # 20% tax

    @staticmethod
    def rizz_fn(args: list, interpreter: 'Interpreter') -> float:
        """Charisma. Adds value."""
        val = float(args[0]) if args else 0.0
        return val + 10.0

    @staticmethod
    def ballerina_cappuccina_fn(args: list, interpreter: 'Interpreter') -> str:
        """A graceful and fancy operation."""
        return "Fancy Ballerina Cappuccina"

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
        'ohio': BuiltinFunction('ohio', ohio_fn),
        'grimace_shake': BuiltinFunction('grimace_shake', grimace_shake_fn),
        'mewing': BuiltinFunction('mewing', mewing_fn),
        'fanum_tax': BuiltinFunction('fanum_tax', fanum_tax_fn),
        'rizz': BuiltinFunction('rizz', rizz_fn),
        'ballerina_cappuccina': BuiltinFunction('ballerina_cappuccina', ballerina_cappuccina_fn),
    }

    @classmethod
    def get_function(cls, name: str) -> Optional[BuiltinFunction]:
        return cls.FUNCTIONS.get(name)