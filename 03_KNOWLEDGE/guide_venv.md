# Guide: Venv Separation — Why Every Project Needs Its Own Environment

A virtual environment is an isolated Python installation. When you create one for a project, that project gets its own copy of Python and its own set of installed packages. Changes to one virtual environment do not affect any other. Projects that need different versions of the same library can coexist on the same machine without conflict.

This isolation is the foundation of reliable Python development. Without it, all your projects share one Python installation, all their dependencies compete for the same package slots, and upgrading a library for one project can silently break every other project on the machine.

My ecosystem has four active Python projects: the BDF soccer content generator, the CA Book system, the custom agent TTS tool, and the construction business OS. Each one runs in its own isolated virtual environment at a dedicated path.

The BDF venv lives at C drive backslash Dev backslash Projects backslash soccer-content-generator backslash venv. This venv carries the CUDA-specific PyTorch installation required for GPU-accelerated processing, which makes it the heaviest environment in the ecosystem. Rebuilding it from scratch requires careful handling because the CUDA nightly build must be installed with exact version pinning or the GPU acceleration breaks.

The CA Book venv lives at C drive backslash Knowledge backslash CA backslash venv. It carries the Kokoro TTS engine, numpy, and soundfile for audio synthesis. The ca underscore audio dot py script must always be called using this venv's Python executable, never the BDF venv. The CLAUDE dot md for custom agent explicitly documents this requirement.

The construction business OS venv lives at C drive backslash Dev backslash CristianConstruction backslash venv. It carries FastAPI, the Anthropic SDK, and the Twilio and Telegram libraries for the agent communication layer.

The custom agent venv was historically the most problematic. For an extended period, ca underscore audio dot py was being called using the BDF venv because both projects had been developed in the same environment before the separation work. The fix was documented in the CLAUDE dot md file and in Navigation Shortcuts.

The BDF venv reached a state before the separation work where it contained 39 packages that belonged to other projects. These leaked packages arrived over months of development when the wrong environment was active during pip install commands. The contamination had three consequences. Dependency conflicts became unpredictable because upgrading a package for soccer could break the CA compiler. Cost auditing became impossible because it was unclear which project owned which computational overhead. Claude Code got confused about project scope because it saw dependencies from multiple unrelated projects in a single environment.

The fix required auditing the BDF venv against the actual requirements of the soccer project, saving the CUDA PyTorch build separately because it cannot be reinstalled through a normal pip command, deleting the entire venv directory, rebuilding it from scratch, and reinstalling only the packages that actually belonged to the soccer content generator.

The PowerShell profile maintains activation aliases for each project. Each alias activates the correct venv for that project. The profile file location is critical. PowerShell loads the profile from the path in the PROFILE variable which on Windows typically resolves to the OneDrive Documents folder rather than the local Documents folder. Installing aliases in the wrong profile file means they are never loaded. Navigation Shortcuts documents all four profile file locations and notes which one is active.

The discipline required to maintain venv isolation is simple. Before any pip install command, confirm the correct environment is active. The prompt should show the project name in parentheses. If it shows the wrong project or no project at all, stop. Run the activation alias for the correct project first. This thirty-second check prevents hours of cleanup work later.

Virtual environments are cheap to create and expensive to contaminate. Create a new one for every project. Name it venv at the project root. Document its path in Navigation Shortcuts the moment you create it. Add it to the project gitignore so it never gets committed. These four habits keep the ecosystem clean indefinitely.
