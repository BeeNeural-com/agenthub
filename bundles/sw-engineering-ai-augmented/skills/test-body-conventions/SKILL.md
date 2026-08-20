---
name: test-body-conventions
description: "Shared test body implementation conventions: spec-to-code step mapping, AAA-with-steps format, and worked examples for both SWE.5 integration tests and SWE.6 qualification tests. Read this skill before implementing any GTest body in tests/integration/ or tests/qualification/."
---

# Test Body Implementation Conventions — Worked Examples

The normative rules are in `test-implementation.instructions.md` § 5 (auto-applied for both `tests/integration/` and `tests/qualification/`). This skill provides **worked examples** demonstrating correct step-to-code mapping.

## Step Comment Formats

Two accepted formats exist for step comments in test bodies:

**Format A — Pure step comments (preferred for 6+ steps):**
```cpp
// Step N: <Action from spec>
<code implementing the action>
// Verify step N: <Expected from spec>
<EXPECT_*/ASSERT_* checking the expected result>
```

When the step's Expected column says "n/a" or contains no observable outcome, the Step comment stands alone with no Verify line.

**Format B — AAA-with-steps (acceptable for up to 5 steps):**
```cpp
// Arrange (step 1): <Action from spec>
<setup code>
// Act (step 3): <Action from spec>
<action code>
// Assert (step 3): <Expected from spec>
EXPECT_EQ(...);
```

---

## Why Step Mapping Matters

A human reviewer opens the TCASE spec and the GTest file side by side. For every Step row in the Test Procedure table, the reviewer locates the corresponding `// Step N:` or `(step N):` comment in the code. If any step is missing or renumbered, the review fails. This 1:1 mapping is the primary ASPICE traceability artifact from spec to implementation.

---

## Pattern A — Pure Step Comments (Preferred)

Best when the Test Procedure table has many fine-grained steps. Each step from the table maps to one comment block.

### Example Spec (Integration — TCASE_01)

| Step | Action | Expected |
|-----:|--------|----------|
| 1 | Construct `<Component>::Server` | `isListening()` == false |
| 2 | Call `processEvents()` before `listen()` | Returns success (no-op) |
| 3 | Register handlers; call `listen(path)` | Returns success; `isListening()` == true |
| 4 | Connect Client; call `server.processEvents()` | Client-connected notification fires |
| 5 | Client sends message; call `server.processEvents()` | Message notification fires |
| 6 | Call `server.closeClient(handler)` | Returns success |
| 7 | Call `server.shutdown()` | Returns success; `isListening()` == false |
| 8 | Call `server.shutdown()` again | Returns success (no-op) |

### Correct Implementation

```cpp
TEST_F(<Component>IntegrationTest, ServerApiFullOperationSequence)
{
    // Step 1: Construct Server
    EXPECT_FALSE(server_.isListening());

    // Step 2: processEvents() before listen() is a no-op — returns success
    EXPECT_FALSE(server_.processEvents()) << "processEvents before listen must succeed";

    // Step 3: Register handlers; call listen(path)
    <Component>::ClientHandler* pHandler = nullptr;
    server_.setClientConnectedHandler([&](<Component>::ClientHandler& h) { pHandler = &h; });
    server_.setClientDisconnectedHandler([](<Component>::ClientHandler&) {});
    ASSERT_FALSE(server_.listen(kTestSocketPath));
    EXPECT_TRUE(server_.isListening());

    // Step 4: Connect Client; call server.processEvents() to accept
    <Component>::Client client;
    client.setMessageHandler([](const uint8_t*, uint32_t) {});
    client.setServerDisconnectedHandler([] {});
    ASSERT_FALSE(client.connect(kTestSocketPath));
    ASSERT_FALSE(server_.processEvents());
    ASSERT_NE(pHandler, nullptr);

    // Step 5: Client sends message; server receives via processEvents
    bool serverReceivedMessage = false;
    pHandler->setMessageHandler([&](const uint8_t*, uint32_t) { serverReceivedMessage = true; });
    const uint8_t data[] = {'h', 'i'};
    ASSERT_FALSE(client.send(data, 2));
    ASSERT_FALSE(server_.processEvents());
    EXPECT_TRUE(serverReceivedMessage);

    // Step 6: closeClient
    EXPECT_FALSE(server_.closeClient(*pHandler));

    // Step 7: shutdown
    EXPECT_FALSE(server_.shutdown());
    EXPECT_FALSE(server_.isListening());

    // Step 8: second shutdown is a no-op — must return success
    EXPECT_FALSE(server_.shutdown()) << "second shutdown must succeed (no-op)";
}
```

### Why This Works

- Every step number appears in the code.
- Step comments reuse wording from the spec **Action** column.
- Expected values from the spec table appear as assertions immediately after each step.
- A reviewer checks off steps 1–8 without scrolling back and forth.

---

## Pattern B — AAA-with-Steps (Alternative)

Best when the test has a clear Arrange/Act/Assert structure with few steps. Embed step references in the AAA labels.

### Example Spec (Qualification — TCASE_03)

| Step | Action | Expected Result |
|-----:|--------|----------------|
| 1 | Start server; register `clientDisconnectedHandler` setting a flag | Server listening |
| 2 | Scope-create a Client; connect; accept via `processEvents()` | Client connected |
| 3 | Destroy Client (let it go out of scope) | Destructor runs |
| 4 | Call `server.processEvents()` | `clientDisconnectedHandler` invoked |

### Correct Implementation

```cpp
TEST_F(<Component>QualificationTest, ClientDestruct_ConnectionClosed_ServerDetectsDisconnect)
{
    // Arrange (step 1): Start server; register clientDisconnectedHandler
    bool disconnectedCalled = false;
    server_.setClientConnectedHandler([](<Component>::ClientHandler&) {});
    server_.setClientDisconnectedHandler([&](<Component>::ClientHandler&) { disconnectedCalled = true; });
    ASSERT_FALSE(server_.listen(kTestSocketPath));

    // Act (step 2): Scope-create Client, connect, accept
    {
        <Component>::Client client;
        client.setMessageHandler([](const uint8_t*, uint32_t) {});
        client.setServerDisconnectedHandler([] {});
        ASSERT_FALSE(client.connect(kTestSocketPath));
        ASSERT_FALSE(server_.processEvents());
    }  // Act (step 3): Client destroyed — destructor closes connection

    // Act (step 4): Server processes disconnect
    ASSERT_FALSE(server_.processEvents());

    // Assert (step 4): clientDisconnectedHandler invoked
    EXPECT_TRUE(disconnectedCalled);
}
```

### Why This Works

- Steps 1–4 all appear.
- The AAA grouping aids readability.
- Step numbers still match the spec table 1:1.
- The scope comment `// Act (step 3):` annotates the implicit destructor action.

---

## Pattern C — Multi-Phase (Multiple Act/Assert Blocks)

When a test has multiple Act phases, repeat the labels with correct step references.

### Example Spec (Qualification — TCASE_01)

| Step | Action | Expected Result |
|-----:|--------|----------------|
| 1 | Scope-create Server. Connect two Clients with disconnect handlers. Accept. | Two Clients connected; socket file exists |
| 2 | Destroy Server (out of scope) | Destructor runs |
| 3 | Call `processEvents()` on both Clients | Both disconnect handlers fire |
| 4 | Check socket file | Socket file removed |

### Correct Implementation

```cpp
TEST_F(<Component>QualificationTest, ServerDestruct_ReleasesAllResources)
{
    // Arrange (step 1): Scope-create server; connect two Clients with disconnect handlers
    bool disco1 = false;
    bool disco2 = false;
    auto client1 = std::make_unique<<Component>::Client>();
    client1->setMessageHandler([](const uint8_t*, uint32_t) {});
    client1->setServerDisconnectedHandler([&] { disco1 = true; });

    auto client2 = std::make_unique<<Component>::Client>();
    client2->setMessageHandler([](const uint8_t*, uint32_t) {});
    client2->setServerDisconnectedHandler([&] { disco2 = true; });

    {
        <Component>::Server server;
        server.setClientConnectedHandler([](<Component>::ClientHandler&) {});
        server.setClientDisconnectedHandler([](<Component>::ClientHandler&) {});
        ASSERT_FALSE(server.listen(kTestSocketPath));
        ASSERT_EQ(::access(kTestSocketPath, F_OK), 0);

        ASSERT_FALSE(client1->connect(kTestSocketPath));
        ASSERT_FALSE(client2->connect(kTestSocketPath));
        for (int i = 0; i < 10; ++i)
        {
            ASSERT_FALSE(server.processEvents());
        }

        // Act (step 2): Destroy server (goes out of scope)
    }

    // Act (step 3): Process events on both Clients
    ASSERT_FALSE(client1->processEvents());
    ASSERT_FALSE(client2->processEvents());

    // Assert (step 3): Both disconnect handlers fire
    EXPECT_TRUE(disco1);
    EXPECT_TRUE(disco2);

    // Assert (step 4): Socket file removed
    EXPECT_NE(::access(kTestSocketPath, F_OK), 0);
}
```

---

## Anti-Pattern Gallery

### Anti-Pattern 1: Plain AAA Without Step Numbers

```cpp
// WRONG — spec has 10 steps but code has 3 AAA sections
TEST_F(IntegrationTest, LifecycleBidirectionalExchange)
{
    // Arrange: server with handlers ...

    // Act: connect → accept → PING/PONG exchange ...

    // Assert: payloads delivered correctly ...
}
```

**Problem:** A reviewer cannot verify which of the 10 spec steps are implemented. Steps 5–8 might be silently skipped.

### Anti-Pattern 2: Ad-Hoc Step Numbers

```cpp
// WRONG — step numbers are author-invented, not from the spec table
TEST_F(QualificationTest, ServerCleanup)
{
    // Arrange (step 1): setup ...
    // Act (step 2): destroy ...
    // Assert (step 3): check ...
}
```

**Problem:** The spec table might have 4 steps where step 2 is "Connect clients" and step 3 is "Destroy server". The code's numbering creates false traceability.

### Anti-Pattern 3: Grouped Steps Without Listing Each

```cpp
// WRONG — steps 4–7 from the spec are hidden under one comment
TEST_F(IntegrationTest, ServerApiSequence)
{
    // Steps 1–3: setup ...
    // Steps 4–7: exercise the full protocol
    // Step 8: verify ...
}
```

**Problem:** Individual step coverage cannot be verified. If step 5 is missing, no reviewer will catch it.

---

## Choosing Between Pattern A and Pattern B

| Condition | Use |
|---|---|
| Test Procedure has ≥ 6 steps | Pattern A (pure steps) |
| Test Procedure has ≤ 5 steps with clear setup/action/check phases | Pattern B (AAA-with-steps) |
| Test has multiple Act phases (e.g., destroy then process) | Pattern C (multi-phase) |
| Any format where every step number appears | Acceptable |
| Any format where step numbers are missing or ad-hoc | **Prohibited** |
