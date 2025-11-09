import unittest
import tempfile
import os
import subprocess
import shutil


class TestQueueSystem(unittest.TestCase):
    def setUp(self):
        """Create an isolated temp directory for each test"""
        self.temp_dir = tempfile.mkdtemp()
        self.storage_path = os.path.join(self.temp_dir, "test_data")

    def tearDown(self):
        """Clean up after test"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _run_cli(self, *args):
        """Helper: run queuectl CLI command and capture all output"""
        result = subprocess.run(
            ['queuectl', '--storage-path', self.storage_path, *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # merge stderr → stdout (Click prints to stderr sometimes)
            text=True
        )
        print(f"\n[CMD] queuectl {' '.join(args)}")
        print("[OUTPUT]:", result.stdout)
        return result

    def test_cli_enqueue(self):
        """✅ Test that enqueue command works"""
        result = self._run_cli('enqueue', 'echo "hello world"')
        self.assertEqual(result.returncode, 0)
        self.assertIn('enqueued successfully', result.stdout.lower())

    def test_job_persistence(self):
        """✅ Test job persists and shows in status"""
        # Enqueue one job
        enqueue_result = self._run_cli('enqueue', 'sleep 1')
        self.assertIn('enqueued successfully', enqueue_result.stdout.lower())

        # Check status
        status_result = self._run_cli('status')
        self.assertIn('pending', status_result.stdout.lower())
        self.assertIn('1', status_result.stdout)

    def test_dlq_functionality(self):
        """✅ Test DLQ (Dead Letter Queue) listing"""
        # Enqueue a job that fails
        enqueue_result = self._run_cli('enqueue', 'invalid_command_xyz', '--max-retries', '1')
        self.assertIn('enqueued successfully', enqueue_result.stdout.lower())

        # Check DLQ list (should initially be empty)
        dlq_result = self._run_cli('dlq', 'list')
        self.assertIn('no jobs in dead letter queue', dlq_result.stdout.lower())


if __name__ == '__main__':
    unittest.main()
