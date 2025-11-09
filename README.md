# 🚀 QueueCTL - Production Background Job Queue System

> **A robust, production-ready CLI job queue system with exponential backoff retries and Dead Letter Queue**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![Tests](https://img.shields.io/badge/tests-100%25%20passing-brightgreen)](https://github.com/yourusername/queuectl)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/status-production%20ready-success)](https://github.com/yourusername/queuectl)

---

## ✨ Features

| Feature | Status | Description |
|---------|--------|-------------|
| ✅ CLI Interface | **Production Ready** | Full command-line control |
| ✅ Persistent Storage | **Production Ready** | JSON-based job persistence |
| ✅ Multi-worker Processing | **Production Ready** | Concurrent job execution |
| ✅ Exponential Backoff | **Production Ready** | Smart retry with configurable delays |
| ✅ Dead Letter Queue | **Production Ready** | Failed job recovery system |
| ✅ Real-time Monitoring | **Production Ready** | Live status and job tracking |

---

## 🏁 Local Development Setup

### 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher**
- **pip** (Python package manager)
- **git** (for cloning the repository)

**Verify your installation:**
```bash
python --version
pip --version
git --version
🛠️ Step-by-Step Installation
Step 1: Clone the Repository
bash
Copy code
# Clone the project
git clone https://github.com/AshwanthGpn/queuectl.git

# Navigate to project directory
cd queuectl
Step 2: Set Up Virtual Environment
Windows:

bash
Copy code
# Create virtual environment
python -m venv queuectl_env

# Activate virtual environment
queuectl_env\Scripts\activate

# Verify activation (you should see (queuectl_env) in your prompt)
Linux/Mac:

bash
Copy code
# Create virtual environment
python -m venv queuectl_env

# Activate virtual environment
source queuectl_env/bin/activate

# Verify activation (you should see (queuectl_env) in your prompt)
Step 3: Install the Package
bash
Copy code
# Install the package in development mode
pip install -e .

# Verify installation
pip list | grep queuectl
Step 4: Verify Installation
bash
Copy code
# Test if queuectl command works
queuectl --help
Expected Output:

text
Copy code
Usage: queuectl [OPTIONS] COMMAND [ARGS]...

  QueueCTL - Background Job Queue System

Options:
  --storage-path TEXT  Path to storage directory
  --help               Show this message and exit.

Commands:
  config   Manage system configuration
  dlq      Manage Dead Letter Queue
  enqueue  Enqueue a new job
  list     List jobs
  start    Start worker processes
  status   Show system status
  stop     Stop all worker processes
Step 5: Test Basic Functionality
bash
Copy code
# Check initial status
queuectl status

# Enqueue your first job
queuectl enqueue "echo 'QueueCTL is working!'"

# Verify job was added
queuectl list

# Start a worker to process the job
queuectl start --count 1 --timeout 10

# Check results
queuectl list --state completed
📚 Command Reference
🧩 Core Commands
Command	Description	Example
enqueue	Add job to queue	queuectl enqueue "sleep 5"
start	Start workers	queuectl start --count 3
stop	Stop workers	queuectl stop
status	System overview	queuectl status
list	Filter jobs by state	queuectl list --state pending

⚙️ Configuration
Command	Description	Example
config	View settings	queuectl config
config --key	Modify setting	queuectl config --key max_retries --value 5

🆘 DLQ Management
Command	Description	Example
dlq list	View failed jobs	queuectl dlq list
dlq retry	Recover job	queuectl dlq retry <full-uuid>

🧪 Testing & Verification
✅ Run Unit Tests
bash
Copy code
# Run the test suite
python -m pytest tests/ -v
Expected Output:

text
Copy code
============================= test session starts =============================
collected 3 items

tests/test_basic.py::TestQueueSystem::test_cli_enqueue PASSED           [ 33%]
tests/test_basic.py::TestQueueSystem::test_dlq_functionality PASSED     [ 66%]
tests/test_basic.py::TestQueueSystem::test_job_persistence PASSED       [100%]

============================== 3 passed in 2.06s ==============================
🧩 Run Comprehensive Verification
bash
Copy code
# Run full integration test
python verify_all.py
Expected Output:

text
Copy code
Building graphs for years: 2020 2021 2022 2023 2024 2025
All systems verified successfully ✅
🏗️ Project Structure
text
Copy code
queuectl/
├── core/
│   ├── job.py          # Job model and retry logic
│   ├── queue.py        # Job queue manager
│   ├── worker.py       # Worker pool implementation
│   ├── storage.py      # JSON-based persistent storage
│   └── utils/
│       └── config.py   # Configuration management
├── cli.py              # Main CLI entrypoint (Click)
├── setup.py            # Package configuration
├── verify_all.py       # Comprehensive verification script
└── tests/
    └── test_basic.py   # Unit test suite
🔧 Development
🧰 Activate Your Virtual Environment
bash
Copy code
# Windows
queuectl_env\Scripts\activate

# Linux/Mac
source queuectl_env/bin/activate
Make code changes in the queuectl/ directory.

🧩 Test Your Changes
bash
Copy code
# The package is installed in editable mode, so changes are immediate
queuectl --help
Run tests to ensure nothing is broken:

bash
Copy code
python -m pytest tests/ -v
➕ Adding New Dependencies
If you need to add new Python dependencies, add them to your requirements.txt:

text
Copy code
click>=8.0.0
tabulate>=0.8.0
your-new-dependency>=1.0.0
Then reinstall the package:

bash
Copy code
pip install -e .
🐛 Troubleshooting
⚠️ Common Issues
Issue: queuectl command not found
Solution:

bash
Copy code
# Reactivate virtual environment and reinstall
queuectl_env\Scripts\activate  # Windows
# OR
source queuectl_env/bin/activate  # Linux/Mac
pip install -e .
Issue: Permission errors on Windows
Solution:

bash
Copy code
# Run as administrator or fix permissions
Issue: File locking errors
Solution:

bash
Copy code
# Stop all workers and retry
queuectl stop
Issue: Virtual environment not activating
Solution:

bash
Copy code
# Recreate the virtual environment
deactivate
rm -rf queuectl_env
python -m venv queuectl_env
# Then reactivate and reinstall
🆘 Getting Help
If you encounter issues:

Check that all prerequisites are installed correctly

Ensure your virtual environment is activated

Verify the package installed properly with pip list

Run the verification script:

bash
Copy code
python verify_all.py
👨‍💻 Author
Ashwanth G P N
Senior Software Engineer