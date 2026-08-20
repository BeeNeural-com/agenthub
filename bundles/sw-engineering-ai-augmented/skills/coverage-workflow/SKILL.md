---
name: coverage-workflow
description: "gcovr coverage measurement workflow for SWE.3 unit construction: local build with COVERAGE=ON, test execution, and report generation."
---

# Coverage Workflow

Run after Stage 3 GREEN to measure line, function, and branch coverage of production code.

## Prerequisites

- `gcovr` and a matching `gcov-<version>` binary on the host (e.g., `gcov-13` for GCC 13).
- `libgtest-dev` must be installed locally.

## Steps

```bash
# 1. Configure with coverage instrumentation (local, not Docker)
mkdir -p build_coverage && cd build_coverage
cmake .. -DCOVERAGE=ON -DCONAN_PKG_VERSION=0.0.1 -DCMAKE_BUILD_TYPE=Debug

# 2. Build test binary
make libipc_gtest -j$(nproc)

# 3. Run tests to generate .gcda profiling data
./bin/libipc_gtest

# 4. Generate text summary (production code only)
cd .. && gcovr --gcov-executable gcov-13 --root . build_coverage \
  -f 'src/libipc/' --print-summary

# 5. Generate HTML report (optional)
gcovr --gcov-executable gcov-13 --root . build_coverage \
  -f 'src/libipc/' --html-details build_coverage/coverage.html
```

## Thresholds (report, do not block)

| Metric | Target |
|---|---|
| Lines (statement coverage) | >= 95% |
| Branches (decision coverage) | >= 95% |

## Exclusions

- Generated code from third-party components placed in `src/gen/` is excluded from coverage measurement. Use the gcovr filter `-f 'src/libipc/'` (or the relevant component path) to target only production code.

## Notes

- The `COVERAGE` CMake option skips VWOS SDK commands (`VWOS/std`, `vwos_add_executable`, `add_subdirectory(cmake)`) so the build works locally without Docker.
- Use `--gcov-executable gcov-13` (match your GCC major version).
- `build_coverage/` is in `.gitignore`; do not commit coverage artifacts.
