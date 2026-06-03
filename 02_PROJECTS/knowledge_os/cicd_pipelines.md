---
knowledge_os_machine_key: cicd_pipelines
knowledge_os_domain: Cloud & DevOps
knowledge_os_status: Not Started
knowledge_os_score: 0
knowledge_os_priority: High
---
# CI/CD Pipelines

## What It Is
CI/CD is the practice of automating the path from code change to running software.
CI, continuous integration, means every change is automatically built and tested.
CD, continuous delivery or deployment, means changes that pass are automatically
prepared for or pushed to production. Together they form a pipeline that takes a
commit and carries it through checks all the way toward release without manual
steps.

## How It Works
You define the pipeline as a sequence of stages triggered automatically, usually by
a push to your repository. A typical flow: pull the code, install dependencies,
run the test suite, build the artifact or container, and if every stage passes,
deploy it. If any stage fails, the pipeline stops and reports exactly where, so a
broken change never reaches production. The whole thing is configured as code, a
file in the repo describing the stages, so the process is versioned and consistent
for every change rather than depending on someone remembering the steps.

## Why It Matters
Manual build-test-deploy is slow and error-prone: steps get skipped, tests get
forgotten, and bad code reaches users. A pipeline makes the safe path the
automatic path, every change is tested the same way every time, and only what
passes moves forward. This is what lets teams ship small changes frequently and
confidently, because the pipeline catches regressions immediately rather than days
later. It is the automation layer that makes testing and containerization pay off,
running them on every single change without human effort.

## The Pattern
Automate the road from commit to production, build, test, deploy, as versioned
pipeline stages that stop on the first failure. Make the safe path the automatic
path so every change is checked the same way.
