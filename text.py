import streamlit as st
import sys
import io
import traceback
import json
import datetime
from code_executor import CodeExecutor
from session_manager import SessionManager

# Configure page
st.set_page_config(
    page_title="Abney Unification Framework",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'executor' not in st.session_state:
    st.session_state.executor = CodeExecutor()
if 'session_manager' not in st.session_state:
    st.session_state.session_manager = SessionManager()
if 'code_history' not in st.session_state:
    st.session_state.code_history = []
if 'output_history' not in st.session_state:
    st.session_state.output_history = []
if 'current_code' not in st.session_state:
    st.session_state.current_code = ""

def main():
    st.title("🧮 Abney Unification Framework")
    st.markdown("Advanced mathematical computing and scientific analysis platform")
    
    # Sidebar for session management and tools
    with st.sidebar:
        st.header("🛠️ Console Tools")
        
        # Session Management
        st.subheader("Session Management")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Session", use_container_width=True):
                session_data = st.session_state.session_manager.save_session(
                    st.session_state.code_history,
                    st.session_state.output_history,
                    st.session_state.executor.get_variables()
                )
                st.success("Session saved!")
        
        with col2:
            if st.button("🔄 Clear Session", use_container_width=True):
                st.session_state.executor.clear_variables()
                st.session_state.code_history = []
                st.session_state.output_history = []
                st.success("Session cleared!")
        
        # Export/Import
        st.subheader("Export/Import")
        if st.button("📤 Export History", use_container_width=True):
            export_data = {
                'code_history': st.session_state.code_history,
                'output_history': st.session_state.output_history,
                'timestamp': datetime.datetime.now().isoformat()
            }
            st.download_button(
                "Download Session",
                json.dumps(export_data, indent=2),
                file_name=f"python_console_session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        uploaded_file = st.file_uploader("📥 Import Session", type=['json'])
        if uploaded_file is not None:
            try:
                import_data = json.loads(uploaded_file.getvalue().decode())
                st.session_state.code_history = import_data.get('code_history', [])
                st.session_state.output_history = import_data.get('output_history', [])
                st.success("Session imported successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error importing session: {str(e)}")
        
        # Variable Inspector
        st.subheader("🔍 Variable Inspector")
        variables = st.session_state.executor.get_variables()
        if variables:
            for var_name, var_info in variables.items():
                if not var_name.startswith('_'):  # Hide private variables
                    with st.expander(f"{var_name} ({var_info['type']})"):
                        st.code(str(var_info['value']))
        else:
            st.info("No variables defined")
        
        # Quick Actions
        st.subheader("⚡ Quick Actions")
        if st.button("📊 Import Scientific Libraries", use_container_width=True):
            quick_import = """import numpy as np
import pandas as pd
import scipy as sp
from scipy import stats, linalg, optimize
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import sklearn
from sklearn import datasets, model_selection, metrics
import sympy as sym
import networkx as nx
import statsmodels.api as sm
print("Scientific libraries imported successfully!")
print("Available: numpy, pandas, scipy, matplotlib, seaborn, plotly, sklearn, sympy, networkx, statsmodels")"""
            result = st.session_state.executor.execute_code(quick_import)
            st.session_state.code_history.append(quick_import)
            st.session_state.output_history.append(result)
            st.rerun()
        
        # Keyboard Shortcuts Help
        with st.expander("⌨️ Keyboard Shortcuts"):
            st.markdown("""
            - **Ctrl+Enter**: Execute code
            - **Shift+Enter**: Execute and clear
            - **Ctrl+L**: Clear console (upcoming)
            - **Ctrl+S**: Save session (upcoming)
            """)

    # Main console area
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("💻 Code Input")
        
        # Code input area
        code_input = st.text_area(
            "Enter your Python code:",
            height=200,
            value=st.session_state.current_code,
            placeholder="# Enter your Python code here\n# Example:\nimport numpy as np\nx = np.array([1, 2, 3, 4, 5])\nprint(f'Array: {x}')\nprint(f'Mean: {np.mean(x)}')",
            key="code_input"
        )
        
        # Execution buttons
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            execute_button = st.button("▶️ Execute Code", type="primary", use_container_width=True)
        with col_btn2:
            execute_clear_button = st.button("🔄 Execute & Clear", use_container_width=True)
        with col_btn3:
            if st.button("📋 Load Example", use_container_width=True):
                example_code = """# Abney Framework - Advanced Mathematical Analysis
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.fft import fftn, fftfreq
from scipy.stats import qmc
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
import sympy as sym
import networkx as nx

# Mathematical Unification Example
print("🧮 Abney Unification Framework - Demo")
print("=" * 40)

# 1. Symbolic Mathematics
x, y = sym.symbols('x y')
expr = sym.sin(x) * sym.exp(-x**2/2)
diff_expr = sym.diff(expr, x)
print(f"Function: {expr}")
print(f"Derivative: {diff_expr}")

# 2. Data Analysis
data = pd.DataFrame({
    'x': np.random.normal(0, 1, 100),
    'y': np.random.normal(0, 1, 100),
    'category': np.random.choice(['A', 'B', 'C'], 100)
})
print(f"\\nData shape: {data.shape}")
print(data.describe())

# 3. Network Analysis
G = nx.erdos_renyi_graph(20, 0.3)
print(f"\\nNetwork: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
print(f"Average clustering: {nx.average_clustering(G):.3f}")

print("\\n✅ Framework ready for advanced mathematical research!")"""
                st.session_state.current_code = example_code
                st.rerun()
        
        # Execute code logic
        if execute_button or execute_clear_button:
            if code_input.strip():
                with st.spinner("Executing code..."):
                    result = st.session_state.executor.execute_code(code_input)
                    st.session_state.code_history.append(code_input)
                    st.session_state.output_history.append(result)
                    
                    if execute_clear_button:
                        st.session_state.current_code = ""
                        st.rerun()
        
        # Update current code in session state
        st.session_state.current_code = code_input
    
    with col2:
        st.subheader("📤 Output")
        
        # Output display area
        output_container = st.container()
        with output_container:
            if st.session_state.output_history:
                # Show recent outputs
                for i, (code, output) in enumerate(zip(st.session_state.code_history[-5:], 
                                                      st.session_state.output_history[-5:])):
                    with st.expander(f"Output {len(st.session_state.output_history) - 5 + i + 1}", expanded=(i == len(st.session_state.output_history[-5:]) - 1)):
                        if output['success']:
                            if output['stdout']:
                                st.success("Output:")
                                st.text(output['stdout'])
                            if output['result'] is not None and output['result'] != '':
                                st.info("Result:")
                                st.code(str(output['result']))
                            if output['plots']:
                                st.success("Plots:")
                                for plot in output['plots']:
                                    st.pyplot(plot)
                        else:
                            st.error("Error:")
                            st.code(output['stderr'])
            else:
                st.info("No output yet. Execute some code to see results!")
    
    # History section
    if st.session_state.code_history:
        st.subheader("📚 Code History")
        
        # Search through history
        search_term = st.text_input("🔍 Search history:", placeholder="Search your code history...")
        
        # Filter history based on search
        if search_term:
            filtered_history = [(i, code) for i, code in enumerate(st.session_state.code_history) 
                              if search_term.lower() in code.lower()]
        else:
            filtered_history = list(enumerate(st.session_state.code_history))
        
        # Display history in reverse order (most recent first)
        for i, (original_index, code) in enumerate(reversed(filtered_history[-10:])):  # Show last 10
            with st.expander(f"Code Block {original_index + 1}", expanded=False):
                st.code(code, language='python')
                col_hist1, col_hist2 = st.columns(2)
                with col_hist1:
                    if st.button(f"🔄 Re-run", key=f"rerun_{original_index}"):
                        result = st.session_state.executor.execute_code(code)
                        st.session_state.output_history.append(result)
                        st.success("Code re-executed!")
                        st.rerun()
                with col_hist2:
                    if st.button(f"📋 Copy to Input", key=f"copy_{original_index}"):
                        st.session_state.current_code = code
                        st.success("Copied to input area!")
                        st.rerun()

if __name__ == "__main__":
    main()
