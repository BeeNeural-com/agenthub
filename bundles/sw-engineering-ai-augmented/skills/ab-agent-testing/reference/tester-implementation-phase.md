# Tester Implementation Phase (Phase 2)

This reference applies only to the Integration Tester and Qualification Tester
agents. Phase 2 tests evaluate the agent's ability to implement test code from
specifications. The agent receives Phase 1 output (spec files) as input and
produces `.cpp`/`.h` test implementations.

---

## How to Inject Phase 1 Output into Phase 2 Clones

Use the `--phase phase2 --inject-spec <directory>` flags during prepare:

```bash
# First, get Phase 1 output from a previous successful run
PHASE1_SPECS="$(readlink -f "$PHASE1_RUN_DIR/improved/worktree")/doc/<component>/component_integration_tests"

# Prepare Phase 2 clones with spec injection
RUN_DIR=$(./tools/ab-test/ab-test prepare "<agent-name>" \
  --refs develop HEAD \
  --phase phase2 \
  --inject-spec "$PHASE1_SPECS" \
  | grep "Run dir:" | awk '{print $NF}')
```

The prepare step:
1. Clones and normalizes both versions (same as Phase 1)
2. Cleans Phase 2 output artifacts (`tests/integration/*.cpp`, `*.h`)
3. Copies all `.md` files from `--inject-spec` into the manifest's
   `inject.target_subdir` within each clone's `doc/<component>/` directory
4. Both clones receive identical spec files (the variable is still only the
   agent definition and ecosystem)

---

## Phase 2 Run Command

```bash
./tools/ab-test/ab-test run "$RUN_DIR" baseline --exec --phase phase2 --runs 1 --timeout 1200
./tools/ab-test/ab-test run "$RUN_DIR" improved --exec --phase phase2 --runs 1 --timeout 1200
```

Phase 2 metrics (`phase2` section in manifest) measure TEST_F macro counts,
annotation coverage, AAA step comments, and CMake registration.
