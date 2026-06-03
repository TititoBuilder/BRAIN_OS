---
knowledge_os_machine_key: diffusion_models
knowledge_os_domain: AI/ML
knowledge_os_status: Learning
knowledge_os_score: 30
knowledge_os_priority: Medium
knowledge_os_evidence: DALL-E 3 â†’ gpt-image-1 BDF migration
knowledge_os_last_touched: '2026-04-20'
---
# Diffusion Models

## What It Is
Diffusion models generate images, and increasingly audio and other data, by
learning to reverse a process of adding noise. They are the technology behind most
modern AI image generation. The core trick is counterintuitive: the model learns to
turn random noise into a coherent image by removing noise step by step.

## How It Works
Training works by taking real images and progressively adding random noise until
they are pure static, while the model learns to predict and undo each step of that
corruption. To generate, you start from pure random noise and run the learned
process in reverse: the model repeatedly estimates what noise to remove, and over
many steps a clear image emerges that never existed before. Text-to-image versions
steer this denoising with a text prompt, so the image that forms matches the
description, the prompt guides which coherent image the noise resolves into.

## Why It Matters
Diffusion is why high-quality image generation became widely usable, and
understanding it demystifies what these tools are doing, not retrieving or
collaging existing images, but synthesizing new ones by guided denoising. It also
clarifies their behavior: why generation takes many steps and is slower than a
single model pass, why the same prompt with different starting noise gives
different images, and why the prompt shapes but does not fully determine the
result. Knowing the mechanism makes the tools predictable rather than magical.

## The Pattern
Generate by reversing noise: start from static, remove noise step by step toward a
coherent result, steer the process with a prompt. New synthesis, not retrieval,
which is why it is iterative and why starting noise matters.
