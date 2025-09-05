#!/usr/bin/env python
import os
from datetime import datetime, timedelta

import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_manager.settings")
django.setup()

from django.contrib.auth.models import User

from app_models.models.constant import TaskStatus
from app_models.models.project import Project
from app_models.models.task import Task
from app_models.models.time_entry import TimeEntry


def create_test_data():
    print("Loading test data...")

    # Create test users
    users_data = [
        {
            "username": "john_dev",
            "email": "john@company.com",
            "first_name": "John",
            "last_name": "Developer",
        },
        {
            "username": "sarah_pm",
            "email": "sarah@company.com",
            "first_name": "Sarah",
            "last_name": "Manager",
        },
        {
            "username": "mike_designer",
            "email": "mike@company.com",
            "first_name": "Mike",
            "last_name": "Designer",
        },
    ]

    users = {}
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data["username"], defaults=user_data
        )
        if created:
            user.set_password("password123")
            user.save()
            print(f"✓ Created user: {user.username}")
        else:
            print(f"✓ User already exists: {user.username}")
        users[user_data["username"]] = user

    # Create test projects with realistic data
    projects_data = [
        {
            "title": "E-commerce Platform",
            "description": "Complete online store with payment integration, inventory management, and admin dashboard",
            "owner": "sarah_pm",
        },
        {
            "title": "Mobile Banking App",
            "description": "Secure mobile application for banking operations with biometric authentication",
            "owner": "john_dev",
        },
        {
            "title": "HR Management System",
            "description": "Internal tool for employee management, payroll, and performance tracking",
            "owner": "sarah_pm",
        },
    ]

    projects = {}
    for project_data in projects_data:
        project, created = Project.objects.get_or_create(
            title=project_data["title"],
            defaults={
                "description": project_data["description"],
                "owner": users[project_data["owner"]],
            },
        )
        if created:
            print(f"✓ Created project: {project.title}")
        else:
            print(f"✓ Project already exists: {project.title}")
        projects[project_data["title"]] = project

    # Create comprehensive tasks with realistic workflow
    tasks_data = [
        # E-commerce Platform tasks
        {
            "title": "Project Setup & Architecture",
            "project": "E-commerce Platform",
            "status": TaskStatus.DONE,
            "estimated_time": 480,
            "spent_time": 450,
        },
        {
            "title": "User Authentication System",
            "project": "E-commerce Platform",
            "status": TaskStatus.DONE,
            "estimated_time": 360,
            "spent_time": 380,
        },
        {
            "title": "Product Catalog Management",
            "project": "E-commerce Platform",
            "status": TaskStatus.IN_PROGRESS,
            "estimated_time": 720,
            "spent_time": 240,
        },
        {
            "title": "Shopping Cart & Checkout",
            "project": "E-commerce Platform",
            "status": TaskStatus.TODO,
            "estimated_time": 600,
            "spent_time": 0,
        },
        {
            "title": "Payment Gateway Integration",
            "project": "E-commerce Platform",
            "status": TaskStatus.TODO,
            "estimated_time": 480,
            "spent_time": 0,
        },
        {
            "title": "Admin Dashboard",
            "project": "E-commerce Platform",
            "status": TaskStatus.TODO,
            "estimated_time": 540,
            "spent_time": 0,
        },
        # Mobile Banking App tasks
        {
            "title": "Security Architecture Design",
            "project": "Mobile Banking App",
            "status": TaskStatus.DONE,
            "estimated_time": 600,
            "spent_time": 580,
        },
        {
            "title": "API Development",
            "project": "Mobile Banking App",
            "status": TaskStatus.IN_PROGRESS,
            "estimated_time": 900,
            "spent_time": 420,
        },
        {
            "title": "Biometric Authentication",
            "project": "Mobile Banking App",
            "status": TaskStatus.IN_PROGRESS,
            "estimated_time": 480,
            "spent_time": 120,
        },
        {
            "title": "Transaction Processing",
            "project": "Mobile Banking App",
            "status": TaskStatus.TODO,
            "estimated_time": 720,
            "spent_time": 0,
        },
        {
            "title": "Security Testing",
            "project": "Mobile Banking App",
            "status": TaskStatus.TODO,
            "estimated_time": 360,
            "spent_time": 0,
        },
        # HR Management System tasks
        {
            "title": "Database Schema Design",
            "project": "HR Management System",
            "status": TaskStatus.DONE,
            "estimated_time": 240,
            "spent_time": 260,
        },
        {
            "title": "Employee Profile Management",
            "project": "HR Management System",
            "status": TaskStatus.DONE,
            "estimated_time": 480,
            "spent_time": 465,
        },
        {
            "title": "Payroll Calculation Module",
            "project": "HR Management System",
            "status": TaskStatus.IN_PROGRESS,
            "estimated_time": 600,
            "spent_time": 180,
        },
        {
            "title": "Performance Review System",
            "project": "HR Management System",
            "status": TaskStatus.TODO,
            "estimated_time": 720,
            "spent_time": 0,
        },
        {
            "title": "Reporting & Analytics",
            "project": "HR Management System",
            "status": TaskStatus.TODO,
            "estimated_time": 480,
            "spent_time": 0,
        },
    ]

    tasks = {}
    for task_data in tasks_data:
        project = projects[task_data["project"]]
        task, created = Task.objects.get_or_create(
            title=task_data["title"],
            project=project,
            defaults={
                "description": f"Detailed implementation of {task_data['title']} for {task_data['project']}",
                "status": task_data["status"],
                "estimated_time": task_data["estimated_time"],
                "spent_time": task_data["spent_time"],
            },
        )
        if created:
            print(f"✓ Created task: {task.title}")
        else:
            print(f"✓ Task already exists: {task.title}")
        tasks[task_data["title"]] = task

    # Create realistic time entries
    time_entries_data = [
        # Completed tasks - multiple sessions
        {
            "task": "Project Setup & Architecture",
            "user": "john_dev",
            "sessions": [
                {"start_offset_days": 10, "duration": 240},
                {"start_offset_days": 9, "duration": 210},
            ],
        },
        {
            "task": "User Authentication System",
            "user": "john_dev",
            "sessions": [
                {"start_offset_days": 8, "duration": 180},
                {"start_offset_days": 7, "duration": 200},
            ],
        },
        {
            "task": "Security Architecture Design",
            "user": "john_dev",
            "sessions": [
                {"start_offset_days": 6, "duration": 300},
                {"start_offset_days": 5, "duration": 280},
            ],
        },
        {
            "task": "Database Schema Design",
            "user": "mike_designer",
            "sessions": [{"start_offset_days": 4, "duration": 260}],
        },
        {
            "task": "Employee Profile Management",
            "user": "mike_designer",
            "sessions": [
                {"start_offset_days": 3, "duration": 240},
                {"start_offset_days": 2, "duration": 225},
            ],
        },
        # In-progress tasks - active sessions
        {
            "task": "Product Catalog Management",
            "user": "john_dev",
            "sessions": [{"start_offset_days": 1, "duration": 240, "active": False}],
        },
        {
            "task": "API Development",
            "user": "john_dev",
            "sessions": [
                {"start_offset_days": 2, "duration": 300, "active": False},
                {
                    "start_offset_days": 0,
                    "duration": 120,
                    "active": True,
                },  # Currently active
            ],
        },
        {
            "task": "Biometric Authentication",
            "user": "mike_designer",
            "sessions": [{"start_offset_days": 1, "duration": 120, "active": False}],
        },
        {
            "task": "Payroll Calculation Module",
            "user": "sarah_pm",
            "sessions": [{"start_offset_days": 0, "duration": 180, "active": False}],
        },
    ]

    for entry_data in time_entries_data:
        task = tasks[entry_data["task"]]
        user = users[entry_data["user"]]

        for session in entry_data["sessions"]:
            start_time = datetime.now() - timedelta(
                days=session["start_offset_days"], hours=2
            )
            is_active = session.get("active", False)
            end_time = (
                None if is_active else start_time + timedelta(minutes=session["duration"])
            )

            # Check if this specific time entry already exists
            existing_entry = TimeEntry.objects.filter(
                task=task,
                user=user,
                start_time__date=start_time.date(),
                is_active=is_active,
            ).first()

            if not existing_entry:
                TimeEntry.objects.create(
                    user=user,
                    task=task,
                    start_time=start_time,
                    end_time=end_time,
                    duration=session["duration"] if not is_active else None,
                    is_active=is_active,
                )
                status = "Active" if is_active else "Completed"
                print(
                    f"✓ Created {status.lower()} time entry: {task.title} ({user.username})"
                )

    print("\n✅ Test data loaded successfully!")
    print(f"Users: {User.objects.count()}")
    print(f"Projects: {Project.objects.count()}")
    print(f"Tasks: {Task.objects.count()}")
    print(f"Time entries: {TimeEntry.objects.count()}")
    print(f"Active timers: {TimeEntry.objects.filter(is_active=True).count()}")


if __name__ == "__main__":
    create_test_data()
