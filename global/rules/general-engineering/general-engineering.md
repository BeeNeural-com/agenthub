# General Engineering Guidelines

- Approach every task with the mindset of a **senior software engineer**, aiming for clean, maintainable, and scalable solutions.
- Consistently apply the **SOLID principles** throughout the codebase.
- Use **design patterns** thoughtfully — apply them only when they improve clarity, scalability, or maintainability.
- Follow established **best practices**, including:
  - A clear, modular **folder and module structure** that scales with the project.
  - Consistent and descriptive **naming conventions** for files, classes, functions, and variables.
- Favor the **object-oriented programming paradigm** whenever appropriate, while remaining pragmatic and flexible when another paradigm provides a simpler solution.
- Avoid unnecessary **boilerplate code**, as it increases maintenance efforts and reduces scalability.
- Prevent and eliminate **duplicate code** by refactoring into reusable components or utilities.
- Ensure all code is **testable** and provide **unit tests** for all logics.
- Maintain **clear documentation**:
  - Use **Google-style docstrings** for functions, classes, and modules.
  - Add comments only where they clarify intent or rationale.
- Keep external dependencies **minimal** and document their purpose and justification.

## Context
- Always consider the **project context** and maintain a clear **folder/module structure** when working on any file.
- When writing or modifying code, apply changes **incrementally and step by step** — avoid introducing large chunks of code at once.


## Documentation
- Create a single **README.md** file at the project root to document the overall project.
- Do not add additional README files inside subfolders unless explicitly required.

````
