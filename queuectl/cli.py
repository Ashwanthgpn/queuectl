#!/usr/bin/env python3
import click
import json
import time
import logging
from tabulate import tabulate

from queuectl.core.storage import JobStorage
from queuectl.core.queue import JobQueue
from queuectl.core.worker import WorkerManager
from queuectl.utils.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@click.group()
@click.option('--storage-path', default='queuectl_data', help='Path to storage directory')
@click.pass_context
def cli(ctx, storage_path):
    """QueueCTL - Background Job Queue System"""
    ctx.ensure_object(dict)
    ctx.obj['storage'] = JobStorage(storage_path)
    ctx.obj['queue'] = JobQueue(ctx.obj['storage'])
    ctx.obj['config'] = Config(ctx.obj['storage'])
    ctx.obj['worker_manager'] = None

@cli.command()
@click.argument('command')
@click.option('--max-retries', default=3, help='Maximum retry attempts')
@click.option('--timeout', default=30, help='Job timeout in seconds')
@click.option('--backoff-base', default=2, help='Exponential backoff base')
@click.pass_context
def enqueue(ctx, command, max_retries, timeout, backoff_base):
    """Enqueue a new job"""
    job = ctx.obj['queue'].enqueue(
        command,
        max_retries=max_retries,
        timeout=timeout,
        backoff_base=backoff_base
    )
    
    if job:
        click.echo(f"Job enqueued successfully!")
        click.echo(f"   ID: {job.id}")
        click.echo(f"   Command: {job.command}")
    else:
        click.echo("Failed to enqueue job")

@cli.command()
@click.option('--count', default=1, help='Number of workers to start')
@click.pass_context
def start(ctx, count):
    """Start worker processes"""
    ctx.obj['worker_manager'] = WorkerManager(ctx.obj['queue'])
    ctx.obj['worker_manager'].start_workers(count)
    click.echo(f"Started {count} worker(s)")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        click.echo("\nShutting down workers...")
        ctx.obj['worker_manager'].stop_workers()

@cli.command()
@click.pass_context
def stop(ctx):
    """Stop all worker processes"""
    if ctx.obj['worker_manager']:
        ctx.obj['worker_manager'].stop_workers()
        click.echo("All workers stopped")
    else:
        click.echo("No workers running")

@cli.command()
@click.pass_context  
def status(ctx):
    """Show system status"""
    stats = ctx.obj['queue'].get_stats()
    
    click.echo("QueueCTL System Status")
    click.echo("=" * 40)
    
    table_data = [
        ["Pending", stats["pending"]],
        ["Processing", stats["processing"]],
        ["Completed", stats["completed"]],
        ["Failed", stats["failed"]],
        ["Dead (DLQ)", stats["dead"]],
        ["Total", stats["total_jobs"]]
    ]
    click.echo(tabulate(table_data, tablefmt="simple"))
    
    if ctx.obj['worker_manager']:
        worker_stats = ctx.obj['worker_manager'].get_worker_stats()
        if worker_stats:
            click.echo(f"\nActive Workers: {len(worker_stats)}")
            for ws in worker_stats:
                status = "Running" if ws['running'] else "Stopped"
                click.echo(f"  {ws['worker_id']}: {status}")
        else:
            click.echo("\nNo active workers")
    else:
        click.echo("\nNo worker manager running")

@cli.command(name='list')
@click.option('--state', type=click.Choice(['pending', 'processing', 'completed', 'failed', 'dead']))
@click.option('--limit', default=10, help='Limit number of jobs to show')
@click.pass_context
def list_jobs(ctx, state, limit):
    """List jobs"""
    try:
        from queuectl.core.job import JobState
        
        all_jobs = ctx.obj['queue'].storage.get_all_jobs()
        
        if state:
            jobs = [job for job in all_jobs.values() if job.state.value == state]
        else:
            job_list = list(all_jobs.values())  # Use different variable name
        
        job_list.sort(key=lambda x: x.created_at, reverse=True)
        job_list = job_list[:limit]
        
        if not job_list:
            click.echo("No jobs found")
            return
        
        table_data = []
        for job in job_list:
            command_text = str(job.command)
            if len(command_text) > 30:
                command_display = command_text[:30] + "..."
            else:
                command_display = command_text
            
            table_data.append([
                str(job.id)[:8],
                command_display,
                str(job.state.value),
                job.attempts,
                job.max_retries,
            ])
        
        headers = ["ID", "Command", "State", "Attempts", "Max Retries"]
        click.echo(tabulate(table_data, headers=headers, tablefmt="simple"))
        
    except Exception as e:
        click.echo(f"Error listing jobs: {e}")

@cli.group()
def dlq():
    """Manage Dead Letter Queue"""
    pass

@dlq.command(name='list')
@click.pass_context
def dlq_list(ctx):
    """List jobs in Dead Letter Queue"""
    try:
        from queuectl.core.job import JobState
        
        dlq_jobs = ctx.obj['queue'].storage.get_jobs_by_state(JobState.DEAD)
        
        if not dlq_jobs:
            click.echo("No jobs in Dead Letter Queue")
            return
        
        table_data = []
        for job in dlq_jobs:
            command_text = str(job.command)
            if len(command_text) > 40:
                command_display = command_text[:40] + "..."
            else:
                command_display = command_text
            
            error_text = str(job.last_error) if job.last_error else "N/A"
            if len(error_text) > 50:
                error_display = error_text[:50] + "..."
            else:
                error_display = error_text
            
            table_data.append([
                str(job.id)[:8],
                command_display,
                job.attempts,
                error_display,
            ])
        
        headers = ["ID", "Command", "Attempts", "Last Error"]
        click.echo(tabulate(table_data, headers=headers, tablefmt="simple"))
        
    except Exception as e:
        click.echo(f"Error listing DLQ jobs: {e}")

@dlq.command()
@click.argument('job_id')
@click.pass_context
def retry(ctx, job_id):
    """Retry a job from Dead Letter Queue"""
    if ctx.obj['queue'].retry_dlq_job(job_id):
        click.echo(f"Job {job_id} moved from DLQ to pending queue")
    else:
        click.echo(f"Failed to retry job {job_id}")

@cli.command()
@click.option('--key', help='Configuration key')
@click.option('--value', help='Configuration value')
@click.option('--reset', is_flag=True, help='Reset to defaults')
@click.pass_context
def config(ctx, key, value, reset):
    """Manage system configuration"""
    if reset:
        ctx.obj['config'].reset()
        click.echo("Configuration reset to defaults")
    elif key and value:
        try:
            if value.isdigit():
                value = int(value)
            elif value.lower() in ('true', 'false'):
                value = value.lower() == 'true'
        except:
            pass
        
        if ctx.obj['config'].set(key, value):
            click.echo(f"Set {key} = {value}")
        else:
            click.echo(f"Failed to set {key}")
    elif key:
        value = ctx.obj['config'].get(key)
        click.echo(f"{key} = {value}")
    else:
        for k, v in ctx.obj['config'].get_all().items():
            click.echo(f"{k} = {v}")

if __name__ == '__main__':
    cli()