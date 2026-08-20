---
name: vlan-kmatrix
description: "E3 VLAN K-Matrix (Kommunikationsmatrix) reference data for CARIAD SE TX-XN VLAN connectivity and module configuration. Use when analyzing VLAN connectivity requirements or configuration for E3 platform modules."
---

# E3 VLAN K-Matrix (Kommunikationsmatrix)

## Official References

- **Source document**: `E3_1_2_Ultra_VLAN_Connect_KMatrix_Module_V20.00.00.00A_20260217_BAm_P07.xlsx` — CARIAD SE TX-XN, 17.02.2026, Version V20.00.00.00A (P01–P07)
- **Converted reference**: `.github/references/E3_1_2_Ultra_VLAN_Connect_KMatrix_Module_V20.00.00.00A_20260217_BAm_P07.adoc`
- **ServiceDesk for questions**: https://devstack.vwgroup.com/jira/servicedesk/customer/portal/23/group/63
- **E3 Build Modes**: https://devstack.vwgroup.com/confluence/display/E3ARCH/Build+Modes

---

## Overview

A **Kommunikationsmatrix** (K-Matrix) is the master communication specification for an automotive E/E architecture. It defines every signal, message (frame), and protocol data unit (PDU) exchanged between Electronic Control Units (ECUs) on a specific bus segment. This document covers the **VLAN/Ethernet** bus segment of the E3 1.2 platform.

### Purpose

- Defines **which ECU sends each signal**, which ECUs receive it, and how it is encoded.
- Serves as the authoritative input for:
  - Generating network database files (DBC, FIBEX, ARXML).
  - Software interface definitions and API contracts at ECU boundary.
  - Integration test scope: which signals must be verified during SWE.5.
  - Requirements analysis (SWE.1): externally observable behaviour in terms of signal names, ranges, and timing.

### Technology Context

The E3 1.2 VLAN K-Matrix describes Ethernet-based communication using:
- **UDP unicast / UDP multicast** — application signal frames and service discovery.
- **TCP** — connection-oriented services (e.g., LUM, diagnostics).
- **SOME/IP** — Service-Oriented Middleware over IP (including SOME/IP SD for service discovery).
- **ViWi** — VW Vehicle API (also uses SOME/IP SD for discovery).
- **IPv6** — all addresses are IPv6 (ULA unicast `fd53:7cb8:383:x::y`; multicast `ff14::x`).

---

## Document Structure

A K-Matrix workbook contains two sheets:

### Sheet 1 — Deckblatt (Cover Page)

Contains document metadata and the signal participation legend:

| Field               | Content                                                                                                            |
| ------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Datenfestlegung     | Document title: "Datenfestlegung, EndToEnd Elektronikbaukasten 1.2"                                                |
| Stand               | Release date: 17.02.2026                                                                                           |
| Timestamp           | Export timestamp: 2026-02-17_01-06-54                                                                              |
| Version             | V20.00.00.00A_P01_P02_P03_P04_P05_P06_P07                                                                          |
| Autor               | CARIAD SE TX-XN, Major-Hirst-Strasse 7, 38442 Wolfsburg                                                            |
| Hinweis (Tool Note) | Vector db-Editor byte counting starts at 0 (dbc-file); K-Matrix Excel uses bytes starting at 1, bits starting at 0 |

#### Signal Participation Legend

| Code | Meaning (German → English)                                                                                                                                   |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `S`  | Signal wird aktiv gesendet — Signal is actively sent by this ECU (supported)                                                                                 |
| `S*` | Signal wird geroutet von anderem Bussegment — Signal is routed from another bus segment; at least one ECU in the vehicle supports it. Contact the ECU owner. |
| `0`  | Signal kann nicht aktiv bedient werden — ECU cannot actively operate this signal; transmits "0" or init value                                                |
| `0*` | Geroutetes Signal, nicht aktiv bedienbar — Routed but inactive: ECU routes the signal but cannot operate it                                                  |
| `E`  | Signal wird empfangen und ausgewertet — Signal is received and evaluated (may also be routed at gateway)                                                     |
| `E*` | Signal wird geroutet in anderes Bussegment — Signal is routed to another bus segment; not used internally                                                    |
| `FD` | CAN FD frame format (in "Protokoll" column); "Classical" = CAN 2.0 — Note: not applicable in VLAN sheet                                                      |

### Sheet 2 — VLAN_Connect

The main data matrix. Each row represents one **signal**. Frame and PDU columns repeat for each signal belonging to the same PDU/frame. The table has 271 columns organized into five groups:

1. **Frames** (14 columns) — network packet definition
2. **PDUs** (12 columns) — protocol data unit definition
3. **Signale** (10 columns) — individual signal encoding
4. **Wertebereich** (9 columns) — value range, physical conversion, and logical labels
5. **Sender–Empfänger** (~225 columns) — participation matrix per SW function component per ECU
6. **FunktionsCluster** (1 column) — functional domain classification
7. **Signalkommentar** (1 column) — natural-language signal description

---

## Data Hierarchy

```
Frame  (network packet: IP src/dst, port, protocol, payload size, timing)
  └── PDU  (protocol data unit: ID, offset, send type, cycle time)
        └── Signal  (bit-level encoding: position, width, initial/error/inactive values)
              └── Value Range  (physical conversion, logical label table)
```

**Key rule**: Multiple rows in the matrix share the same `Frame` + `PDU` values when they belong to the same PDU. Each row adds one signal. To read all signals in a PDU, group rows by (Frame, PDU).

---

## Frame Attributes

| Column                 | German Label           | Description                                                                                                                                                                                                 |
| ---------------------- | ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Frame                  | Frame                  | Frame name. Naming convention: `SK_<SenderECU>_<TargetOrBus>_<Index>` for application frames; `SD_SomeIP_<ECU>_MC` / `SD_SomeIP_<A>_<B>_UC` for SOME/IP SD frames; `SD_ViWi_<A>_<B>_UC` for ViWi SD frames. |
| Frame-Typ              | Frame-Typ              | Transport protocol: `UDP` or `TCP`                                                                                                                                                                          |
| Frame-Layout           | Frame-Layout           | Payload structure, typically `PDU dynamisch` (variable PDU content)                                                                                                                                         |
| Quell IP-Adresse       | Quell IP-Adresse       | Source IPv6 address. Format: `fd53:7cb8:383:<segment>::<hostid>` (unicast ULA)                                                                                                                              |
| Quell Service-Port     | Quell Service-Port     | Source UDP/TCP port                                                                                                                                                                                         |
| Ziel IP-Adresse        | Ziel IP-Adresse        | Destination IPv6 address. Format: `ff14::<groupid>` (site-local multicast) or ULA for unicast                                                                                                               |
| Ziel Service-Port      | Ziel Service-Port      | Destination UDP/TCP port                                                                                                                                                                                    |
| TCP Sessionaufbau      | TCP Sessionaufbau      | TCP connection initiator ECU (TCP frames only)                                                                                                                                                              |
| TCP Receive Windowsize | TCP Receive Windowsize | TCP receive window size in bytes                                                                                                                                                                            |
| IP-Adressen-Typ        | IP-Adressen-Typ        | Address type: `Unicast` or `Multicast`                                                                                                                                                                      |
| Layer 4 Payload [Byte] | Layer 4 Payload [Byte] | Total UDP/TCP payload size in bytes                                                                                                                                                                         |
| Frame-Timeout [ms]     | Frame-Timeout [ms]     | Maximum allowed receive gap before frame is considered lost (ms)                                                                                                                                            |
| MaxSendBuffer [Bytes]  | MaxSendBuffer [Bytes]  | Maximum transmit buffer size in bytes                                                                                                                                                                       |
| Priorität              | Priorität              | DSCP / VLAN QoS priority                                                                                                                                                                                    |

### Frame Naming Patterns

| Pattern                    | Example                        | Meaning                                                    |
| -------------------------- | ------------------------------ | ---------------------------------------------------------- |
| `SK_<ECU>_<Index>`         | `SK_BCM1_01`                   | Application frame #01 from BCM1 (Body Control Module)      |
| `SK_<ECU1>_<ECU2>_<Index>` | `SK_HCP1_HCP5_01`              | Application frame #01 from HCP1 to HCP5                    |
| `SD_SomeIP_<ECU>_MC`       | `SD_SomeIP_BCM1_MC`            | SOME/IP Service Discovery multicast announcement from BCM1 |
| `SD_SomeIP_<A>_<B>_UC`     | `SD_SomeIP_eCall_HCP3Sys03_UC` | SOME/IP SD unicast between eCall and HCP3Sys03             |
| `SD_ViWi_<A>_<B>_UC`       | `SD_ViWi_HCP3Sys03_SGW03_UC`   | ViWi Service Discovery unicast between HCP3Sys03 and SGW03 |

### IP Addressing

| Type                      | Format                              | Example                       |
| ------------------------- | ----------------------------------- | ----------------------------- |
| IPv6 ULA unicast          | `fd53:7cb8:383:<segment>::<hostid>` | `fd53:7cb8:383:1::10`         |
| IPv6 site-local multicast | `ff14::<groupid>`                   | `ff14::3a`                    |
| SOME/IP SD standard port  | 30490                               | Used by all SOME/IP SD frames |
| Application data ports    | ECU-specific                        | 42557, 42994, etc.            |

---

## PDU Attributes

| Column                  | German Label            | Description                                                                                        |
| ----------------------- | ----------------------- | -------------------------------------------------------------------------------------------------- |
| PDU                     | PDU                     | PDU name. Often reflects the functional group of its signals (e.g., `VMM_04`, `SAD_02`, `HVLS_01`) |
| PDU-Typ                 | PDU-Typ                 | PDU type: `intern` (application data PDU) or service type                                          |
| PDU-ID [hex]            | PDU-ID [hex]            | Unique PDU identifier within the frame (hexadecimal)                                               |
| PDU-Länge [Bytes]       | PDU-Länge [Bytes]       | PDU length in bytes                                                                                |
| PDU-Offset              | PDU-Offset              | Byte offset of PDU within the frame payload                                                        |
| PDU-Sendeart            | PDU-Sendeart            | Send trigger: `Cyclic`, `OnChange`, `OnChangeWithRepetition`, `Event`                              |
| PDU-Timeout [ms]        | PDU-Timeout [ms]        | Maximum allowed receive gap before PDU is considered lost (ms)                                     |
| Trigger                 | Trigger                 | Additional trigger condition (if applicable)                                                       |
| Zykluszeit normal [ms]  | Zykluszeit normal [ms]  | Normal cyclic send interval in ms                                                                  |
| Zykluszeit schnell [ms] | Zykluszeit schnell [ms] | Fast cyclic send interval in ms (used when signal changes rapidly)                                 |
| Inhibitzeit [ms]        | Inhibitzeit [ms]        | Minimum time between two successive transmissions in ms                                            |
| NrOfRepetition          | NrOfRepetition          | Number of repetitions to send after an OnChange event                                              |

---

## Signal Attributes

| Column                   | German Label             | Description                                                                                          |
| ------------------------ | ------------------------ | ---------------------------------------------------------------------------------------------------- |
| Signal                   | Signal                   | Signal name. Prefix reflects originating function or ECU (see Signal Naming below)                   |
| StartByte                | StartByte                | Byte position within the PDU — **1-based** (K-Matrix Excel convention; Vector dbc-files use 0-based) |
| StartBit                 | StartBit                 | Bit position within the start byte — **0-based**                                                     |
| Signal Länge [Bits]      | Signal Länge [Bits]      | Signal width in bits                                                                                 |
| Signalsendeart           | Signalsendeart           | Signal-level send type: `Cyclic`, `OnChange`, `OnChangeWithRepetition`                               |
| Inaktiver Wert roh [dez] | Inaktiver Wert roh [dez] | Raw value encoding "inactive" state (decimal)                                                        |
| MUX Signal               | MUX Signal               | Multiplexer signal name (if this signal is multiplexed)                                              |
| MUX Gruppe               | MUX Gruppe               | Multiplexer group ID (if this signal is multiplexed)                                                 |
| InitWert roh [dez]       | InitWert roh [dez]       | Default/initialization raw value (decimal)                                                           |
| FehlerWert roh [dez]     | FehlerWert roh [dez]     | Error/fault raw value (decimal)                                                                      |

### Bit Counting Warning

> **IMPORTANT**: The K-Matrix Excel uses **bytes starting at 1**, bits starting at 0. The Vector db-Editor (dbc-file) uses **bytes starting at 0**. When consuming K-Matrix data to generate dbc or ARXML, subtract 1 from every `StartByte` value.

---

## Value Range and Encoding

### Physical Value Conversion

For analogue signals, the physical value is computed from the raw value:

```
physical_value = raw_value × Skalierung + Offset
```

| Column            | German Label      | Description                                                                                  |
| ----------------- | ----------------- | -------------------------------------------------------------------------------------------- |
| Min Rohwert [dez] | Min Rohwert [dez] | Minimum valid raw value (decimal)                                                            |
| Max Rohwert [dez] | Max Rohwert [dez] | Maximum valid raw value (decimal). Special raw values above this maximum encode Init/Fehler. |
| phy Werte [dez]   | phy Werte [dez]   | Physical value range (computed)                                                              |
| Einheit           | Einheit           | Physical unit                                                                                |
| Offset            | Offset            | Offset in the linear conversion formula                                                      |
| Skalierung        | Skalierung        | Scaling factor (resolution per LSB)                                                          |

**Example** — `VMM_LgtPot_ADrg` (longitudinal drag acceleration potential):
- Raw range: 0–2045; Init = 2046; Fehler = 2047
- Offset: −10.23; Skalierung: 0.01
- Physical range: −10.23 m/s² to +10.22 m/s²

### Physical Units Observed

| Unit string               | Meaning                     |
| ------------------------- | --------------------------- |
| `Unit_MeterPerSeconSquar` | m/s² (acceleration)         |
| `Unit_MeterPerSecon`      | m/s (velocity)              |
| `Unit_MeterInver`         | 1/m (curvature)             |
| `Unit_WattPerMeterSquar`  | W/m² (solar irradiance)     |
| `Unit_None`               | Dimensionless / enumeration |

### Logical Values (Enumeration Encoding)

For enumeration signals, the value range columns contain parallel space-separated lists:

| Column                    | German Label              | Content                                                                                     |
| ------------------------- | ------------------------- | ------------------------------------------------------------------------------------------- |
| Rohwert [dez]             | Rohwert [dez]             | Space-separated raw values, e.g. `0 1 2 3`                                                  |
| Beschreibung              | Beschreibung              | Space-separated label names in same order, e.g. `Init geschlossen nicht_geschlossen Fehler` |
| Worst Case Aufstartlatenz | Worst Case Aufstartlatenz | Maximum startup latency in ms (safety/supply analysis)                                      |

**Example** — `HVLS_LadeklappePosition_Lk1` (charging port lid position):
- Rohwert: `0 1 2 3`
- Beschreibung: `Init geschlossen nicht_geschlossen Fehler`

---

## Sender–Empfänger Matrix

Each ECU occupies one or more **sub-columns**, one per SW function component deployed on that ECU. The sub-column naming convention is:

```
<SoftwareFunctionName>_XIX_<FunctionCluster>_XIX_<ECU>
```

where `_XIX_` is the domain separator used in the E3 SOME/IP service architecture.

**Examples**:
- `Car2PhoneApp_XIX_Connectivity_XIX_ConMod_CD` — Car2Phone app, Connectivity cluster, on ConMod_CD ECU
- `AnsteuerungLadeklappe_VALK_SG1_XIX_HV_Laden_XIX_SACID_1` — Charging port control, HV charging cluster, on SACID_1 ECU

### ECUs in This Document

| ECU                  | Description                                            | Sub-columns |
| -------------------- | ------------------------------------------------------ | ----------- |
| `BAP_Tester`         | BAP test system                                        | 2           |
| `ConMod_CD`          | Connectivity Module — Consumer Device                  | ~14         |
| `ConMod_NAD`         | Connectivity Module — Network Access Device (cellular) | ~22         |
| `ConMod_V2X`         | Connectivity Module — Vehicle-to-Everything            | ~7          |
| `HCP5_P10_ETHRouter` | HCP5 Ethernet Router processor                         | 3           |
| `HCP5_P4_E3SWPAC`    | HCP5 E3 SW Platform + ADAS Compute                     | ~38         |
| `HCP5_P6_MOD`        | HCP5 MOD (Mobility Online Data) processor              | ~52         |
| `HCP5_P9_PDX`        | HCP5 PDX processor                                     | 2           |
| `SACID_1`            | Smart AC/DC Integrated Charger #1                      | ~36         |
| `SACID_1_Primary`    | SACID_1 Primary partition                              | ~32         |
| `TestSysIP`          | IP test system                                         | 6           |

### Participation Cell Values

A cell contains one of the codes from the legend:

| Code    | Meaning                                                                      |
| ------- | ---------------------------------------------------------------------------- |
| `S`     | This SW function component sends the signal                                  |
| `S*`    | Routes the signal from another bus segment; original sender exists elsewhere |
| `E`     | This SW function component receives and evaluates the signal                 |
| `E*`    | Routes the signal to another bus segment; not used internally                |
| `0`     | Cannot actively operate the signal; sends init/zero value                    |
| `0*`    | Routed but cannot actively operate                                           |
| (empty) | Not involved in this signal                                                  |

---

## Special Frame Types

### Application Data Frames (`SK_*`)

- Carry real signal data (sensor readings, actuator commands, status values).
- One ECU has `S` (active sender) in exactly one SW function sub-column.
- Receiving ECUs have `E` (receiver) in their relevant SW function sub-columns.
- Routed ECUs have `S*` (routing sender) or `E*` (routing receiver).

### SOME/IP Service Discovery Frames (`SD_SomeIP_*`)

- Do **not** carry application signals; carry only `Service_ServiceDiscoverySomeIP` (64-bit service handle).
- Two subtypes:
  - **Multicast** (`_MC`): Each ECU announces its own services to all others on `ff14::x` multicast. The announcing ECU is `S`; all others are `E`; gateways may be `E*`.
  - **Unicast** (`_UC`): Bidirectional service discovery between a specific ECU pair. One ECU is `S`, the other is `E*`, and the reverse frame exists with inverted roles.
- Standard SOME/IP SD port: **30490**.

### ViWi Service Discovery Frames (`SD_ViWi_*`)

- Same structure as SOME/IP SD unicast frames but for the ViWi (Vehicle Wi-Fi / VW Vehicle API) protocol.
- Always unicast (`_UC`), always between a specific ECU pair.
- Carry `Service_ServiceDiscoveryViWi` (64-bit).

---

## Signal Naming Conventions

### Signal Prefix → Originating Function

| Prefix                      | German / English expansion       | Domain                                                                        |
| --------------------------- | -------------------------------- | ----------------------------------------------------------------------------- |
| `VMM_`                      | Vehicle Motion Management        | Powertrain, ADAS, driving dynamics                                            |
| `SAD_`                      | Schiebeausstelldach              | Sliding/tilting sunroof (panoramic roof)                                      |
| `SSA_`                      | SmartSensorAktor                 | Smart sensor/actuator (door, mirror, roller blind, ambient light, child lock) |
| `SSAM_`                     | SmartSensorAktorManagement       | Management of SmartSensorActor sub-systems                                    |
| `SoSe_`                     | Sonnensensor                     | Sun intensity sensor                                                          |
| `HVLS_`                     | Hochvolt-Ladesystem              | High-voltage charging system                                                  |
| `bCall_`                    | Breakdown Call                   | Emergency breakdown call (b-Call / eCall-adjacent)                            |
| `Service_`                  | SOME/IP / ViWi service interface | Named service endpoints (64-bit handles)                                      |
| `TCPClient_` / `TCPServer_` | TCP connection status signals    | HTTP/diagnostic TCP sessions                                                  |
| `void`                      | (reserved)                       | Unused/padding bits in a PDU                                                  |

### Signal Integrity Signals

Many PDUs include two integrity signals automatically appended:

| Signal suffix | Width  | Description                                                                          |
| ------------- | ------ | ------------------------------------------------------------------------------------ |
| `<PDU>_CRC`   | 8 bits | CRC-8 protection over the PDU payload                                                |
| `<PDU>_BZ`    | 4 bits | **Botschaftszähler** (rolling counter / message counter) — replay and loss detection |

The presence of CRC + BZ indicates the PDU is protected against transmission errors and replay attacks. Software must validate both fields on reception.

### Domain Separator `_XIX_`

The string `_XIX_` separates the three parts of a SW function component column name:

```
<SoftwareFunctionName>  _XIX_  <FunctionCluster>  _XIX_  <ECU>
```

It is a unique delimiter chosen to avoid collisions with underscores within each part name. It appears only in column headers, not in signal names.

---

## FunktionsCluster — Functional Domain Classification

The `FunktionsCluster` column classifies each signal row into a functional domain:

| Value                          | Domain                                                                                         |
| ------------------------------ | ---------------------------------------------------------------------------------------------- |
| `02_Basefunction_Powertrain`   | Base powertrain functions (drivetrain, traction control foundation)                            |
| `06_Basefunction_ComfortLight` | Base comfort and lighting (body control, SmartSensorActor, sun sensor, ambient light)          |
| `10_Powertrain`                | Extended powertrain and ADAS (VMM signals, AEB, parking control, guidance)                     |
| `20_OptionalComfort`           | Optional comfort features (panoramic sunroof SAD, mirror folding, roller blinds, tinted glass) |

Additional clusters exist in the document for connectivity, charging (HV_Laden), diagnostics, OTA, and others — the list above represents the clusters seen in the sampled sections.

---

## Lifecycle & Usage Pattern

### Reading a K-Matrix to Understand a Signal

1. **Filter by Signal name prefix** to narrow to the functional domain.
2. **Identify the Frame row** by finding the rows where `Signal` matches. All rows sharing the same `Frame` + `PDU` values belong to one PDU; all rows sharing the same `Frame` belong to one packet.
3. **Read Frame attributes**: IP addresses → determine unicast vs. multicast, sender ECU.
4. **Read PDU attributes**: PDU-ID, length, send type, cycle time → determines timing contract.
5. **Read Signal attributes**: StartByte (1-based), StartBit (0-based), length in bits → bit extraction.
6. **Read Value Range**: For analogue: apply `physical = raw × Skalierung + Offset`. For enumerations: map `Rohwert` to `Beschreibung` labels.
7. **Read Sender–Empfänger**: Find which SW function sub-column holds `S` → that is the signal owner ECU.

### Finding All Signals of an ECU

1. Locate the ECU's column group in the header row.
2. Filter all rows where any sub-column of that ECU contains `S` (sender) or `E` (receiver).
3. Rows with `S*` indicate routed signals; contact the original sender's ECU team for the source definition.

### Verifying Frame / PDU Membership

Multiple rows with the same `Frame` name AND the same `PDU` name = multiple signals packed into one PDU. The `PDU-Offset` tells you where the PDU starts in the frame payload.

### Converting K-Matrix Bit Position to Software

```
# K-Matrix uses 1-based byte, 0-based bit.
# To convert to 0-based byte offset for software:
byte_offset_0based  = StartByte - 1
bit_within_byte     = StartBit       # already 0-based
bit_offset_from_start_of_pdu = byte_offset_0based * 8 + bit_within_byte
```

---

## Error Catalogue

| Error Condition                     | Indicator                                     | Handling                                                                      |
| ----------------------------------- | --------------------------------------------- | ----------------------------------------------------------------------------- |
| Frame timeout exceeded              | No frame received within `Frame-Timeout [ms]` | Treat all PDU signals as invalid; apply FehlerWert or safe substitute         |
| Signal raw value = `FehlerWert roh` | Signal encoding detected internal ECU fault   | Treat signal as invalid; do not use physical value                            |
| Signal raw value = `InitWert roh`   | ECU has not yet provided valid signal data    | Treat as "not yet available"; wait for valid range                            |
| `BZ` counter discontinuity          | Rolling counter skipped or repeated           | Frame lost or replayed; apply application-level fault reaction                |
| CRC mismatch                        | Computed CRC ≠ received CRC                   | Discard frame; count error; apply timeout reaction after N consecutive errors |
| `S*` signal with no active sender   | No ECU in vehicle supports signal             | Signal will always be `0` or InitWert; do not interpret as active data        |
| `0` code in Sender column           | Signal cannot be actively operated            | Do not trust signal value; use application-level default                      |

---

## Best Practices

1. **Always check FehlerWert and InitWert before using a signal value.** Raw values in these ranges indicate that the ECU itself is not providing valid data. Failing to check leads to acting on invalid physical values.

2. **Apply the byte offset correction when consuming K-Matrix data in software.** The K-Matrix uses 1-based byte counting; all software APIs (AUTOSAR, POSIX memory layouts, dbc-files) use 0-based. Subtract 1 from `StartByte`.

3. **Validate CRC and BZ for safety-relevant signals.** Signals carrying `<PDU>_CRC` and `<PDU>_BZ` must have both fields validated before the application value is used. This is especially critical for VMM (powertrain) and HVLS (charging) signals.

4. **Use the FunktionsCluster column to scope integration test sets.** When testing a specific functional domain (e.g., `10_Powertrain`), filter by `FunktionsCluster` to identify all relevant signal rows without manually reading the entire matrix.

5. **Group rows by (Frame, PDU) before extracting signal lists.** Do not treat each row independently; signals in the same PDU share the same send trigger, cycle time, and timing contract. All signals in a PDU are transmitted atomically.

6. **Distinguish `_MC` from `_UC` SD frames when configuring SOME/IP middleware.** Multicast SD frames announce service availability to all ECUs. Unicast SD frames negotiate subscriptions between specific ECU pairs. Misconfiguring multicast vs. unicast is a common integration error.

7. **Never hardcode IP addresses.** IP addresses in the K-Matrix may change across platform versions (P01–P07 patches). Always derive addresses from the K-Matrix version in use for the target build.

8. **Verify the Worst Case Aufstartlatenz for startup-critical signals.** This field specifies the maximum time after ECU power-on before the signal is guaranteed valid. Startup sequences that consume signals before this latency has elapsed must handle the `InitWert` period explicitly.

9. **Use `Zykluszeit schnell` only when specified.** Many PDUs only define `Zykluszeit normal`. Using a fast cycle time where none is defined is a bus load violation.

10. **Contact the originating ECU team before using `S*` signals.** A `S*` entry means the signal is routed — its semantics and quality are governed by another bus segment's K-Matrix. The VLAN K-Matrix only documents the routing, not the signal definition.

---

## Domain Glossary

This glossary classifies terms for use in requirements. Black-box terms describe externally observable behaviour and are allowed at any requirement level (SWE.1 and above). White-box terms describe internal implementation details and are restricted to SWE.3/SWE.4 design and unit-test artefacts.

### Black-Box Terms (approved for SWE.1 requirements)

**Frame**
Definition: A network packet on the VLAN bus segment, identified by source/destination IP address and port. Each frame carries one or more PDUs. A frame is the unit of transmission and the unit of timeout detection.
Rationale: Observable from outside — a receiver either receives a frame within the timeout window or it does not.

**PDU (Protocol Data Unit)**
Definition: A logical grouping of related signals within a frame, identified by PDU-ID. Defines the timing contract (cycle time, send type) and is the atomic unit of signal delivery.
Rationale: Observable from outside — applications subscribe to a PDU and receive all its signals together on each cycle or event.

**Signal**
Definition: A named data item carried within a PDU, defined by a bit position and width. A signal encodes one physical measurement, status flag, or enumeration value.
Rationale: Observable from outside — the signal value and its physical interpretation are externally contractual.

**Physical value**
Definition: The real-world value of a signal after applying the linear conversion `physical = raw × Skalierung + Offset`. Expressed in the declared unit (e.g., m/s², W/m²).
Rationale: Observable from outside — this is the value the application consumes.

**InitWert (Init value)**
Definition: A reserved raw signal value indicating that the ECU has not yet produced a valid measurement after power-on. The application must not interpret the signal's physical value when the raw value equals InitWert.
Rationale: Observable from outside — the receiver can detect the "not yet valid" state.

**FehlerWert (Error value)**
Definition: A reserved raw signal value indicating an internal ECU fault. The application must not use the physical value when the raw value equals FehlerWert.
Rationale: Observable from outside — part of the fault signalling contract.

**Inaktiver Wert (Inactive value)**
Definition: A reserved raw signal value indicating that the function associated with the signal is currently not active (e.g., a feature is disabled or not equipped).
Rationale: Observable from outside — the receiver distinguishes between "feature inactive" and an active measurement.

**Botschaftszähler / BZ (Message counter / rolling counter)**
Definition: A 4-bit counter incremented by the sender with each PDU transmission. The receiver uses it to detect lost or replayed frames.
Rationale: Observable from outside — a discontinuity in the counter is an observable fault condition.

**Frame timeout**
Definition: The maximum interval between two consecutive receptions of the same frame. If this interval is exceeded, the receiver must treat all signals in the frame as invalid.
Rationale: Observable from outside — timeout is an externally contractual timing property.

**CRC (Cyclic Redundancy Check)**
Definition: An 8-bit checksum appended to a PDU. The receiver must validate it and discard the PDU if the check fails.
Rationale: Observable from outside — CRC validation failure is a detectable, externally observable fault.

**Service Discovery (SD)**
Definition: The SOME/IP or ViWi mechanism by which an ECU announces its available services to other ECUs on the network and negotiates subscriptions. SD frames are distinct from application data frames.
Rationale: Observable from outside — the presence or absence of a service announcement is an externally observable event.

**FunktionsCluster**
Definition: The functional domain classification of a signal or service, as declared in the K-Matrix (e.g., `02_Basefunction_Powertrain`, `06_Basefunction_ComfortLight`).
Rationale: Observable from outside — used to scope integration test coverage and requirement allocation.

**Worst Case Aufstartlatenz (Worst-case startup latency)**
Definition: The maximum time after ECU power-on before the signal is guaranteed to carry a valid, non-Init value. Expressed in ms.
Rationale: Observable from outside — a system-level timing constraint that affects startup sequence validation.

---

### White-Box Terms (restricted to SWE.3 / SWE.4 artefacts)

**StartByte / StartBit**
Definition: The physical bit position of a signal within the PDU byte array (StartByte is 1-based in the K-Matrix; StartBit is 0-based).
Rationale: Internal implementation detail of the signal extraction algorithm. Requirements must not specify bit positions; they must specify signal names and physical value contracts.

**Skalierung / Offset**
Definition: The linear conversion coefficients used to transform a raw integer value to a physical value.
Rationale: Internal encoding detail. Requirements must specify physical ranges and units; the Skalierung/Offset are implementation parameters of the codec.

**Rohwert (Raw value)**
Definition: The integer value transmitted on the wire before physical conversion.
Rationale: Internal encoding. Requirements must state behaviour in physical terms; raw values belong to the codec implementation.

**PDU-ID**
Definition: The numeric identifier of a PDU within a frame (hexadecimal).
Rationale: Network stack configuration detail. Requirements must not depend on PDU IDs; they must depend on signal names and timing contracts.

**MUX Signal / MUX Gruppe**
Definition: Multiplexer control fields that allow a PDU to carry different signal sets depending on the MUX value.
Rationale: Internal PDU layout detail. Requirements must describe the observable behaviour of each signal variant; the MUX mechanism is an encoding implementation.

**PDU-Typ = `intern`**
Definition: Internal K-Matrix marker indicating that this row describes an application data PDU (as opposed to a service handle or diagnostic PDU).
Rationale: Tool artefact of the K-Matrix authoring process; has no observable meaning outside the K-Matrix document.

**`_XIX_` separator**
Definition: The domain separator in SW function component column names (`<SoftwareFunctionName>_XIX_<FunctionCluster>_XIX_<ECU>`).
Rationale: A naming convention of the E3 SOME/IP service architecture toolchain. Not part of any observable behaviour; only relevant when reading or generating K-Matrix column headers programmatically.

**NrOfRepetition**
Definition: The number of times a PDU is retransmitted after an `OnChange` event.
Rationale: Internal transmission behaviour; observable only as additional bus load. Requirements must state the signal's update timing in physical terms (e.g., "updated within X ms of a change").
