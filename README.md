# Abney Unification Framework

A unified framework for advanced mathematical computing, scientific analysis, and complex computational research. Built for researchers, mathematicians, and computational scientists working with sophisticated mathematical models and simulations.

## 🚀 Features

- **Interactive Python Execution**: Run Python code with real-time output capture
- **Mathematical Computing**: Built-in support for NumPy, SciPy, Matplotlib, and Plotly
- **Session Management**: Save, load, and export your work sessions
- **Variable Inspector**: View and manage your workspace variables
- **Code History**: Search and reuse your previous code blocks
- **Plot Visualization**: Automatic matplotlib and plotly plot rendering
- **Scientific Libraries**: Quick import of common scientific computing libraries
- **Error Handling**: Comprehensive error capture and display

## 📦 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/infraredracoon1/Abney_Unification_Framework.git
   cd Abney_Unification_Framework
   ```

2. **Run with Docker Compose**:
   ```bash
   docker-compose up
   ```

3. **Access the application**:
   Open your browser and navigate to `http://localhost:5000`

### Using Python Directly

1. **Prerequisites**:
   - Python 3.11 or higher
   - pip or uv package manager

2. **Install dependencies**:
   ```bash
   pip install streamlit numpy scipy matplotlib plotly
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py --server.port 5000 --server.address 0.0.0.0 --server.headless true
   ```

### Using Quick Start Script

For quick setup:

```bash
chmod +x run.sh
./run.sh
```

## 🐳 Docker Deployment

### Build and Run

```bash
# Build the image
docker build -t python-math-console .

# Run the container
docker run -p 5000:5000 python-math-console
```

### Production Deployment

```bash
# Run with nginx reverse proxy
docker-compose --profile production up
```

## 🔧 Configuration

### Streamlit Configuration

The application uses a custom Streamlit configuration in `.streamlit/config.toml`:

```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000

[theme]
base = "dark"
```

### Environment Variables

- `STREAMLIT_SERVER_PORT`: Server port (default: 5000)
- `STREAMLIT_SERVER_ADDRESS`: Server address (default: 0.0.0.0)
- `STREAMLIT_SERVER_HEADLESS`: Run in headless mode (default: true)

## 📖 Usage Examples

### Basic Mathematical Operations

```python
import numpy as np
import matplotlib.pyplot as plt

# Create data
x = np.linspace(0, 10, 100)
y = np.sin(x) * np.exp(-x/5)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', linewidth=2)
plt.title('Damped Sine Wave')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.show()
```

### Advanced Scientific Computing

```python
from scipy import stats, optimize
from scipy.fft import fft, fftfreq

# Generate sample data
np.random.seed(42)
data = stats.norm.rvs(size=1000, loc=5, scale=2)

# Perform statistical analysis
mean_val = np.mean(data)
std_val = np.std(data)
skewness = stats.skew(data)

print(f"Mean: {mean_val:.2f}")
print(f"Std: {std_val:.2f}")
print(f"Skewness: {skewness:.2f}")
```

### Navier-Stokes Simulation Example

The console includes a built-in example for fluid dynamics simulation:

```python
# Click "Load Example" button to load the Navier-Stokes simulation
# This demonstrates advanced mathematical computing capabilities
```

## 🗂️ Project Structure

```
Abney_Unification_Framework/
├── app.py                 # Main Streamlit application
├── code_executor.py       # Python code execution engine
├── session_manager.py     # Session persistence and management
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── Dockerfile            # Container configuration
├── docker-compose.yml    # Multi-service deployment
├── requirements.txt      # Python dependencies
├── run.sh               # Quick start script

└── README.md            # This file
```

## 🛠️ Development

### Local Development

1. **Clone and setup**:
   ```bash
   git clone https://github.com/infraredracoon1/Abney_Unification_Framework.git
   cd Abney_Unification_Framework
   pip install -r requirements-extended.txt
   ```

2. **Run in development mode**:
   ```bash
   streamlit run app.py
   ```

### Contributing

1. Fork the repository  
2. Create a feature branch
3. Commit your changes
4. Push to the branch  
5. Open a Pull Request

## 📋 Requirements

### Python Dependencies

- streamlit >= 1.28.0
- numpy >= 1.24.0
- scipy >= 1.10.0
- matplotlib >= 3.7.0
- plotly >= 5.15.0

### System Requirements

- Python 3.11+
- 512MB RAM minimum
- Docker (for containerized deployment)

## 🚀 Deployment Options

### Cloud Platforms

- **Streamlit Cloud**: Direct deployment from GitHub
- **Heroku**: Using the provided Dockerfile  
- **Google Cloud Run**: Container-based deployment
- **AWS ECS**: Production-ready container orchestration

### Self-Hosted

- **Docker**: Single container deployment
- **Docker Compose**: Multi-service deployment with nginx

## 🔒 Security

- Non-root user execution in containers
- Health checks for container monitoring
- Input sanitization for code execution
- Session isolation between users

## 📜 License

This project is licensed under the MIT License.

## 🤝 Support

- **Issues**: [GitHub Issues](https://github.com/infraredracoon1/Abney_Unification_Framework/issues)
- **Discussions**: [GitHub Discussions](https://github.com/infraredracoon1/Abney_Unification_Framework/discussions)
- **Documentation**: [Wiki](https://github.com/infraredracoon1/Abney_Unification_Framework/wiki)

## 🏆 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Scientific computing powered by [NumPy](https://numpy.org/) and [SciPy](https://scipy.org/)
- Visualization by [Matplotlib](https://matplotlib.org/) and [Plotly](https://plotly.com/)
- Inspired by Jupyter notebooks and mathematical computing environments