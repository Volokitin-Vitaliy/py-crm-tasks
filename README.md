# Task Manager for IT Team

This is a web application designed to help a team of developers,
designers, project managers, and QA specialists effectively collaborate
on product development by managing their tasks.

### Project Description

Each team member can:

- create new tasks,

- assign tasks to other team members,

- mark tasks as completed (preferably before the deadline).

### Key Features

- Management of employee positions (e.g., developer, designer, tester).

- User registration with assigned positions.

- Task categorization by type.

- Setting task priority levels: urgent, high, medium, and low.

- Ability to set deadlines for tasks.

- Assigning a single task to multiple employees.

- Viewing completed and incomplete tasks separately for each worker.

### Models Overview

**Position** - employee job titles.

**Worker** - users with assigned positions (inherits from AbstractUser).

**TaskType** - categories/types of tasks.

**Task** - tasks with description, deadline, completion status, priority, type, and assignees.