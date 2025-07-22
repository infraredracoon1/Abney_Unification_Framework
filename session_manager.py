import json
import datetime
import streamlit as st
from typing import Dict, Any, List, Optional
import base64
import pickle

class SessionManager:
    """Manages session persistence, export, and import functionality."""
    
    def __init__(self):
        self.session_key = 'python_console_session'
    
    def save_session(self, code_history: List[str], output_history: List[Dict], 
                    variables: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save current session data.
        
        Args:
            code_history: List of executed code strings
            output_history: List of execution results
            variables: Current variable namespace
            
        Returns:
            Session data dictionary
        """
        session_data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'code_history': code_history,
            'output_history': self._serialize_output_history(output_history),
            'variables': self._serialize_variables(variables),
            'version': '1.0'
        }
        
        # Store in Streamlit session state for persistence
        st.session_state[self.session_key] = session_data
        
        return session_data
    
    def load_session(self) -> Optional[Dict[str, Any]]:
        """
        Load session data from Streamlit session state.
        
        Returns:
            Session data dictionary or None if no session exists
        """
        return st.session_state.get(self.session_key)
    
    def export_session(self, session_data: Dict[str, Any]) -> str:
        """
        Export session data as JSON string.
        
        Args:
            session_data: Session data dictionary
            
        Returns:
            JSON string representation of session
        """
        return json.dumps(session_data, indent=2, default=str)
    
    def import_session(self, json_data: str) -> Dict[str, Any]:
        """
        Import session data from JSON string.
        
        Args:
            json_data: JSON string containing session data
            
        Returns:
            Parsed session data dictionary
        """
        try:
            session_data = json.loads(json_data)
            
            # Validate session data structure
            required_keys = ['code_history', 'output_history', 'timestamp']
            if not all(key in session_data for key in required_keys):
                raise ValueError("Invalid session data format")
            
            # Deserialize components
            session_data['output_history'] = self._deserialize_output_history(
                session_data['output_history']
            )
            
            if 'variables' in session_data:
                session_data['variables'] = self._deserialize_variables(
                    session_data['variables']
                )
            
            return session_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error importing session: {str(e)}")
    
    def clear_session(self):
        """Clear all session data."""
        if self.session_key in st.session_state:
            del st.session_state[self.session_key]
    
    def _serialize_output_history(self, output_history: List[Dict]) -> List[Dict]:
        """
        Serialize output history for storage.
        
        Args:
            output_history: List of execution results
            
        Returns:
            Serialized output history
        """
        serialized = []
        
        for output in output_history:
            serialized_output = {
                'success': output.get('success', False),
                'stdout': output.get('stdout', ''),
                'stderr': output.get('stderr', ''),
                'result': str(output.get('result', '')) if output.get('result') is not None else None,
                'plots': len(output.get('plots', [])),  # Just store count, not actual plots
                'timestamp': datetime.datetime.now().isoformat()
            }
            serialized.append(serialized_output)
        
        return serialized
    
    def _deserialize_output_history(self, serialized_history: List[Dict]) -> List[Dict]:
        """
        Deserialize output history from storage.
        
        Args:
            serialized_history: Serialized output history
            
        Returns:
            Deserialized output history
        """
        deserialized = []
        
        for output in serialized_history:
            deserialized_output = {
                'success': output.get('success', False),
                'stdout': output.get('stdout', ''),
                'stderr': output.get('stderr', ''),
                'result': output.get('result'),
                'plots': [],  # Plots are not preserved across sessions
                'timestamp': output.get('timestamp', datetime.datetime.now().isoformat())
            }
            deserialized.append(deserialized_output)
        
        return deserialized
    
    def _serialize_variables(self, variables: Dict[str, Any]) -> Dict[str, str]:
        """
        Serialize variables for storage (basic serialization).
        
        Args:
            variables: Variable dictionary
            
        Returns:
            Serialized variables
        """
        serialized = {}
        
        for name, var_info in variables.items():
            try:
                # Store basic information about variables
                serialized[name] = {
                    'type': var_info.get('type', 'unknown'),
                    'repr': var_info.get('repr', ''),
                    'size': var_info.get('size', 'unknown'),
                    'serializable': False  # Mark as non-serializable by default
                }
                
                # Try to serialize simple types
                value = var_info.get('value')
                if isinstance(value, (int, float, str, bool, list, dict)):
                    serialized[name]['value'] = value
                    serialized[name]['serializable'] = True
                
            except Exception:
                # Skip variables that can't be serialized
                continue
        
        return serialized
    
    def _deserialize_variables(self, serialized_vars: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deserialize variables from storage.
        
        Args:
            serialized_vars: Serialized variables
            
        Returns:
            Deserialized variables
        """
        # Note: This is a simplified deserialization
        # Full variable restoration would require more complex handling
        return serialized_vars
    
    def create_backup(self, session_data: Dict[str, Any]) -> str:
        """
        Create a backup of session data.
        
        Args:
            session_data: Session data to backup
            
        Returns:
            Backup identifier
        """
        backup_key = f"{self.session_key}_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        st.session_state[backup_key] = session_data
        return backup_key
    
    def list_backups(self) -> List[str]:
        """
        List available session backups.
        
        Returns:
            List of backup identifiers
        """
        backups = []
        backup_prefix = f"{self.session_key}_backup_"
        
        for key in st.session_state.keys():
            if key.startswith(backup_prefix):
                backups.append(key)
        
        return sorted(backups, reverse=True)  # Most recent first
    
    def restore_backup(self, backup_key: str) -> Optional[Dict[str, Any]]:
        """
        Restore session from backup.
        
        Args:
            backup_key: Backup identifier
            
        Returns:
            Restored session data or None
        """
        if backup_key in st.session_state:
            return st.session_state[backup_key]
        return None
    
    def delete_backup(self, backup_key: str):
        """
        Delete a session backup.
        
        Args:
            backup_key: Backup identifier to delete
        """
        if backup_key in st.session_state:
            del st.session_state[backup_key]
    
    def get_session_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the current session.
        
        Returns:
            Session statistics
        """
        session_data = self.load_session()
        
        if not session_data:
            return {
                'code_blocks': 0,
                'total_lines': 0,
                'execution_count': 0,
                'last_activity': None,
                'session_duration': None
            }
        
        code_history = session_data.get('code_history', [])
        output_history = session_data.get('output_history', [])
        
        total_lines = sum(len(code.splitlines()) for code in code_history)
        successful_executions = sum(1 for output in output_history if output.get('success', False))
        
        stats = {
            'code_blocks': len(code_history),
            'total_lines': total_lines,
            'execution_count': len(output_history),
            'successful_executions': successful_executions,
            'last_activity': session_data.get('timestamp'),
            'session_start': session_data.get('timestamp')
        }
        
        return stats
