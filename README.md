🚀 Quick Start
Prerequisites
Python 3.8+

pip installed

Installation
bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/queuectl.git
cd queuectl

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -e .

# Verify installation
queuectl --help
⚙️ Usage Examples
📥 Enqueue Jobs
bash
$ queuectl enqueue "echo 'Hello World'"
Job enqueued successfully!
   ID: d6c5097f-ecc8-4a44-89d7-fe88f965497c
   Command: echo 'Hello World'

$ queuectl enqueue "sleep 5" --max-retries 3
Job enqueued successfully!
   ID: b9b6ec38-52a6-4325-ad91-ccc5bc5b5834
   Command: sleep 5

$ queuectl enqueue "invalid_command" --max-retries 1
Job enqueued successfully!
   ID: 08232c92-a58f-4419-a31f-feecc1112dfe
   Command: invalid_command
👥 Manage Workers
bash
$ queuectl start --count 2 --timeout 10
Started 2 worker(s) for 10 seconds
Workers will auto-stop...

2025-11-09 17:01:54,268 - queuectl.core.worker - INFO - Worker worker-1 started
2025-11-09 17:01:54,269 - queuectl.core.worker - INFO - Worker worker-2 started

$ queuectl stop
Stopping all workers...
📊 Monitor System
bash
$ queuectl status
QueueCTL System Status
========================================
Pending     1
Processing  0
Completed   2
Failed      0
Dead (DLQ)  0
Total       3
========================================

No worker manager running

$ queuectl list --state pending
ID        Command          State      Attempts    Max Retries
--------  ---------------  -------  ----------  -------------
08232c92  invalid_command  pending           0              1

$ queuectl list --state completed
ID        Command             State        Attempts    Max Retries
--------  ------------------  ---------  ----------  -------------
d6c5097f  echo 'Hello World'  completed           1              3
b9b6ec38  sleep 2             completed           1              3
⚠️ Dead Letter Queue (DLQ) Management
bash
$ queuectl dlq list
ID                                    Command            Attempts  Last Error
------------------------------------  ---------------  ----------  -----------------------------------------------------
08232c92-a58f-4419-a31f-feecc1112dfe  invalid_command           1  Exit code 1: 'invalid_command' is not recognized a...

$ queuectl dlq retry 08232c92-a58f-4419-a31f-feecc1112dfe
Job 08232c92-a58f-4419-a31f-feecc1112dfe moved from DLQ to pending queue

$ queuectl list --state pending
ID        Command          State      Attempts    Max Retries
--------  ---------------  -------  ----------  -------------
08232c92  invalid_command  pending           0              1
⚙️ Configuration Management
bash
$ queuectl config
max_retries = 3
backoff_base = 2
job_timeout = 30
worker_count = 1
storage_path = queuectl_data
log_level = INFO

$ queuectl config --key max_retries --value 5
Set max_retries = 5

$ queuectl config --key backoff_base --value 3
Set backoff_base = 3

$ queuectl config
max_retries = 5
backoff_base = 3
job_timeout = 30
worker_count = 1
storage_path = queuectl_data
log_level = INFO
🧠 Architecture Overview
🧩 Components
CLI Layer - Handles user input and command parsing using Click library

Queue Manager - Coordinates job lifecycle and state transitions

Storage Layer - JSON-based persistent storage for job data

Worker System - Multi-process job execution with exponential backoff

Dead Letter Queue - Stores permanently failed jobs for recovery

🔄 Job Lifecycle
text
pending → processing → completed
                |
                → failed → (retry) → pending
                        |
                        → dead (DLQ)
📋 Job Specification
json
{
    "id": "unique-uuid",
    "command": "echo 'Hello World'",
    "state": "pending|processing|completed|failed|dead",
    "attempts": 0,
    "max_retries": 3,
    "created_at": "2025-11-04T10:30:00Z",
    "updated_at": "2025-11-04T10:30:00Z"
}
⚖️ Assumptions & Trade-offs
🎯 Design Decisions
Persistence: JSON-based storage chosen for simplicity and portability

Concurrency: Multi-process model avoids GIL contention and provides isolation

Resilience: Exponential backoff balances reliability with resource efficiency

Configuration: CLI-based configuration for ease of use and portability

Scalability: Optimized for local/medium-scale workloads

⚠️ Known Limitations
File locking issues on Windows under heavy concurrent access

Not designed for distributed systems (single-node only)

JSON storage may not scale to millions of jobs

🧪 Testing
✅ Comprehensive Verification
bash
$ python verify_all.py
COMPREHENSIVE QUEUECTL VERIFICATION
============================================================
Testing: Job Enqueue - PASS
Testing: Status Command - PASS  
Testing: List Command - PASS
Testing: Configuration Management - PASS
Testing: DLQ Commands - PASS
Testing: Multiple Job Types - PASS
============================================================
ALL FEATURES VERIFIED SUCCESSFULLY!
🧩 Unit Tests
bash
$ python -m pytest tests/ -v
================================ test session starts ================================
platform win32 -- Python 3.14.0, pytest-8.4.2, pluggy-1.6.0
collected 3 items

tests/test_basic.py::TestQueueSystem::test_cli_enqueue PASSED [33%]
tests/test_basic.py::TestQueueSystem::test_dlq_functionality PASSED [66%]
tests/test_basic.py::TestQueueSystem::test_job_persistence PASSED [100%]

================================= 3 passed in 2.06s =================================
🔍 Complete Workflow Demo
bash
# Clean start
$ rmdir /s queuectl_data 2>nul

# Enqueue test jobs
$ queuectl enqueue "sleep 2"
Job enqueued successfully!
   ID: b9b6ec38-52a6-4325-ad91-ccc5bc5b5834
   Command: sleep 2

$ queuectl enqueue "echo 'Hello World'"
Job enqueued successfully!
   ID: d6c5097f-ecc8-4a44-89d7-fe88f965497c
   Command: echo 'Hello World'

$ queuectl enqueue "invalid_command" --max-retries 1
Job enqueued successfully!
   ID: 08232c92-a58f-4419-a31f-feecc1112dfe
   Command: invalid_command

# Process jobs
$ queuectl start --count 2 --timeout 10
Started 2 worker(s) for 10 seconds

# Check results
$ queuectl status
QueueCTL System Status
========================================
Pending     0
Processing  0
Completed   2
Failed      0
Dead (DLQ)  1
Total       3
========================================

# Recover from DLQ
$ queuectl dlq retry 08232c92-a58f-4419-a31f-feecc1112dfe
Job 08232c92-a58f-4419-a31f-feecc1112dfe moved from DLQ to pending queue


📁 Project Structure
text
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


💡 Future Enhancements
🚀 Planned Features
Distributed backend (Redis/RabbitMQ)

Web dashboard for real-time monitoring

Priority-based job queues

Job timeout handling

Scheduled/delayed jobs (run_at parameter)

Advanced metrics and execution statistics

Rate limiting and throttling mechanisms



🔧 Immediate Improvements
Enhanced file locking for Windows compatibility

Job output capture and logging

Better error handling and user feedback

Performance optimizations for large queues



🐛 Troubleshooting
❌ DLQ Retry Issues
bash
# ❌ Wrong - using short ID
$ queuectl dlq retry 08232c92
Failed to retry job 08232c92

# ✅ Correct - using full UUID
$ queuectl dlq retry 08232c92-a58f-4419-a31f-feecc1112dfe
Job 08232c92-a58f-4419-a31f-feecc1112dfe moved from DLQ to pending queue
🔒 File Locking Issues
bash
# If you see file locking errors on Windows:
2025-11-09 17:01:54,274 - queuectl.core.storage - ERROR - Failed to get all jobs: [WinError 32] The process cannot access the file...

# Solution: Reduce worker count or wait for auto-recovery
$ queuectl start --count 1
📦 Installation Issues
bash
# If queuectl command not found:
$ pip install -e .
$ queuectl --help


👨‍💻 Author
Ashwanth G P N
Senior Software Engineer


