#!/usr/bin/env python3
"""Command Tool SDK - A fun admin command-line tool"""

import click
import psutil
import platform
import os
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


class AdminTool:
    """Admin command tool class"""
    
    @staticmethod
    def check_admin():
        """Check if running with admin privileges"""
        try:
            is_admin = os.getuid() == 0 if hasattr(os, 'getuid') else (
                os.getenv('USERNAME') is not None and 
                'admin' in os.popen('whoami /groups 2>nul').read().lower()
            )
            return is_admin
        except:
            return False
    
    @staticmethod
    def get_system_info():
        """Get system information"""
        return {
            'hostname': platform.node(),
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'python_version': platform.python_version(),
            'cpu_count': psutil.cpu_count(),
            'total_memory': f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
            'available_memory': f"{psutil.virtual_memory().available / (1024**3):.2f} GB",
        }
    
    @staticmethod
    def get_running_processes():
        """Get list of running processes"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'status']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'status': proc.info['status']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return processes


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """🎮 Command Tool SDK - Admin Command-line Tool"""
    pass


@cli.command()
def status():
    """Show tool status"""
    click.clear()
    click.echo(f"{Fore.CYAN}{'='*50}")
    click.echo(f"{Fore.GREEN}Command Tool SDK - Status Report{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    click.echo()
    
    if AdminTool.check_admin():
        click.echo(f"{Fore.GREEN}✓ Running with admin privileges{Style.RESET_ALL}")
    else:
        click.echo(f"{Fore.YELLOW}⚠ Running without admin privileges{Style.RESET_ALL}")
    
    click.echo(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    click.echo(f"Tool Version: 1.0.0")
    click.echo()


@cli.command()
def system_info():
    """Display system information"""
    click.clear()
    click.echo(f"{Fore.CYAN}{'='*50}")
    click.echo(f"{Fore.GREEN}System Information{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    click.echo()
    
    info = AdminTool.get_system_info()
    for key, value in info.items():
        display_key = key.replace('_', ' ').title()
        click.echo(f"{Fore.YELLOW}{display_key:.<30}{Style.RESET_ALL} {value}")
    click.echo()


@cli.command()
def list_processes():
    """List running processes"""
    click.clear()
    click.echo(f"{Fore.CYAN}{'='*50}")
    click.echo(f"{Fore.GREEN}Running Processes{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    click.echo()
    
    processes = AdminTool.get_running_processes()
    
    # Display header
    click.echo(f"{Fore.YELLOW}{'PID':>10} {'Name':<30} {'Status':<15}{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}{'-'*55}{Style.RESET_ALL}")
    
    # Display processes (limited to first 20)
    for proc in processes[:20]:
        click.echo(f"{proc['pid']:>10} {proc['name']:<30} {proc['status']:<15}")
    
    if len(processes) > 20:
        click.echo(f"{Fore.YELLOW}... and {len(processes) - 20} more processes{Style.RESET_ALL}")
    
    click.echo()
    click.echo(f"{Fore.GREEN}Total processes: {len(processes)}{Style.RESET_ALL}")
    click.echo()


@cli.command()
def cpu_usage():
    """Show CPU usage"""
    click.clear()
    click.echo(f"{Fore.CYAN}{'='*50}")
    click.echo(f"{Fore.GREEN}CPU Usage{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    click.echo()
    
    cpu_percent = psutil.cpu_percent(interval=1)
    click.echo(f"Overall CPU Usage: {Fore.YELLOW}{cpu_percent}%{Style.RESET_ALL}")
    click.echo()
    
    # Per-core CPU usage
    per_cpu = psutil.cpu_percent(interval=1, percpu=True)
    click.echo("Per-Core CPU Usage:")
    for i, percent in enumerate(per_cpu):
        bar = '█' * int(percent / 5) + '░' * (20 - int(percent / 5))
        click.echo(f"  Core {i}: {Fore.CYAN}{bar}{Style.RESET_ALL} {percent}%")
    click.echo()


@cli.command()
def memory_info():
    """Show memory information"""
    click.clear()
    click.echo(f"{Fore.CYAN}{'='*50}")
    click.echo(f"{Fore.GREEN}Memory Information{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    click.echo()
    
    mem = psutil.virtual_memory()
    
    total_gb = mem.total / (1024**3)
    used_gb = mem.used / (1024**3)
    available_gb = mem.available / (1024**3)
    percent = mem.percent
    
    click.echo(f"Total:     {Fore.YELLOW}{total_gb:.2f} GB{Style.RESET_ALL}")
    click.echo(f"Used:      {Fore.RED}{used_gb:.2f} GB{Style.RESET_ALL}")
    click.echo(f"Available: {Fore.GREEN}{available_gb:.2f} GB{Style.RESET_ALL}")
    click.echo(f"Percent:   {Fore.YELLOW}{percent}%{Style.RESET_ALL}")
    click.echo()
    
    # Memory bar
    bar_length = 30
    filled = int((percent / 100) * bar_length)
    bar = '█' * filled + '░' * (bar_length - filled)
    click.echo(f"Memory: {Fore.CYAN}{bar}{Style.RESET_ALL} {percent}%")
    click.echo()


if __name__ == '__main__':
    cli()
