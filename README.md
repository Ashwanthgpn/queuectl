# QueueCTL — Background Job Queue System

  [![License](https://img.shields.io/static/v1?label=License&message=MIT&color=blue&?style=plastic&logo=appveyor)](https://opensource.org/license/MIT)



## Table Of Content

- [Description](#description)

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contribution)
- [Tests](#tests)
- [GitHub](#github)
- [Contact](#contact)
- [License](#license)




![GitHub repo size](https://img.shields.io/github/repo-size/AshwanthGpn/queuectl?style=plastic)

  ![GitHub top language](https://img.shields.io/github/languages/top/AshwanthGpn/queuectl?style=plastic)



## Description

  💡 What was your motivation?

My motivation was to understand how distributed job queue systems work under the hood — like Celery or RabbitMQ — but without relying on heavy frameworks.
I wanted to build a lightweight, production-style CLI queue system from scratch to learn about concurrency, persistence, and fault tolerance in real-world background processing systems.

⚙️ Why did you build this project?

I built QueueCTL to gain hands-on experience designing and implementing:

A reliable job scheduling and execution pipeline

Worker process management

Retry mechanisms with exponential backoff

Dead Letter Queue (DLQ) for failed jobs

Configuration and monitoring through a clean CLI interface

Essentially, I wanted to bridge the gap between conceptual system design and real, working code that I could run and extend.

🧩 What problem does it solve?

QueueCTL solves the problem of managing background jobs safely and efficiently without needing a large external dependency or server setup.
It lets developers:

Offload long-running or error-prone tasks

Automatically retry failed jobs

Monitor the system state easily

Ensure no job is lost (thanks to JSON-based persistence and DLQ)

This is particularly useful for local automation, testing asynchronous workflows, or educational system design purposes.

🧠 What did you learn?

Through this project, I learned:

How to design and implement a persistent job queue

How worker concurrency and process management work in Python

The logic behind retry policies and backoff algorithms

How to build a robust CLI interface using the click library

How to organize a production-style Python package with tests, setup, and configuration management

It also helped me strengthen my understanding of software architecture, logging, and fault recovery systems.











## Installation

Method 1: Standard Installation (Recommended)
Step 1: Download the Project
bash
# Clone the repository
git clone https://github.com/yourusername/queuectl.git
cd queuectl

# OR download and extract ZIP
# Unzip and navigate to the queuectl directory
Step 2: Set Up Virtual Environment
Windows:

bash
# Create virtual environment
python -m venv queuectl_env

# Activate virtual environment
queuectl_env\Scripts\activate

# Your terminal should now show (queuectl_env) prefix
macOS/Linux:

bash
# Create virtual environment
python3 -m venv queuectl_env

# Activate virtual environment
source queuectl_env/bin/activate

# Your terminal should now show (queuectl_env) prefix
Step 3: Install Dependencies
bash
# Install the package in development mode
pip install -e .

# Alternative: Install from requirements (if available)
# pip install -r requirements.txt
Step 4: Verify Installation
bash
# Check if queuectl command is available
queuectl --help

# Expected output should show available commands
Method 2: Development Installation
For contributors or those who want to modify the code:

bash
# Clone the repository
git clone https://github.com/yourusername/queuectl.git
cd queuectl

# Create and activate virtual environment
python -m venv queuectl_env
# Windows: queuectl_env\Scripts\activate
# Unix: source queuectl_env/bin/activate

# Install in development mode with testing dependencies
pip install -e ".[dev]"

# Run tests to verify installation
python -m pytest tests/ -v
Method 3: Direct PIP Installation (If Published)
bash
# If published to PyPI
pip install queuectl

# Verify installation
queuectl --version
🔧 Platform-Specific Instructions
Windows
Open Command Prompt or PowerShell as Administrator

Ensure Python is in PATH:

cmd
# Check Python
python --version
If Python not found, download from python.org and check "Add Python to PATH" during installation

macOS
bash
# Ensure Homebrew is installed (optional)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python if not present
brew install python

# Proceed with standard installation
Linux (Ubuntu/Debian)
bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv

# Proceed with standard installation
Linux (CentOS/RHEL)
bash
# Install Python and pip
sudo yum install python3 python3-pip

# Or for newer versions
sudo dnf install python3 python3-pip

# Proceed with standard installation




QueueCTL — Background Job Queue System is built with the following tools and libraries: <ul><li>Python 3.8+</li> <li>Click - For building command-line interfaces</li> <li>Tabulate - For formatted table output in CLI</li> <li>Pytest - For unit testing and test framework</li> <li>JSON - For persistent job storage and data serialization</li> <li>subprocess - For executing shell commands as jobs</li> <li>threading - For concurrent worker management</li> <li>logging - For system logging and debugging</li> <li>uuid - For generating unique job identifiers</li> <li>datetime - For job timestamping and scheduling</li> <li>time - For sleep operations and timing controls</li> <li>os - For file system operations and path management</li> <li>signal - For graceful worker shutdown handling</li> <li>setuptools - For package distribution and installation</li></ul>





## Usage
 
🎯 Basic Usage
Starting with QueueCTL
bash
# Get help and see all available commands
queuectl --help

# Check system status
queuectl status

# View current configuration
queuectl config
📥 Adding Jobs to the Queue
Basic Job Enqueue
bash
# Add a simple command
queuectl enqueue "echo 'Hello World'"

# Add a job with custom retry settings
queuectl enqueue "sleep 5" --max-retries 3

# Add a job that might fail (limited retries)
queuectl enqueue "invalid_command" --max-retries 1
Job with Custom Options
bash
# Job with specific timeout
queuectl enqueue "long_running_script.sh" --timeout 60

# Job with custom ID (optional)
queuectl enqueue "process_data.py" --job-id "data-processing-001"
👥 Worker Management
Starting Workers
bash
# Start a single worker
queuectl start

# Start multiple workers
queuectl start --count 3

# Start workers with timeout (auto-stop after specified seconds)
queuectl start --count 2 --timeout 300  # 5 minutes

# Start workers with specific configuration
queuectl start --count 4 --worker-name "high-priority"
Stopping Workers
bash
# Stop all workers gracefully
queuectl stop

# Stop workers immediately (force stop)
queuectl stop --force
📊 Monitoring and Inspection
System Status
bash
# Overall system status
queuectl status

# Detailed system information
queuectl status --verbose
Listing Jobs
bash
# List all jobs
queuectl list

# Filter by state
queuectl list --state pending
queuectl list --state completed
queuectl list --state failed
queuectl list --state processing

# Show specific number of jobs
queuectl list --limit 10

# Show jobs with full details
queuectl list --verbose
Job Information
bash
# Get specific job details
queuectl job show <job-id>

# View job history and attempts
queuectl job history <job-id>
⚠️ Dead Letter Queue (DLQ) Management
Viewing DLQ
bash
# List all jobs in Dead Letter Queue
queuectl dlq list

# Show DLQ statistics
queuectl dlq stats

# View detailed DLQ information
queuectl dlq list --verbose
DLQ Recovery
bash
# Retry a specific job from DLQ (use full UUID)
queuectl dlq retry 08232c92-a58f-4419-a31f-feecc1112dfe

# Retry multiple jobs
queuectl dlq retry <job-id-1> <job-id-2> <job-id-3>

# Retry all jobs in DLQ
queuectl dlq retry --all
DLQ Maintenance
bash
# Remove specific job from DLQ
queuectl dlq remove <job-id>

# Clear entire DLQ
queuectl dlq clear --confirm
⚙️ Configuration Management
Viewing Configuration
bash
# Show all configuration settings
queuectl config

# Show specific configuration value
queuectl config --key max_retries
Modifying Configuration
bash
# Update configuration values
queuectl config --key max_retries --value 5
queuectl config --key backoff_base --value 3
queuectl config --key worker_count --value 4
queuectl config --key job_timeout --value 60
queuectl config --key log_level --value DEBUG
Configuration Persistence
bash
# Reset to default configuration
queuectl config --reset

# Export configuration to file
queuectl config --export config.json

# Import configuration from file
queuectl config --import config.json
🗂️ Storage and Data Management
Storage Operations
bash
# Check storage location and size
queuectl storage info

# Backup job data
queuectl storage backup backup_directory/

# Restore from backup
queuectl storage restore backup_directory/

# Clean up old completed jobs
queuectl storage cleanup --older-than 7d
🔍 Advanced Usage
Filtering and Searching
bash
# List jobs by command pattern
queuectl list --command "echo*"

# List jobs created in last hour
queuectl list --since 1h

# List jobs with specific state and command
queuectl list --state failed --command "*script*"
Batch Operations
bash
# Enqueue multiple jobs from file
queuectl enqueue --file jobs.txt

# Bulk retry based on filter
queuectl dlq retry --filter "command:invalid*"
Real-time Monitoring






## Contribution
 
🤝 How to Contribute
We love your input! We want to make contributing to QueueCTL as easy and transparent as possible.

Ways to Contribute
🐛 Report bugs

💡 Suggest new features

📖 Improve documentation

🔧 Submit code fixes

🧪 Write tests

🌟 Share use cases

🚀 Getting Started
Prerequisites for Development
bash
# Ensure you have Python 3.8+ and git
python --version
git --version

# Fork the repository on GitHub
# Clone your fork locally
git clone https://github.com/your-username/queuectl.git
cd queuectl
Development Environment Setup
bash
# Create virtual environment
python -m venv queuectl_dev
source queuectl_dev/bin/activate  # Linux/Mac
# queuectl_dev\Scripts\activate  # Windows

# Install in development mode with all dependencies
pip install -e ".[dev]"

# Verify installation
queuectl --help
python -m pytest tests/ -v
📋 Development Workflow
1. Branch Strategy
bash
# Create a feature branch from main
git checkout -b feature/amazing-feature

# Or a bugfix branch
git checkout -b fix/issue-description

# Or a documentation branch
git checkout -b docs/improve-readme
2. Code Standards
Python Code Style
bash
# We use Black for code formatting
black queuectl/ tests/

# And isort for import sorting
isort queuectl/ tests/

# Run linting checks
flake8 queuectl/ tests/
Code Conventions
Follow PEP 8 guidelines

Use type hints for new functions

Write docstrings for all public methods

Keep functions small and focused

Use meaningful variable names

3. Testing Requirements
bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=queuectl tests/

# Run specific test file
pytest tests/test_basic.py -v

# Run verification script
python verify_all.py
Test Standards
Write tests for all new functionality

Maintain 100% test coverage for new code

Include both unit and integration tests

Test edge cases and error conditions

4. Documentation Updates
Update README.md for user-facing changes

Add docstrings for new functions/classes

Update command help texts in CLI

Include examples for new features

🎯 Contribution Areas
High Priority Needs
🐛 Bug fixes and stability improvements

📊 Performance optimizations

🔧 Windows compatibility enhancements

🧪 Additional test coverage

📖 Documentation improvements

Feature Development
🚀 New queue backends (Redis, PostgreSQL)

📱 Web dashboard interface

⏰ Scheduled job support

🔄 Job dependencies and workflows

📈 Metrics and monitoring

🐛 Reporting Bugs
Bug Report Template
markdown
## Description
Clear description of the issue

## Steps to Reproduce
1. Command run
2. Expected behavior
3. Actual behavior

## Environment
- OS: [e.g. Windows 10, Ubuntu 20.04]
- Python Version: [e.g. 3.8.5]
- QueueCTL Version: [e.g. 0.1.0]

## Logs
Relevant log output or error messages

## Additional Context
Screenshots, configuration, or other relevant information
Creating Issues
Use descriptive titles

Include reproduction steps

Add environment details

Attach logs if available

Check for existing issues first

💡 Suggesting Features
Feature Request Template
markdown
## Problem Statement
What problem does this feature solve?

## Proposed Solution
How should the feature work?

## Alternatives Considered
Other approaches you considered

## Use Cases
Real-world scenarios where this would be helpful

## Additional Context
Screenshots, mockups, or references
🔧 Pull Request Process
PR Checklist
Code follows project style guidelines

Tests pass locally (pytest tests/ -v)

Documentation updated (README, docstrings)

Verification script passes (python verify_all.py)

No decrease in test coverage

Changes are focused and atomic

PR Submission Steps
Fork the repository

Create your feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

PR Review Process
Automated Checks - CI runs tests and linting

Code Review - Maintainers review code quality

Testing - Verify functionality across platforms

Documentation Review - Ensure docs are updated

Merge - Once approved, PR is merged

🏗️ Project Structure
Code Organization
text
queuectl/
├── core/           # Core functionality
│   ├── job.py     # Job models and logic
│   ├── queue.py   # Queue management
│   ├── worker.py  # Worker processes
│   ├── storage.py # Data persistence
│   └── utils/     # Utility functions
├── cli.py         # Command-line interface
├── tests/         # Test suite
└── docs/          # Documentation
Adding New Commands
python
# Example: Adding a new CLI command
@click.command()
@click.option('--verbose', is_flag=True, help='Verbose output')
def new_command(verbose):
    """Description of new command."""
    # Implementation here
    pass
🧪 Testing Guidelines
Writing Tests
python
def test_new_feature():
    # Arrange
    setup_data = "test"
    
    # Act
    result = function_under_test(setup_data)
    
    # Assert
    assert result == expected_value

def test_edge_case():
    # Test error conditions
    with pytest.raises(ExpectedError):
        function_under_test(invalid_input)
Test Structure
One assert per test when possible

Use descriptive test names

Test both success and failure paths

Mock external dependencies

Clean up test data

📝 Code Review Guidelines
What We Look For
Correctness: Does the code work as intended?

Clarity: Is the code easy to understand?

Testing: Are there adequate tests?

Documentation: Is the feature well-documented?

Performance: Any performance implications?

Security: Any security concerns?

Review Comments
Be constructive and specific

Suggest alternatives when possible

Focus on the code, not the person

Explain the "why" behind suggestions

🚀 Release Process
Versioning
We follow Semantic Versioning:

MAJOR version for incompatible API changes

MINOR version for new functionality

PATCH version for bug fixes

Release Checklist
All tests passing

Documentation updated

Changelog updated

Version bumped

Release notes prepared

Compatibility verified





## Tests
 
Run All Tests
bash
# Run complete test suite
python -m pytest tests/ -v

# Run with coverage report
pytest --cov=queuectl tests/ -v

# Run tests in parallel
pytest tests/ -n auto
Run Verification Script
bash
# Comprehensive integration test
python verify_all.py
📋 Test Suite Structure
text
tests/
├── test_basic.py           # Core functionality tests
├── test_cli.py            # CLI command tests
├── test_worker.py         # Worker process tests
├── test_storage.py        # Data persistence tests
├── test_dlq.py           # Dead Letter Queue tests
├── conftest.py           # Test configuration and fixtures
└── test_data/            # Test data files
🛠️ Test Environment Setup
Prerequisites
bash
# Install testing dependencies
pip install -e ".[dev]"

# Verify test dependencies
python -c "import pytest; print('Pytest OK')"
python -c "import coverage; print('Coverage OK')"
Test Database Setup
bash
# Tests automatically use isolated storage
# No manual setup required - each test uses temporary directories
🧩 Running Specific Tests
By Test File
bash
# Run specific test file
pytest tests/test_basic.py -v
pytest tests/test_dlq.py -v
pytest tests/test_worker.py -v
By Test Function
bash
# Run specific test function
pytest tests/test_basic.py::TestQueueSystem::test_cli_enqueue -v
pytest tests/test_dlq.py::TestDLQ::test_dlq_recovery -v
By Test Marker
bash
# Run tests with specific markers
pytest -m "unit" -v
pytest -m "integration" -v
pytest -m "slow" -v
By Test Name Pattern
bash
# Run tests matching name pattern
pytest -k "test_cli" -v
pytest -k "enqueue" -v
pytest -k "not slow" -v
📊 Test Coverage
Generate Coverage Reports
bash
# Terminal coverage report
pytest --cov=queuectl tests/ --cov-report=term

# HTML coverage report
pytest --cov=queuectl tests/ --cov-report=html

# XML coverage report (for CI)
pytest --cov=queuectl tests/ --cov-report=xml

# Missing lines report
pytest --cov=queuectl tests/ --cov-report=term-missing
View Coverage Reports
bash
# Open HTML report in browser
open htmlcov/index.html  # macOS
start htmlcov/index.html # Windows
xdg-open htmlcov/index.html # Linux
🔧 Test Configuration
pytest.ini Configuration
ini
[tool:pytest]
addopts = -v --tb=short
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
    cli: CLI command tests
Environment Variables for Testing
bash
# Set test-specific environment
export QUEUECTL_TEST_MODE=true
export QUEUECTL_TEST_STORAGE_PATH=/tmp/queuectl_test
🎯 Test Categories
Unit Tests
bash
# Fast, isolated tests
pytest -m "unit" -v

# Core component tests
pytest tests/test_basic.py -m "unit" -v
Integration Tests
bash
# End-to-end functionality tests
pytest -m "integration" -v

# CLI integration tests
pytest tests/test_cli.py -m "integration" -v
CLI Command Tests
bash
# Test all CLI commands
pytest -m "cli" -v

# Specific command tests
pytest tests/test_cli.py -k "enqueue" -v
🧪 Manual Testing Procedures
1. Basic Functionality Test
bash
# Clean start
rm -rf queuectl_data

# Test job lifecycle
queuectl enqueue "echo 'test job'"
queuectl list
queuectl start --count 1 --timeout 5
queuectl list --state completed
2. DLQ Recovery Test
bash
# Test failure handling
queuectl enqueue "invalid_command" --max-retries 1
queuectl start --count 1 --timeout 5
queuectl dlq list
queuectl dlq retry <job_id>
queuectl list --state pending
3. Configuration Test
bash
# Test config management
queuectl config
queuectl config --key max_retries --value 5
queuectl config --key backoff_base --value 3
queuectl config
4. Persistence Test
bash
# Test data persistence across sessions
queuectl enqueue "sleep 1"
queuectl enqueue "echo 'persistence test'"
# Restart application or new terminal
queuectl list  # Should show same jobs
🔄 Continuous Integration Tests
Local CI Simulation
bash
# Run all CI checks locally
./scripts/run_ci_checks.sh

# Or manually run each step
pytest tests/ -v --cov=queuectl --cov-fail-under=90
black queuectl/ tests/ --check
flake8 queuectl/ tests/
isort queuectl/ tests/ --check-only
CI Test Matrix
Python Versions: 3.8, 3.9, 3.10, 3.11

Operating Systems: Ubuntu, Windows, macOS

Storage Backends: JSON file system

🐛 Debugging Tests
Verbose Test Output
bash
# Very verbose output
pytest tests/ -v -s

# Show print statements
pytest tests/ -s

# Debug on failure
pytest tests/ --pdb
Test Isolation
bash
# Run tests in random order to detect interdependencies
pytest tests/ --random-order

# Run tests in specific order
pytest tests/ --tb=long -x  # Stop on first failure
Memory Leak Detection
bash
# Check for test leaks
pytest tests/ --show-leaks
📝 Writing New Tests
Test Template
python
import pytest
from queuectl.core.queue import QueueManager

class TestNewFeature:
    def test_feature_success(self, temp_storage):
        """Test successful feature execution."""
        # Setup
        queue = QueueManager(storage_path=temp_storage)
        
        # Exercise
        result = queue.new_feature()
        
        # Verify
        assert result is True
        assert queue.has_feature() is True
    
    def test_feature_failure(self, temp_storage):
        """Test feature failure conditions."""
        queue = QueueManager(storage_path=temp_storage)
        
        with pytest.raises(ExpectedError):
            queue.new_feature(invalid_input)
Test Fixtures
python
# Use existing fixtures from conftest.py
def test_with_fixtures(temp_storage, sample_job, mock_worker):
    # temp_storage: Isolated storage directory
    # sample_job: Pre-configured job object
    # mock_worker: Mock worker for testing
    pass
Best Practices for Test Writing
One Assert Per Test: Focus on single responsibility

Descriptive Names: Clear test purpose from name

Test Edge Cases: Include boundary conditions

Mock External Dependencies: Isolate unit under test

Clean Up: Ensure tests don't leave side effects

🎰 Test Data Management
Creating Test Data
bash
# Generate test jobs
python tests/utils/generate_test_data.py

# Create specific test scenarios
python tests/utils/create_failure_scenario.py
Test Data Files
json
// tests/test_data/sample_jobs.json
{
  "valid_jobs": [
    {"command": "echo 'test'", "max_retries": 3},
    {"command": "sleep 1", "max_retries": 1}
  ],
  "invalid_jobs": [
    {"command": "invalid_command", "max_retries": 2}
  ]
}
🔍 Performance Testing
Benchmark Tests
bash
# Run performance tests
pytest tests/benchmarks/ -v

# Time specific operations
python -m timeit -s "from queuectl.core.queue import QueueManager" "QueueManager().enqueue('echo test')"
Load Testing
bash
# Test with many concurrent jobs
python tests/load_test.py --jobs 100 --workers 5

# Stress test storage
python tests/stress_test.py --operations 1000
🚨 Common Test Issues & Solutions
Issue: Test Interference
bash
# Solution: Use isolated storage
export QUEUECTL_TEST_STORAGE_PATH=$(mktemp -d)
pytest tests/ -v
Issue: Hanging Tests
bash
# Solution: Add timeout
pytest tests/ --timeout=30

# Or debug hanging test
pytest tests/test_specific.py -v -s --pdb
Issue: Platform-Specific Failures
bash
# Solution: Use conditional skipping
@pytest.mark.skipif(sys.platform == "win32", reason="Windows-specific issue")
def test_unix_specific_feature():
    pass
Issue: Flaky Tests
bash
# Solution: Retry flaky tests
pytest tests/ --reruns 3 --reruns-delay 1





## GitHub

<a href="https://github.com/AshwanthGpn"><strong>AshwanthGpn</a></strong>






## Contact

Feel free to reach out to me on my email:
ashwanthgpn@gmail.com





## License

[![License](https://img.shields.io/static/v1?label=Licence&message=MIT&color=blue)](https://opensource.org/license/MIT)


