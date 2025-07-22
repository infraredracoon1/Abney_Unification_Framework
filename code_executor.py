import sys
import io
import traceback
import matplotlib.pyplot as plt
import matplotlib
import contextlib
from typing import Dict, Any, List
import numpy as np

# Use non-GUI backend for matplotlib
matplotlib.use('Agg')

class CodeExecutor:
    """Handles Python code execution with output capture and variable management."""
    
    def __init__(self):
        self.namespace = {}
        self.setup_namespace()
    
    def setup_namespace(self):
        """Initialize the execution namespace with basic imports."""
        # Add built-in functions and common imports
        self.namespace.update({
            '__builtins__': __builtins__,
            'print': print,
            'len': len,
            'range': range,
            'list': list,
            'dict': dict,
            'str': str,
            'int': int,
            'float': float,
            'bool': bool,
            'type': type,
            'help': help,
            'dir': dir,
        })
    
    def execute_code(self, code: str) -> Dict[str, Any]:
        """
        Execute Python code and capture output, errors, and plots.
        
        Args:
            code: Python code string to execute
            
        Returns:
            Dictionary containing execution results
        """
        result = {
            'success': False,
            'stdout': '',
            'stderr': '',
            'result': None,
            'plots': []
        }
        
        # Capture stdout and stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        
        try:
            # Redirect output streams
            sys.stdout = stdout_buffer
            sys.stderr = stderr_buffer
            
            # Clear any existing matplotlib figures
            plt.clf()
            plt.close('all')
            
            # Compile and execute the code
            compiled_code = compile(code, '<console>', 'exec')
            
            # Execute in the persistent namespace
            exec(compiled_code, self.namespace)
            
            # Capture any matplotlib figures
            figures = []
            for fig_num in plt.get_fignums():
                fig = plt.figure(fig_num)
                if fig.get_axes():  # Only capture if figure has content
                    figures.append(fig)
            
            result.update({
                'success': True,
                'stdout': stdout_buffer.getvalue(),
                'plots': figures,
                'result': None  # For exec, result is typically None
            })
            
        except Exception as e:
            # Capture the error traceback
            error_traceback = traceback.format_exc()
            result.update({
                'success': False,
                'stderr': error_traceback,
                'stdout': stdout_buffer.getvalue()  # Include any output before error
            })
            
        finally:
            # Restore original streams
            sys.stdout = old_stdout
            sys.stderr = old_stderr
        
        return result
    
    def evaluate_expression(self, expression: str) -> Dict[str, Any]:
        """
        Evaluate a Python expression and return the result.
        
        Args:
            expression: Python expression string to evaluate
            
        Returns:
            Dictionary containing evaluation results
        """
        result = {
            'success': False,
            'stdout': '',
            'stderr': '',
            'result': None,
            'plots': []
        }
        
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        
        try:
            sys.stdout = stdout_buffer
            sys.stderr = stderr_buffer
            
            # Compile and evaluate the expression
            compiled_expr = compile(expression, '<console>', 'eval')
            eval_result = eval(compiled_expr, self.namespace)
            
            result.update({
                'success': True,
                'stdout': stdout_buffer.getvalue(),
                'result': eval_result
            })
            
        except Exception as e:
            error_traceback = traceback.format_exc()
            result.update({
                'success': False,
                'stderr': error_traceback,
                'stdout': stdout_buffer.getvalue()
            })
            
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
        
        return result
    
    def get_variables(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about variables in the current namespace.
        
        Returns:
            Dictionary mapping variable names to their info
        """
        variables = {}
        
        for name, value in self.namespace.items():
            if not name.startswith('__') and name != '__builtins__':
                try:
                    var_info = {
                        'type': type(value).__name__,
                        'value': value,
                        'repr': repr(value)[:100] + ('...' if len(repr(value)) > 100 else ''),
                        'size': self._get_size_info(value)
                    }
                    variables[name] = var_info
                except Exception:
                    # Skip variables that can't be inspected
                    continue
                    
        return variables
    
    def _get_size_info(self, obj) -> str:
        """Get size information for an object."""
        try:
            if hasattr(obj, 'shape'):  # numpy arrays, pandas dataframes
                return f"shape: {obj.shape}"
            elif hasattr(obj, '__len__'):  # lists, dicts, etc.
                return f"length: {len(obj)}"
            else:
                return "scalar"
        except Exception:
            return "unknown"
    
    def clear_variables(self):
        """Clear all user-defined variables from the namespace."""
        # Keep only built-in functions and modules
        to_keep = ['__builtins__', 'print', 'len', 'range', 'list', 'dict', 
                   'str', 'int', 'float', 'bool', 'type', 'help', 'dir']
        
        # Also keep any imported modules
        modules_to_keep = {}
        for name, value in self.namespace.items():
            if hasattr(value, '__name__') and hasattr(value, '__file__'):
                modules_to_keep[name] = value
        
        self.namespace.clear()
        self.setup_namespace()
        self.namespace.update(modules_to_keep)
    
    def add_to_namespace(self, name: str, value: Any):
        """Add a variable to the execution namespace."""
        self.namespace[name] = value
    
    def remove_from_namespace(self, name: str):
        """Remove a variable from the execution namespace."""
        if name in self.namespace and name not in ['__builtins__']:
            del self.namespace[name]
    
    def get_namespace_size(self) -> int:
        """Get the number of user-defined variables."""
        return len([name for name in self.namespace.keys() 
                   if not name.startswith('__') and name != '__builtins__'])
