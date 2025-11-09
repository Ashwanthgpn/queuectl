# 🚀 QueueCTL - Production Background Job Queue System

> **A robust, production-ready CLI job queue system with exponential backoff retries and Dead Letter Queue**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![Tests](https://img.shields.io/badge/tests-100%25%20passing-brightgreen)](https://github.com/AshwanthGpn/queuectl)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/status-production%20ready-success)](https://github.com/AshwanthGpn/queuectl)

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

## 🏁 Quick Start

### 📋 Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- **git** (for cloning the repository)

**Verify your installation:**

```bash
python --version
pip --version
git --version
```

---

## 🛠️ Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/AshwanthGpn/queuectl.git
cd queuectl
```

### Step 2: Set Up Virtual Environment

**Windows:**
```cmd
python -m venv queuectl_env
queuectl_env\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv queuectl_env
source queuectl_env/bin/activate
```

> 💡 You should see `(queuectl_env)` in your terminal prompt after activation.

### Step 3: Install the Package

```bash
pip install -e .
```

### Step 4: Verify Installation

```bash
queuectl --help
```

**Expected Output:**
```
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
```

### Step 5: Test Basic Functionality

```bash
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
```

---

## 📚 Command Reference

### 🧩 Core Commands

| Command | Description | Example |
|---------|-------------|---------|
| `enqueue` | Add job to queue | `queuectl enqueue "sleep 5"` |
| `start` | Start workers | `queuectl start --count 3` |
| `stop` | Stop workers | `queuectl stop` |
| `status` | System overview | `queuectl status` |
| `list` | Filter jobs by state | `queuectl list --state pending` |

### ⚙️ Configuration

| Command | Description | Example |
|---------|-------------|---------|
| `config` | View settings | `queuectl config` |
| `config --key` | Modify setting | `queuectl config --key max_retries --value 5` |

### 🆘 Dead Letter Queue (DLQ) Management

| Command | Description | Example |
|---------|-------------|---------|
| `dlq list` | View failed jobs | `queuectl dlq list` |
| `dlq retry` | Recover job | `queuectl dlq retry <job-uuid>` |

---

## 🧪 Testing & Verification

### ✅ Run Unit Tests

```bash
python -m pytest tests/ -v
```

**Expected Output:**
```
============================= test session starts =============================
collected 3 items

tests/test_basic.py::TestQueueSystem::test_cli_enqueue PASSED           [ 33%]
tests/test_basic.py::TestQueueSystem::test_dlq_functionality PASSED     [ 66%]
tests/test_basic.py::TestQueueSystem::test_job_persistence PASSED       [100%]

============================== 3 passed in 2.06s ==============================
```

### 🧩 Run Comprehensive Verification

```bash
python verify_all.py
```

**Expected Output:**
```
All systems verified successfully ✅
```

---

## 🏗️ Project Structure

```
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
```

---

## 🔧 Development Workflow

### 1. Activate Your Virtual Environment

**Windows:**
```cmd
queuectl_env\Scripts\activate
```

**Linux/Mac:**
```bash
source queuectl_env/bin/activate
```

### 2. Make Your Changes

Edit files in the `queuectl/` directory. Changes take effect immediately since the package is installed in editable mode (`-e`).

### 3. Test Your Changes

```bash
# Test CLI
queuectl --help

# Run test suite
python -m pytest tests/ -v
```

### 4. Adding New Dependencies

Edit `requirements.txt`:
```
click>=8.0.0
tabulate>=0.8.0
your-new-dependency>=1.0.0
```

Then reinstall:
```bash
pip install -e .
```

---

## 🐛 Troubleshooting

### ⚠️ `queuectl` Command Not Found

**Solution:**
```bash
# Reactivate virtual environment
# Windows:
queuectl_env\Scripts\activate

# Linux/Mac:
source queuectl_env/bin/activate

# Reinstall package
pip install -e .
```

### ⚠️ Permission Errors (Windows)

**Solution:** Run your terminal as Administrator or adjust folder permissions.

### ⚠️ File Locking Errors

**Solution:**
```bash
# Stop all workers first
queuectl stop
```

### ⚠️ Virtual Environment Won't Activate

**Solution:**
```bash
# Recreate the virtual environment
deactivate
rm -rf queuectl_env  # Linux/Mac
# OR
rmdir /s queuectl_env  # Windows

python -m venv queuectl_env
# Then reactivate and reinstall
```

### ⚠️ Checking Installed Packages

**Windows:**
```cmd
pip list | findstr queuectl
```

**Linux/Mac:**
```bash
pip list | grep queuectl
```

---

## 🔒 Security Considerations

> ⚠️ **WARNING:** QueueCTL executes shell commands. Only enqueue jobs from trusted sources. Never expose the enqueue endpoint to untrusted users without proper authentication and input validation.

**Best Practices:**
- Run workers with minimal privileges
- Validate and sanitize all job commands
- Monitor the DLQ for suspicious patterns
- Keep storage files in secure locations with appropriate permissions

---

## 📦 Storage

Jobs are persisted in JSON format at:
- **Default location:** `./queuectl_storage/jobs.json`
- **Custom location:** Use `--storage-path` flag

Example:
```bash
queuectl --storage-path /path/to/storage status
```

---

## 🆘 Getting Help

If you encounter issues:

1. ✅ Verify all prerequisites are installed
2. ✅ Ensure your virtual environment is activated
3. ✅ Check package installation: `pip list | grep queuectl` (Linux/Mac) or `pip list | findstr queuectl` (Windows)
4. ✅ Run verification script: `python verify_all.py`
5. ✅ Check [GitHub Issues](https://github.com/AshwanthGpn/queuectl/issues)



## 👨‍💻 Author

**Ashwanth G P N**  
Senior Software Engineer

[GitHub](https://github.com/AshwanthGpn) • [LinkedIn](www.linkedin.com/in/ashwanth-gpn-ab53aa2a7)

---

