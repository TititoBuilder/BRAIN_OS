---
knowledge_os_machine_key: docker_fundamentals
knowledge_os_domain: Cloud & DevOps
knowledge_os_status: Not Started
knowledge_os_score: 0
knowledge_os_priority: High
---
# Docker Fundamentals

## What It Is
Docker packages an application together with everything it needs to run, its code,
its dependencies, its system libraries, into a single unit called a container that
runs the same way on any machine. It solves the oldest problem in deployment: it
works on my machine but breaks on the server. With Docker, your machine and the
server run the identical packaged environment.

## How It Works
You write a Dockerfile, a recipe that says start from this base, copy in this code,
install these dependencies, run this command. Building it produces an image, a
frozen snapshot of that whole environment. Running an image produces a container, a
live isolated instance of it. The container shares the host's operating system
kernel but has its own isolated filesystem, dependencies, and process space, which
is why it is far lighter than a full virtual machine yet still cleanly separated
from everything else on the host. The same image runs identically on your laptop,
a teammate's machine, or a cloud server.

## Why It Matters
Docker makes environments reproducible, which removes a whole category of
deployment bugs caused by mismatched versions and missing system libraries between
development and production. It is the foundation under modern deployment: cloud
platforms run containers, and the consistency means what you tested is exactly what
ships. It connects directly to the dependency-isolation discipline you already
practice with virtual environments, Docker extends that same idea from just Python
packages to the entire operating-system-level environment around the app.

## The Pattern
Package the whole environment, not just the code, so it runs identically
everywhere. A Dockerfile is the recipe, the image is the frozen build, the
container is the running instance. Reproducibility kills works-on-my-machine.
