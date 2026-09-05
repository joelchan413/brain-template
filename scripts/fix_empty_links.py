#!/usr/bin/env python3
"""
Fix Empty / Unresolved Wikilinks across the vault.
Scaffolds concept notes, lectures, quizzes, and assignment notes.
"""

import os
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def write_note(rel_path: str, content: str):
    p = ROOT / rel_path
    ensure_dir(p.parent)
    p.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Created: {rel_path}")

# ==============================================================================
# 1. CONCEPTS (03-Concepts/)
# ==============================================================================

CONCEPTS = {
    "Divide-and-Conquer.md": """---
title: Divide and Conquer
type: concept
tags: [concept, computer-science, algorithms, divide-and-conquer]
aliases: [D&C, Divide & Conquer]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Time-Complexity]]", "[[Recurrence-Relations-and-Master-Theorem]]", "[[COMS3110-Overview]]", "[[Computer-Science-MOC]]"]
---

# 🧠 Divide and Conquer

> [!NOTE] One-Sentence Definition (ELI5)
> Divide and Conquer is an algorithm design paradigm where a problem is broken down into two or more smaller subproblems of the same type, solved recursively, and their solutions combined to solve the original problem.

---

## 🔍 The Three Steps
1. **Divide**: Break the problem into subproblems of smaller sizes ($n/b$).
2. **Conquer**: Recursively solve each subproblem until reaching base cases ($n \le n_0$).
3. **Combine**: Merge solutions of subproblems into the overall solution.

---

## 💻 Classic Examples
- **Merge Sort**: Divide array in half, recursively sort both, merge in $O(n)$ $\implies O(n \log n)$.
- **Quick Sort**: Partition around pivot, recursively sort partitions $\implies O(n \log n)$ average.
- **Binary Search**: Divide search interval in half $\implies O(\log n)$.
- **Strassen's Matrix Multiplication**: Subdivide matrices into blocks $\implies O(n^{2.81})$.
- **Closest Pair of Points**: Divide points by vertical median line $\implies O(n \log n)$.

---

## ⚠️ Common Pitfalls
1. Failing to establish an efficient combine step (e.g., $O(n^2)$ combine ruins divide benefits).
2. Forgetting the recursive base case leading to stack overflow.
""",

    "Master-Theorem.md": """---
title: Master Theorem
type: concept
tags: [concept, computer-science, algorithms, recurrences]
aliases: [Master Method]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Recurrence-Relations-and-Master-Theorem]]", "[[Divide-and-Conquer]]", "[[Time-Complexity]]", "[[COMS3110-Overview]]"]
---

# 🧠 Master Theorem

> [!NOTE] One-Sentence Definition
> The Master Theorem provides a cookbook recipe for determining asymptotic runtime bounds for divide-and-conquer recurrence relations of the form $T(n) = aT(n/b) + f(n)$.

---

## 📐 General Recurrence Form
$$T(n) = a T(n/b) + f(n)$$
Where $a \ge 1$, $b > 1$, and $f(n)$ is the non-recursive work per level. Let $c_{\text{crit}} = \log_b a$.

---

## 🎯 The Three Cases
1. **Case 1 (Leaves Dominate)**: If $f(n) = O(n^{\log_b a - \epsilon})$ for some $\epsilon > 0$:
   $$T(n) = \Theta(n^{\log_b a})$$
2. **Case 2 (Even Balance)**: If $f(n) = \Theta(n^{\log_b a} \log^k n)$ for $k \ge 0$:
   $$T(n) = \Theta(n^{\log_b a} \log^{k+1} n)$$
3. **Case 3 (Root Dominates)**: If $f(n) = \Omega(n^{\log_b a + \epsilon})$ for some $\epsilon > 0$ AND regularity condition holds ($a f(n/b) \le c f(n)$ for $c < 1$):
   $$T(n) = \Theta(f(n))$$

---

## 🔗 Related Notes
- See comprehensive guide: [[Recurrence-Relations-and-Master-Theorem]]
""",

    "Recurrence-Relations-and-Master-Theorem.md": """---
title: Recurrence Relations and Master Theorem
type: concept
tags: [concept, computer-science, algorithms, math, recurrences]
aliases: [Recurrences, Master Theorem Guide]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Time-Complexity]]", "[[Master-Theorem]]", "[[Divide-and-Conquer]]", "[[COMS3110-Overview]]", "[[Mathematics-MOC]]"]
---

# 🧠 Recurrence Relations & Master Theorem

> [!NOTE] Executive Summary
> Techniques for solving recursive algorithm runtimes, including Substitution Method (Induction), Recursion Trees, and the Master Method.

---

## 🛠️ Method 1: Recursion Tree Method
Draw tree with branching factor $a$ and subproblem size $n/b^i$:
- Height: $h = \log_b n$.
- Total leaves: $a^{\log_b n} = n^{\log_b a}$.
- Level $i$ work: $a^i \cdot f(n/b^i)$.
- Total cost: $\sum_{i=0}^{\log_b n} a^i f(n/b^i)$.

---

## 🛠️ Method 2: Substitution Method
1. Guess the asymptotic form (e.g., $T(n) \le c n \log n$).
2. Use mathematical induction to prove $T(n) \le c n \log n$ for base case and inductive step.
3. Solve for constants $c > 0$ and $n_0 \ge 1$.

---

## 🛠️ Method 3: Master Method
See dedicated reference note: [[Master-Theorem]].
""",

    "Linear-Sorting-Algorithms.md": """---
title: Linear Sorting Algorithms
type: concept
tags: [concept, computer-science, algorithms, sorting]
aliases: [Counting Sort, Radix Sort, Bucket Sort]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Time-Complexity]]", "[[COMS3110-Overview]]", "[[Computer-Science-MOC]]"]
---

# 🧠 Linear Sorting Algorithms

> [!NOTE] Key Principle
> Comparison-based sorting has a theoretical lower bound of $\Omega(n \log n)$. Non-comparison sorting breaks this lower bound by exploiting input constraints to achieve $O(n)$ runtime.

---

## 📊 Linear Sort Comparison
| Algorithm | Time Complexity | Space Complexity | Key Condition | Stable? |
| :--- | :--- | :--- | :--- | :--- |
| **Counting Sort** | $O(n + k)$ | $O(n + k)$ | Keys are integers in range $[0, k]$ | ✅ Yes |
| **Radix Sort** | $O(d(n + k))$ | $O(n + k)$ | $d$ digits of base $k$ | ✅ Yes |
| **Bucket Sort** | $O(n)$ avg, $O(n^2)$ worst | $O(n + k)$ | Uniform distribution over $[0, 1)$ | ✅ Yes |
""",

    "Dynamic-Programming.md": """---
title: Dynamic Programming
type: concept
tags: [concept, computer-science, algorithms, dynamic-programming, optimization]
aliases: [DP, Memoization, Tabulation]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Time-Complexity]]", "[[Divide-and-Conquer]]", "[[Greedy-Algorithms]]", "[[COMS3110-Overview]]"]
---

# 🧠 Dynamic Programming (DP)

> [!NOTE] One-Sentence Definition (ELI5)
> Dynamic Programming is an optimization technique that solves complex problems by breaking them into overlapping subproblems and storing the results to avoid redundant calculations.

---

## 🔑 Core Properties Required
1. **Optimal Substructure**: The optimal solution to the problem contains within it optimal solutions to subproblems.
2. **Overlapping Subproblems**: Recursive algorithm visits the same subproblems repeatedly.

---

## 🎯 Approaches
- **Top-Down (Memoization)**: Recursive approach with cache lookup.
- **Bottom-Up (Tabulation)**: Iterative filling of DP table in topological order of dependencies.

---

## 📚 Canonical DP Patterns
- **0/1 Knapsack**: $DP[i][w] = \max(DP[i-1][w], DP[i-1][w-w_i] + v_i)$
- **Longest Common Subsequence (LCS)**
- **Matrix Chain Multiplication**
- **Bellman-Ford Shortest Path**
- **Floyd-Warshall All-Pairs Shortest Path**
""",

    "Greedy-Algorithms.md": """---
title: Greedy Algorithms
type: concept
tags: [concept, computer-science, algorithms, greedy, optimization]
aliases: [Greedy Choice Property]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Dynamic-Programming]]", "[[Time-Complexity]]", "[[Graph-Algorithms-Advanced]]", "[[COMS3110-Overview]]"]
---

# 🧠 Greedy Algorithms

> [!NOTE] One-Sentence Definition
> A greedy algorithm makes the locally optimal choice at each stage with the hope of finding a global optimum.

---

## 🔑 Key Invariants & Proof Techniques
1. **Greedy Choice Property**: A globally optimal solution can be arrived at by making a locally optimal choice.
2. **Optimal Substructure**: The problem exhibits optimal substructure.

### Proving Correctness:
- **Exchange Argument**: Show that any optimal solution differing from the greedy solution can be transformed into the greedy solution without worsening objective value.
- **Greedy Stays Ahead**: Prove that at every step $k$, the greedy solution is at least as good as any other candidate.

---

## 📚 Standard Examples
- **Interval Scheduling**: Sort by earliest finish time.
- **Huffman Coding**: Priority queue min-merge.
- **Fractional Knapsack**: Sort by value-to-weight ratio $v_i / w_i$.
- **Kruskal's & Prim's MST**: Pick lightest safe edge.
- **Dijkstra's Shortest Path**: Expand closest unvisited vertex.
""",

    "Graph-Algorithms-Advanced.md": """---
title: Graph Algorithms Advanced
type: concept
tags: [concept, computer-science, algorithms, graphs]
aliases: [Graph Theory, Shortest Paths, MST, Network Flow]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Time-Complexity]]", "[[Greedy-Algorithms]]", "[[Dynamic-Programming]]", "[[COMS3110-Overview]]"]
---

# 🧠 Advanced Graph Algorithms

> [!NOTE] Overview
> Core algorithms for traversing, pathfinding, clustering, spanning, and flowing across directed and undirected graphs.

---

## 🗺️ Algorithmic Landscape
| Problem | Algorithm | Time Complexity | Notes |
| :--- | :--- | :--- | :--- |
| **Connectivity & Cycles** | BFS / DFS | $O(V + E)$ | Bipartite testing, topological sort |
| **Topological Sort** | Kahn's / DFS Post-order | $O(V + E)$ | Valid on DAGs only |
| **Strongly Connected (SCC)** | Kosaraju / Tarjan | $O(V + E)$ | Condensation DAG |
| **Single-Source Shortest Path** | Dijkstra | $O(E + V \log V)$ | Non-negative weights |
| **Single-Source with Negative** | Bellman-Ford | $O(V \cdot E)$ | Detects negative cycles |
| **All-Pairs Shortest Path** | Floyd-Warshall | $O(V^3)$ | DP matrix formulation |
| **Minimum Spanning Tree** | Kruskal / Prim | $O(E \log V)$ | Greedy cut property |
| **Max Flow / Min Cut** | Ford-Fulkerson / Edmonds-Karp | $O(V E^2)$ | Augmenting paths |
""",

    "NP-Completeness.md": """---
title: NP-Completeness
type: concept
tags: [concept, computer-science, complexity-theory, np-completeness]
aliases: [P vs NP, Polynomial Reduction]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Time-Complexity]]", "[[COMS3110-Overview]]", "[[Computer-Science-MOC]]"]
---

# 🧠 NP-Completeness & Complexity Theory

> [!NOTE] One-Sentence Definition
> NP-Complete problems are the hardest problems in NP; if any single NP-Complete problem can be solved in polynomial time ($P = NP$), all problems in NP can be solved in polynomial time.

---

## 🎯 Complexity Classes
- **P**: Decision problems solvable in deterministic polynomial time ($O(n^k)$).
- **NP**: Decision problems whose solutions are verifiable in polynomial time.
- **NP-Hard**: At least as hard as any problem in NP (every problem in NP reduces to it in polynomial time).
- **NP-Complete**: Both in NP and NP-Hard ($NPC = NP \cap NP\text{-Hard}$).

---

## 🔄 Proving NP-Completeness
To prove language $L$ is NP-Complete:
1. Show $L \in NP$ (provide a certificate and polynomial-time verifier).
2. Select a known NP-Complete problem $X$ (e.g., 3-SAT, Vertex Cover, Clique).
3. Construct a polynomial-time reduction $X \le_p L$.
4. Prove that $x \in X \iff f(x) \in L$.
""",

    "Operating-Systems-Overview.md": """---
title: Operating Systems Overview
type: concept
tags: [concept, computer-engineering, operating-systems, cpre3080]
aliases: [OS Fundamentals, Kernel Architecture]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Process-Management]]", "[[Threads-and-Concurrency]]", "[[CPU-Scheduling]]", "[[CPRE3080-Overview]]", "[[Engineering-MOC]]"]
---

# 🧠 Operating Systems Overview

> [!NOTE] One-Sentence Definition (ELI5)
> An operating system is a fundamental software layer that manages computer hardware resources (CPU, memory, storage, I/O devices) and provides a secure, abstracted execution environment for user applications.

---

## 🧱 Kernel Architecture
- **Monolithic Kernel** (e.g., Linux): All OS services (VFS, drivers, networking, scheduler) run in privileged kernel space.
- **Microkernel** (e.g., QNX, seL4): Only minimal primitives (IPC, low-level scheduling, memory paging) run in kernel space; servers run in user mode.
- **Dual-Mode Operation**: User Mode (ring 3) vs Kernel Mode (ring 0) enforced by hardware status bit.
""",

    "Process-Management.md": """---
title: Process Management
type: concept
tags: [concept, computer-engineering, operating-systems, processes, cpre3080]
aliases: [PCB, Process Lifecycle, fork and exec]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Operating-Systems-Overview]]", "[[Threads-and-Concurrency]]", "[[CPU-Scheduling]]", "[[CPRE3080-Overview]]"]
---

# 🧠 Process Management & Lifecycle

> [!NOTE] Definition
> A process is a program in execution, consisting of program code (text), program counter, stack, data section, and heap.

---

## 🔄 Process States & PCB
- **States**: `New` $\to$ `Ready` $\leftrightarrow$ `Running` $\to$ `Terminated` (or `Waiting` for I/O).
- **Process Control Block (PCB)**: Stores PID, register state, program counter, open file descriptors, scheduling priority, and memory limits.

---

## ⚙️ Core UNIX System Calls
- `fork()`: Clones calling process with separate address space (Copy-On-Write).
- `execvp()` / `exec()`: Replaces process memory image with a new executable.
- `wait()` / `waitpid()`: Blocks parent until child process terminates (prevents zombie processes).
- `exit()`: Terminates process execution.
""",

    "Threads-and-Concurrency.md": """---
title: Threads and Concurrency
type: concept
tags: [concept, computer-engineering, operating-systems, concurrency, pthreads]
aliases: [Multithreading, POSIX Threads]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Process-Management]]", "[[Synchronization-Primitives]]", "[[Deadlocks-and-Bankers-Algorithm]]", "[[CPRE3080-Overview]]"]
---

# 🧠 Threads and Concurrency

> [!NOTE] Definition
> A thread (lightweight process) is the smallest unit of CPU execution, sharing address space, code, data, and OS resources with sibling threads while maintaining its own registers and stack.

---

## 🆚 Processes vs Threads
| Attribute | Process | Thread |
| :--- | :--- | :--- |
| **Address Space** | Isolated (separate virtual memory) | Shared with sibling threads |
| **Creation Overhead** | High (`fork()`) | Low (`pthread_create()`) |
| **Context Switch** | Expensive (TLB flush, page table reload) | Fast (registers and stack pointer only) |
| **Inter-communication**| IPC (pipes, sockets, shared memory) | Direct memory access (requires synchronization) |
""",

    "CPU-Scheduling.md": """---
title: CPU Scheduling
type: concept
tags: [concept, computer-engineering, operating-systems, scheduling]
aliases: [Scheduler, Round Robin, FCFS, SJF]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Process-Management]]", "[[Threads-and-Concurrency]]", "[[CPRE3080-Overview]]"]
---

# 🧠 CPU Scheduling Algorithms

> [!NOTE] Definition
> The CPU scheduler determines which ready process is allocated CPU core time based on performance criteria.

---

## 📊 Scheduling Criteria
- **CPU Utilization**: Percentage of time CPU is busy.
- **Throughput**: Processes completed per unit time.
- **Turnaround Time**: Total time from process arrival to termination ($T_{\text{finish}} - T_{\text{arrival}}$).
- **Waiting Time**: Time spent waiting in the ready queue.
- **Response Time**: Time from submission to first output.

---

## ⚙️ Algorithms
1. **FCFS (First-Come, First-Served)**: Non-preemptive, subject to convoy effect.
2. **SJF (Shortest Job First)**: Provably minimal average waiting time; requires burst time estimation.
3. **Round Robin (RR)**: Preemptive time-slicing with quantum $q$.
4. **Multilevel Feedback Queue (MLFQ)**: Adaptive dynamic priority queues.
""",

    "Synchronization-Primitives.md": """---
title: Synchronization Primitives
type: concept
tags: [concept, computer-engineering, operating-systems, concurrency, mutex]
aliases: [Mutex, Semaphores, Condition Variables]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Threads-and-Concurrency]]", "[[Deadlocks-and-Bankers-Algorithm]]", "[[CPRE3080-Overview]]"]
---

# 🧠 Synchronization Primitives

> [!NOTE] Definition
> Software mechanisms and hardware instructions used to coordinate concurrent threads and prevent race conditions on shared memory.

---

## 🔒 Primitives
1. **Mutex (`pthread_mutex_t`)**: Binary mutual exclusion lock with ownership.
2. **Counting Semaphore (`sem_t`)**: Integer counter representing available resource units.
   - `sem_wait()` / $P()$: Decrements; blocks if $\le 0$.
   - `sem_post()` / $V()$: Increments; wakes waiting thread.
3. **Condition Variable (`pthread_cond_t`)**: Allows threads to block until a condition predicate is met (`wait`, `signal`, `broadcast`).
4. **Atomic Instructions**: Hardware-supported `compare-and-swap` (CAS), `test-and-set`.
""",

    "Deadlocks-and-Bankers-Algorithm.md": """---
title: Deadlocks and Banker's Algorithm
type: concept
tags: [concept, computer-engineering, operating-systems, deadlocks]
aliases: [Deadlock Coffman Conditions, Bankers Algorithm]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Synchronization-Primitives]]", "[[Process-Management]]", "[[CPRE3080-Overview]]"]
---

# 🧠 Deadlocks & Banker's Algorithm

> [!NOTE] Definition
> A deadlock is a state where a set of processes are permanently blocked because each process is holding a resource and waiting for another resource acquired by another process in the set.

---

## 🛑 The Four Coffman Conditions (Must all hold simultaneously)
1. **Mutual Exclusion**: At least one resource is held in a non-shareable mode.
2. **Hold and Wait**: A process holds $\ge 1$ resource while waiting to acquire additional resources.
3. **No Preemption**: Resources cannot be forcibly confiscated.
4. **Circular Wait**: A closed chain of processes exists where $P_0$ waits for $P_1$, $\dots$, $P_n$ waits for $P_0$.

---

## 🏦 Banker's Algorithm
Safety algorithm for resource allocation avoidance in systems with multiple instances of resources:
- Vectors: `Available`, `Allocation`, `Max`, `Need = Max - Allocation`.
- Find process $P_i$ whose $\text{Need}_i \le \text{Available}$.
- Assume $P_i$ runs and returns resources: $\text{Available} \leftarrow \text{Available} + \text{Allocation}_i$.
- If all processes can terminate, system state is **Safe**.
""",

    "Virtual-Memory-and-Paging.md": """---
title: Virtual Memory and Paging
type: concept
tags: [concept, computer-engineering, operating-systems, memory, paging]
aliases: [Page Tables, TLB, Page Fault]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Operating-Systems-Overview]]", "[[Process-Management]]", "[[CPRE3080-Overview]]"]
---

# 🧠 Virtual Memory & Paging

> [!NOTE] Definition
> Virtual memory is a memory management capability of an OS that creates the illusion of a large, contiguous, isolated address space for each process using hardware address translation (MMU).

---

## 📄 Address Translation & Page Tables
- **Virtual Address**: `[ Virtual Page Number (VPN) | Offset ]`.
- **Physical Address**: `[ Physical Frame Number (PFN) | Offset ]`.
- **Translation Lookaside Buffer (TLB)**: Fast hardware cache for VPN $\to$ PFN translations.
- **Page Fault**: Interrupt triggered when requested page is not in physical RAM (requires disk swap fetch).
- **Page Replacement**: LRU (Least Recently Used), FIFO, Clock algorithm.
""",

    "File-Systems-and-IO.md": """---
title: File Systems and I/O
type: concept
tags: [concept, computer-engineering, operating-systems, filesystems]
aliases: [Inodes, VFS, Ext4]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Operating-Systems-Overview]]", "[[Linux-Systems-Programming]]", "[[CPRE3080-Overview]]"]
---

# 🧠 File Systems & I/O Subsystems

> [!NOTE] Definition
> File systems provide persistent storage abstraction, translating human-readable directory structures and filenames into raw sector/block layouts on physical storage.

---

## 🗂️ Inode-Based Architecture (UNIX / Linux)
- **Inode**: Data structure containing file metadata (size, permissions, timestamps, block pointers). Does **not** store filename.
- **Directory**: Special file mapping filenames to Inode numbers.
- **Hard Link**: Directory entry pointing directly to an existing Inode.
- **Symbolic (Soft) Link**: File containing a path string to another target file.
""",

    "OS-Security-and-Protection.md": """---
title: OS Security and Protection
type: concept
tags: [concept, computer-engineering, operating-systems, security]
aliases: [Access Control, Ring Privileges]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Operating-Systems-Overview]]", "[[Linux-Systems-Programming]]", "[[CPRE3080-Overview]]"]
---

# 🧠 OS Security & Protection

> [!NOTE] Definition
> Mechanisms that control access of programs, processes, and users to system resources (CPU, memory, files, hardware devices).

---

## 🛡️ Core Protection Principles
1. **Principle of Least Privilege (PoLP)**: Give entities only the minimum capabilities needed.
2. **Access Control Matrices / ACLs**: Role-based access control (RBAC) and discretionary access control (DAC: `rwx` permissions).
3. **Memory Safety & ASLR**: Address Space Layout Randomization, non-executable stack ($W \oplus X$), stack canaries.
""",

    "Linux-Systems-Programming.md": """---
title: Linux Systems Programming
type: concept
tags: [concept, computer-engineering, linux, c-programming, systems]
aliases: [POSIX APIs, System Calls]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Operating-Systems-Overview]]", "[[Process-Management]]", "[[CPRE3080-Overview]]"]
---

# 🧠 Linux Systems Programming

> [!NOTE] Definition
> Low-level C programming interfacing directly with the Linux kernel via POSIX system calls.

---

## 💻 Essential System Calls
- **File I/O**: `open()`, `read()`, `write()`, `close()`, `lseek()`, `dup2()`.
- **Process Control**: `fork()`, `execvp()`, `waitpid()`, `pipe()`.
- **Signal Handling**: `signal()`, `sigaction()`, `kill()`.
- **Memory Mapping**: `mmap()`, `munmap()`.
""",

    "Wireless-Threat-Models.md": """---
title: Wireless Threat Models
type: concept
tags: [concept, cybersecurity, wireless, cpre4370]
aliases: [RF Security Threats, Wireless Attack Vectors]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[WPA2-WPA3-Protocols]]", "[[Rogue-APs-and-Evil-Twins]]", "[[CPRE4370-Overview]]"]
---

# 🧠 Wireless Threat Models & Attacks

> [!NOTE] Overview
> Analysis of adversary capabilities, attack vectors, and eavesdropping risks specific to shared RF (radio frequency) spectrum communications.

---

## 🎯 Threat Categories
1. **Passive Attacks**: Eavesdropping, traffic analysis, frame sniffing (`airodump-ng`).
2. **Active Attacks**: Deauthentication flooding, Evil Twin APs, replay attacks, man-in-the-middle (MitM).
3. **Jamming & Physical Layer DOS**: Constant RF jamming, reactive preamble jamming.
""",

    "WPA2-WPA3-Protocols.md": """---
title: WPA2 and WPA3 Security Protocols
type: concept
tags: [concept, cybersecurity, wireless, cryptography, cpre4370]
aliases: [4-Way Handshake, SAE, Dragonblood]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Wireless-Threat-Models]]", "[[Wireless-Authentication-EAP]]", "[[CPRE4370-Overview]]"]
---

# 🧠 WPA2 vs WPA3 Security Protocols

> [!NOTE] Key Difference
> WPA2 relies on a 4-Way Handshake vulnerable to offline dictionary attacks if the PMK is captured. WPA3 replaces PSK with Simultaneous Authentication of Equals (SAE) providing forward secrecy.

---

## 🔑 Protocol Breakdown
- **WPA2 (IEEE 802.11i)**: Uses AES-CCMP encryption; 4-Way Handshake derives PTK (Pairwise Transient Key) from PMK/ANonce/SNonce.
- **WPA3**: Uses Dragonfly (SAE) handshake resistant to offline dictionary attacks; protected management frames (PMF) mandatory; 192-bit cryptographic suite option.
""",

    "Wireless-Authentication-EAP.md": """---
title: Wireless Authentication and EAP
type: concept
tags: [concept, cybersecurity, wireless, 802-1x, radius]
aliases: [EAP-TLS, EAP-PEAP, RADIUS]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[WPA2-WPA3-Protocols]]", "[[Wireless-Threat-Models]]", "[[CPRE4370-Overview]]"]
---

# 🧠 Wireless Enterprise Authentication & EAP

> [!NOTE] Definition
> IEEE 802.1X enterprise network authentication using the Extensible Authentication Protocol (EAP) and RADIUS authentication servers (e.g., eduroam).

---

## 🔐 EAP Methods
- **EAP-TLS**: Mutual certificate-based authentication (most secure, no shared passwords).
- **PEAP / EAP-MSCHAPv2**: Server authenticated via TLS tunnel; client authenticated via MSCHAPv2 credentials.
- **EAP-TTLS**: Tunneling protocol supporting legacy client credentials.
""",

    "Rogue-APs-and-Evil-Twins.md": """---
title: Rogue APs and Evil Twins
type: concept
tags: [concept, cybersecurity, wireless, attacks, mitm]
aliases: [Evil Twin, Rogue Access Point]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Wireless-Threat-Models]]", "[[WPA2-WPA3-Protocols]]", "[[CPRE4370-Overview]]"]
---

# 🧠 Rogue APs & Evil Twin Attacks

> [!NOTE] Definition
> An Evil Twin is a rogue Wi-Fi access point masquerading as a legitimate network by spoofing its SSID and BSSID MAC address to lure wireless clients into connecting and intercepting traffic.

---

## ⚔️ Attack Execution
1. Send deauthentication frames to kick client off legitimate AP.
2. Broadcast identical SSID with higher signal strength ($RSSI$).
3. Client automatically reconnects to attacker's AP.
4. Attacker launches captive portal phishing or SSL stripping.
""",

    "Bluetooth-BLE-Security.md": """---
title: Bluetooth and BLE Security
type: concept
tags: [concept, cybersecurity, wireless, bluetooth, ble]
aliases: [BLE Pairing, BlueBorne, BLE Cryptography]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Wireless-Threat-Models]]", "[[IoT-Sensor-Network-Security]]", "[[CPRE4370-Overview]]"]
---

# 🧠 Bluetooth Classic & BLE Security

> [!NOTE] Definition
> Security architecture and vulnerability vectors in IEEE 802.15.1 and Bluetooth Low Energy (BLE) peripheral protocols.

---

## 🔒 BLE Pairing Association Models
- **Just Works**: Unauthenticated ECDH key exchange; vulnerable to active MitM.
- **Passkey Entry**: 6-digit numeric comparison entry on one or both devices.
- **Numeric Comparison** (LE Secure Connections): Both devices display 6-digit number; users verify match.
- **Out of Band (OOB)**: Key exchange through NFC.
""",

    "Cellular-Security-and-IMSI.md": """---
title: Cellular Security and IMSI Catchers
type: concept
tags: [concept, cybersecurity, cellular, lte, 5g, stingray]
aliases: [Stingray, IMSI Catcher, 4G/5G Security]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Wireless-Threat-Models]]", "[[CPRE4370-Overview]]"]
---

# 🧠 Cellular Security & IMSI Catchers

> [!NOTE] Definition
> Analysis of baseband cellular protocols (2G/3G/4G/5G) and false base station (IMSI Catcher / Stingray) attacks exploiting unauthenticated broadcast channels.

---

## 📡 Cellular Evolution Security
- **2G (GSM)**: One-way authentication (network authenticates client, but client does not authenticate tower). Enables IMSI catchers.
- **4G LTE**: Mutual authentication (AKA protocol), but broadcast unencrypted broadcast messages allow location tracking.
- **5G**: Introduction of SUPI (Subscription Permanent Identifier) encryption via SUCI (Subscription Concealed Identifier).
""",

    "IoT-Sensor-Network-Security.md": """---
title: IoT and Sensor Network Security
type: concept
tags: [concept, cybersecurity, iot, zigbee, lora]
aliases: [Zigbee, LoRaWAN, 6LoWPAN]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Bluetooth-BLE-Security]]", "[[Wireless-Threat-Models]]", "[[CPRE4370-Overview]]"]
---

# 🧠 IoT & Sensor Network Security

> [!NOTE] Definition
> Security paradigms for resource-constrained embedded nodes operating on low-power wireless mesh networks (Zigbee, Z-Wave, LoRaWAN, 802.15.4).

---

## ⚡ Constraints & Vulnerabilities
- Limited hardware compute/memory precludes heavy public-key cryptography.
- Default link keys (e.g., Zigbee "ZigBeeAlliance09" default key).
- Physical tampering and firmware extraction via UART/JTAG.
""",

    "Engineering-Ethics-Overview.md": """---
title: Engineering Ethics Overview
type: concept
tags: [concept, ethics, engineering-ethics, cpre2320]
aliases: [Professional Ethics, Engineering Responsibility]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Codes-of-Ethics]]", "[[Ethical-Decision-Frameworks]]", "[[CPRE2320-Overview]]"]
---

# 🧠 Engineering Ethics Overview

> [!NOTE] Definition
> The study of moral issues and decisions confronting individuals and organizations involved in engineering and technological design.

---

## 🌟 The Primary Canon
Engineers shall hold paramount the **safety, health, and welfare of the public** in the performance of their professional duties.
""",

    "Ethical-Decision-Frameworks.md": """---
title: Ethical Decision Frameworks
type: concept
tags: [concept, ethics, philosophy, cpre2320]
aliases: [Utilitarianism, Deontology, Virtue Ethics]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Engineering-Ethics-Overview]]", "[[Codes-of-Ethics]]", "[[CPRE2320-Overview]]"]
---

# 🧠 Ethical Decision-Making Frameworks

> [!NOTE] Overview
> Philosophical frameworks applied to resolve moral dilemmas in engineering practice.

---

## ⚖️ Core Frameworks
1. **Utilitarianism (Consequentialism)**: Maximize the greatest good for the greatest number of people (Cost-Benefit Analysis).
2. **Deontology (Duty Ethics / Kantian)**: Actions are intrinsically right or wrong regardless of consequences; respect categorical imperatives and rights.
3. **Virtue Ethics (Aristotelian)**: Emphasizes moral character and integrity (honesty, courage, fairness).
4. **Care Ethics**: Emphasizes relational interconnectedness and minimizing harm to vulnerable parties.
""",

    "Codes-of-Ethics.md": """---
title: Professional Codes of Ethics
type: concept
tags: [concept, ethics, ieee, acm, nspe, cpre2320]
aliases: [IEEE Code of Ethics, ACM Code of Ethics, NSPE]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Engineering-Ethics-Overview]]", "[[Whistleblowing-and-Professional-Responsibility]]", "[[CPRE2320-Overview]]"]
---

# 🧠 Professional Codes of Ethics (IEEE & ACM)

> [!NOTE] Definition
> Formalized ethical standards established by professional engineering societies governing professional conduct, conflicts of interest, and public safety.

---

## 📜 Key Tenets
- **IEEE Code of Ethics**: Uphold highest integrity; reject bribery; avoid conflicts of interest; treat all persons fairly.
- **ACM Code of Ethics**: Contribute to society and human well-being; avoid harm; be honest and trustworthy; respect privacy and intellectual property.
""",

    "Whistleblowing-and-Professional-Responsibility.md": """---
title: Whistleblowing and Professional Responsibility
type: concept
tags: [concept, ethics, whistleblowing, legal, cpre2320]
aliases: [Whistleblowing, Moral Courage]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Engineering-Ethics-Overview]]", "[[Engineering-Disasters-and-Case-Studies]]", "[[CPRE2320-Overview]]"]
---

# 🧠 Whistleblowing & Professional Responsibility

> [!NOTE] Definition
> The disclosure by an employee of confidential organizational information relating to illegal conduct, gross waste of funds, safety hazards, or public danger.

---

## ⚖️ De George's Criteria for Justified Whistleblowing
1. The company's product or policy will do serious and considerable harm to the public.
2. The engineer has reported the threat to their immediate superior and exhausted internal remedies.
3. The engineer has brought the grievance through the board of directors.
4. The engineer has documented, convincing evidence that would satisfy a reasonable observer.
5. The engineer has good reason to believe that going public will prevent the serious harm.
""",

    "Intellectual-Property-in-Tech.md": """---
title: Intellectual Property in Tech
type: concept
tags: [concept, ethics, law, ip, patents, copyrights, cpre2320]
aliases: [Patents, Copyrights, Trade Secrets, Open Source Licenses]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Engineering-Ethics-Overview]]", "[[CPRE2320-Overview]]"]
---

# 🧠 Intellectual Property in Technology

> [!NOTE] Definition
> Legal protections granting creators exclusive rights over technological inventions, source code, and design specifications.

---

## 📜 Forms of IP
- **Patents**: Protect novel, non-obvious utility inventions/algorithms for 20 years.
- **Copyrights**: Protect fixed original expressions (source code, documentation).
- **Trade Secrets**: Protect proprietary formulas or algorithms kept confidential (e.g., proprietary search engine code).
- **Open Source Licensing**: Permissive (MIT, Apache 2.0, BSD) vs Copyleft (GPL v3, LGPL).
""",

    "AI-Ethics-and-Data-Privacy.md": """---
title: AI Ethics and Data Privacy
type: concept
tags: [concept, ethics, ai, machine-learning, privacy, gdpr, cpre2320]
aliases: [Algorithmic Bias, Data Privacy, GDPR]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Engineering-Ethics-Overview]]", "[[CPRE2320-Overview]]"]
---

# 🧠 AI Ethics & Data Privacy

> [!NOTE] Definition
> Ethical, legal, and societal dimensions of automated decision systems, machine learning models, and large-scale data harvesting.

---

## 🎯 Core Challenges
1. **Algorithmic Bias**: Training data reflecting historical human inequities leading to biased classification.
2. **Surveillance & Consent**: Notice and choice, right to erasure (GDPR, CCPA).
3. **Accountability & Explainability**: The "Black Box" problem in high-stakes decisions (criminal justice, healthcare).
""",

    "DEI-in-Engineering-Workplaces.md": """---
title: Diversity, Equity, and Inclusion in Engineering
type: concept
tags: [concept, ethics, dei, workplace, engineering, cpre2320]
aliases: [DEI in Tech, Workplace Inclusion]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Engineering-Ethics-Overview]]", "[[CPRE2320-Overview]]"]
---

# 🧠 Diversity, Equity, and Inclusion in Engineering

> [!NOTE] Definition
> Principles and practices fostering equitable access, representative collaboration, and inclusive workplaces in engineering teams.
""",

    "Engineering-Disasters-and-Case-Studies.md": """---
title: Engineering Disasters and Case Studies
type: concept
tags: [concept, ethics, case-studies, therac-25, challenger, cpre2320]
aliases: [Engineering Failures, Therac-25, Challenger Disaster]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Engineering-Ethics-Overview]]", "[[Whistleblowing-and-Professional-Responsibility]]", "[[CPRE2320-Overview]]"]
---

# 🧠 Engineering Disasters & Case Studies

> [!NOTE] Overview
> Historical technological failures analyzed to extract lessons in software safety, management pressure, and ethical accountability.

---

## 💥 Canonical Case Studies
- **Therac-25 Radiation Machine (1985–1987)**: Race conditions in software interlocks caused lethal overdoses due to removal of hardware safety interlocks.
- **Space Shuttle Challenger (1986)**: O-ring blow-by caused by extreme cold; engineers' safety concerns overridden by management.
- **Boeing 737 MAX MCAS (2018–2019)**: Single sensor reliance and concealed automated pitch control systems.
""",

    "Agile-and-Scrum-for-Hardware-Software.md": """---
title: Agile and Scrum for Hardware and Software
type: concept
tags: [concept, senior-design, agile, scrum, cpre4910]
aliases: [Agile Framework, Scrum Sprints]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Requirements-Engineering-and-User-Stories]]", "[[System-Architecture-and-Design-Patterns]]", "[[CPRE4910-Overview]]"]
---

# 🧠 Agile & Scrum for Engineering Projects

> [!NOTE] Definition
> Iterative project management methodology organizing team workflows into fixed-length sprints, continuous client integration, and empirical process control.
""",

    "Requirements-Engineering-and-User-Stories.md": """---
title: Requirements Engineering and User Stories
type: concept
tags: [concept, senior-design, requirements, engineering, cpre4910]
aliases: [Functional Requirements, User Stories]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Agile-and-Scrum-for-Hardware-Software]]", "[[CPRE4910-Overview]]"]
---

# 🧠 Requirements Engineering & User Stories

> [!NOTE] Definition
> The systematic process of defining, documenting, and validating functional and non-functional requirements for an engineering system.
""",

    "System-Architecture-and-Design-Patterns.md": """---
title: System Architecture and Design Patterns
type: concept
tags: [concept, senior-design, architecture, system-design, cpre4910]
aliases: [System Architecture, Design Patterns]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Agile-and-Scrum-for-Hardware-Software]]", "[[CPRE4910-Overview]]"]
---

# 🧠 System Architecture & Design Patterns

> [!NOTE] Definition
> High-level decomposition of hardware/software systems into subsystems, interfaces, communication buses, and data pipelines.
""",

    "Engineering-Standards-and-Compliance.md": """---
title: Engineering Standards and Compliance
type: concept
tags: [concept, senior-design, standards, ieee, iso, cpre4910]
aliases: [IEEE Standards, ISO/IEC Compliance]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Design-Risk-Assessment-and-Mitigation]]", "[[CPRE4910-Overview]]"]
---

# 🧠 Engineering Standards & Compliance

> [!NOTE] Definition
> Technical specifications, guidelines, and safety standards established by standards bodies (IEEE, ISO, IEC, NIST, FCC) that products must adhere to.
""",

    "Design-Risk-Assessment-and-Mitigation.md": """---
title: Design Risk Assessment and Mitigation
type: concept
tags: [concept, senior-design, risk-management, fmea, cpre4910]
aliases: [FMEA, Risk Matrix, Mitigation Plans]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[Engineering-Standards-and-Compliance]]", "[[CPRE4910-Overview]]"]
---

# 🧠 Design Risk Assessment & Mitigation

> [!NOTE] Definition
> The proactive identification, quantification (severity $\times$ occurrence $\times$ detection), and mitigation of technical, financial, and safety risks.
""",

    "Technical-Documentation-and-Reports.md": """---
title: Technical Documentation and Reports
type: concept
tags: [concept, senior-design, documentation, engineering, cpre4910]
aliases: [Design Documents, Technical Writing]
created: 2026-08-20
updated: 2026-08-20
status: evergreen
related: ["[[System-Architecture-and-Design-Patterns]]", "[[CPRE4910-Overview]]"]
---

# 🧠 Technical Documentation & Design Reports

> [!NOTE] Definition
> Professional engineering reports capturing system specifications, trade-off analyses, test plans, and architectural schematics for stakeholders.
"""
}

# ==============================================================================
# 2. LECTURES
# ==============================================================================

LECTURES = {
    "02-Courses/CPRE3080/Lectures/2026-08-24-CPRE3080-L01.md": """---
title: "CPR E 3080 L01: Introduction to Operating Systems"
type: lecture
course: "[[CPRE3080-Overview]]"
tags: [lecture, cpre3080, operating-systems, computer-engineering]
date: 2026-08-24
professor: "Iowa State ECpE Department"
topics: ["Kernel Architecture", "Dual-Mode Operation", "System Calls"]
---

# 🎓 CPR E 3080 L01: Introduction to Operating Systems

> [!SUMMARY] 30-Second Elevator Summary
> Overview of operating system roles as resource allocator and control program. Introduced kernel vs user mode separation and hardware protection mechanisms.

---

## 📌 Key Takeaways
- User mode (Ring 3) vs Kernel mode (Ring 0) prevents rogue programs from corrupting hardware or other processes.
- System calls act as the programmatic gateway for applications to request kernel services.

---

## 🔗 Related Concepts
- [[Operating-Systems-Overview]]
- [[Process-Management]]
""",

    "02-Courses/CPRE2320/Lectures/2026-08-25-CPRE2320-L01.md": """---
title: "CPR E 2320 L01: Course Intro & Engineering Ethics Foundations"
type: lecture
course: "[[CPRE2320-Overview]]"
tags: [lecture, cpre2320, engineering-ethics]
date: 2026-08-25
professor: "Iowa State ECpE Department"
topics: ["Engineering Ethics", "IEEE/ACM Codes", "Public Safety"]
---

# 🎓 CPR E 2320 L01: Course Intro & Engineering Ethics

> [!SUMMARY] 30-Second Elevator Summary
> Introduction to professional ethics for computer and electrical engineers, focusing on public safety obligation and IEEE/ACM professional codes.

---

## 🔗 Related Concepts
- [[Engineering-Ethics-Overview]]
- [[Codes-of-Ethics]]
""",

    "02-Courses/CPRE4910/Lectures/2026-08-25-CPRE4910-Kickoff.md": """---
title: "CPR E 4910 Kickoff: Senior Design Project Launch"
type: lecture
course: "[[CPRE4910-Overview]]"
tags: [lecture, cpre4910, senior-design]
date: 2026-08-25
professor: "Senior Design Faculty"
topics: ["Team Formation", "Client Requirements", "Sprint Planning"]
---

# 🎓 CPR E 4910: Senior Design Project Kickoff

> [!SUMMARY] 30-Second Elevator Summary
> Semester launch for Senior Design Project I. Established team expectations, client deliverables, and Agile/Scrum milestone structures.

---

## 🔗 Related Concepts
- [[Agile-and-Scrum-for-Hardware-Software]]
- [[Requirements-Engineering-and-User-Stories]]
""",

    "02-Courses/CPRE2320/Lectures/Discussion-Therac-25-Software-Safety.md": """---
title: "CPR E 2320 Discussion: Therac-25 & Software Safety"
type: lecture
course: "[[CPRE2320-Overview]]"
tags: [discussion, case-study, cpre2320, ethics, therac-25]
date: 2026-08-25
topics: ["Therac-25", "Race Conditions", "Safety Critical Systems"]
---

# 🎓 CPR E 2320 Case Study: Therac-25 Software Safety

> [!SUMMARY] Case Summary
> Analysis of the Therac-25 medical linear accelerator accidents caused by software race conditions and inadequate hardware interlocks.

---

## 🔗 Related Concepts
- [[Engineering-Disasters-and-Case-Studies]]
- [[Ethical-Decision-Frameworks]]
"""
}

# ==============================================================================
# 3. ASSIGNMENTS & DELIVERABLES
# ==============================================================================

ASSIGNMENTS = {
    "02-Courses/COMS3110/Assignments/COMS3110-HW-01.md": """---
title: "COM S 3110 HW 01: Asymptotic Growth & Recurrences"
type: assignment
course: "[[COMS3110-Overview]]"
tags: [assignment, coms3110, algorithms]
created: 2026-08-20
due_date: 2026-09-08
status: not-started
priority: high
---

# 📝 COM S 3110 HW 01: Asymptotic Growth & Recurrences

> [!INFO] Assignment Details
> **Course**: [[COMS3110-Overview]]
> **Topics**: Big-O proofs, Loop complexity analysis, Master Theorem applications.

---

## 🔗 Prerequisite Concepts
- [[Time-Complexity]]
- [[Master-Theorem]]
- [[Recurrence-Relations-and-Master-Theorem]]
""",

    "02-Courses/COMS3110/Assignments/COMS3110-HW-02.md": """---
title: "COM S 3110 HW 02: Divide and Conquer Design"
type: assignment
course: "[[COMS3110-Overview]]"
tags: [assignment, coms3110, algorithms]
created: 2026-08-20
due_date: 2026-09-22
status: not-started
priority: medium
---

# 📝 COM S 3110 HW 02: Divide and Conquer Design

> [!INFO] Assignment Details
> **Topics**: Divide-and-Conquer recurrence formulation, Strassen's algorithm, Inversion counting.

---

## 🔗 Prerequisite Concepts
- [[Divide-and-Conquer]]
- [[Time-Complexity]]
""",

    "02-Courses/CPRE2320/Assignments/CPRE2320-Case-Study-01.md": """---
title: "CPR E 2320 Case Study 01: Therac-25 & Whistleblowing"
type: assignment
course: "[[CPRE2320-Overview]]"
tags: [assignment, cpre2320, ethics]
created: 2026-08-20
due_date: 2026-09-15
status: not-started
priority: medium
---

# 📝 CPR E 2320 Case Study 01: Therac-25 & Whistleblowing

---

## 🔗 Prerequisite Concepts
- [[Engineering-Disasters-and-Case-Studies]]
- [[Whistleblowing-and-Professional-Responsibility]]
""",

    "02-Courses/CPRE2320/Assignments/CPRE2320-Team-Presentation.md": """---
title: "CPR E 2320 Team Presentation: Emerging Tech Ethics"
type: assignment
course: "[[CPRE2320-Overview]]"
tags: [assignment, cpre2320, ethics]
created: 2026-08-20
due_date: 2026-10-20
status: not-started
priority: medium
---

# 📝 CPR E 2320 Team Presentation: Emerging Tech Ethics

---

## 🔗 Prerequisite Concepts
- [[AI-Ethics-and-Data-Privacy]]
- [[Intellectual-Property-in-Tech]]
""",

    "02-Courses/CPRE3080/Assignments/CPRE3080-Lab-01.md": """---
title: "CPR E 3080 Lab 01: UNIX Shell Implementation"
type: assignment
course: "[[CPRE3080-Overview]]"
tags: [assignment, lab, cpre3080, operating-systems]
created: 2026-08-20
due_date: 2026-09-12
status: not-started
priority: high
---

# 📝 CPR E 3080 Lab 01: UNIX Shell Implementation

> [!INFO] Objective
> Implement a custom UNIX shell in C supporting process execution (`fork`, `execvp`, `waitpid`), background jobs (`&`), and I/O redirection.

---

## 🔗 Prerequisite Concepts
- [[Process-Management]]
- [[Linux-Systems-Programming]]
""",

    "02-Courses/CPRE3080/Assignments/CPRE3080-Lab-02.md": """---
title: "CPR E 3080 Lab 02: Multithreaded Bank Simulator"
type: assignment
course: "[[CPRE3080-Overview]]"
tags: [assignment, lab, cpre3080, operating-systems]
created: 2026-08-20
due_date: 2026-10-03
status: not-started
priority: high
---

# 📝 CPR E 3080 Lab 02: Multithreaded Synchronization

---

## 🔗 Prerequisite Concepts
- [[Threads-and-Concurrency]]
- [[Synchronization-Primitives]]
""",

    "02-Courses/CPRE4370/Assignments/CPRE4370-Lab-01-Packet-Sniffing.md": """---
title: "CPR E 4370 Lab 01: 802.11 Wireless Packet Sniffing"
type: assignment
course: "[[CPRE4370-Overview]]"
tags: [assignment, lab, cpre4370, wireless-security]
created: 2026-08-20
due_date: 2026-09-18
status: not-started
priority: high
---

# 📝 CPR E 4370 Lab 01: 802.11 Wireless Packet Sniffing

---

## 🔗 Prerequisite Concepts
- [[Wireless-Threat-Models]]
""",

    "02-Courses/CPRE4370/Assignments/CPRE4370-Lab-02-WPA-Handshake.md": """---
title: "CPR E 4370 Lab 02: WPA2 4-Way Handshake & Deauth"
type: assignment
course: "[[CPRE4370-Overview]]"
tags: [assignment, lab, cpre4370, wireless-security]
created: 2026-08-20
due_date: 2026-10-09
status: not-started
priority: high
---

# 📝 CPR E 4370 Lab 02: WPA2 4-Way Handshake & Deauth

---

## 🔗 Prerequisite Concepts
- [[WPA2-WPA3-Protocols]]
- [[Wireless-Threat-Models]]
""",

    "02-Courses/CPRE4910/Deliverables/CPRE4910-Advisor-Meetings.md": """---
title: "CPR E 4910 Advisor Meeting Logs"
type: deliverable
course: "[[CPRE4910-Overview]]"
tags: [deliverable, senior-design, cpre4910]
created: 2026-08-20
---

# 📋 CPR E 4910: Weekly Faculty Advisor Meeting Logs
""",

    "02-Courses/CPRE4910/Deliverables/CPRE4910-Client-Meetings.md": """---
title: "CPR E 4910 Client Meeting Logs"
type: deliverable
course: "[[CPRE4910-Overview]]"
tags: [deliverable, senior-design, cpre4910]
created: 2026-08-20
---

# 📋 CPR E 4910: Client Requirements & Feedback Logs
""",

    "02-Courses/CPRE4910/Deliverables/CPRE4910-Sprint-01-Kickoff.md": """---
title: "CPR E 4910 Sprint 01 Planning & Kickoff"
type: deliverable
course: "[[CPRE4910-Overview]]"
tags: [deliverable, senior-design, cpre4910]
created: 2026-08-20
---

# 📋 CPR E 4910: Sprint 01 Backlog & Planning
""",

    "02-Courses/CPRE4940/Deliverables/CPRE4940-Final-Portfolio-Submission.md": """---
title: "CPR E 4940 Final Portfolio Submission"
type: deliverable
course: "[[CPRE4940-Overview]]"
tags: [deliverable, portfolio, cpre4940]
created: 2026-08-20
---

# 📋 CPR E 4940: Final Professional Portfolio
""",

    "02-Courses/CPRE4940/Deliverables/CPRE4940-Project-Reflections.md": """---
title: "CPR E 4940 Engineering Project Reflections"
type: deliverable
course: "[[CPRE4940-Overview]]"
tags: [deliverable, reflection, cpre4940]
created: 2026-08-20
---

# 📋 CPR E 4940: Engineering Reflections & Self-Assessment
""",

    "02-Courses/CPRE4940/Deliverables/CPRE4940-Resume-Draft.md": """---
title: "CPR E 4940 Engineering Resume Draft"
type: deliverable
course: "[[CPRE4940-Overview]]"
tags: [deliverable, career, cpre4940]
created: 2026-08-20
---

# 📋 CPR E 4940: Career Portfolio & Engineering Resume
"""
}

# ==============================================================================
# 4. EXAM PREP & QUIZZES
# ==============================================================================

QUIZZES = {
    "02-Courses/COMS3110/Exams/Quiz-COMS3110-Recurrences-and-Master-Theorem.md": """---
title: "Quiz: Recurrences & Master Theorem"
type: quiz
course: "[[COMS3110-Overview]]"
tags: [quiz, active-recall, coms3110, algorithms]
created: 2026-08-20
mastery_score: 0%
---

# ⚡ Active Recall Quiz: Recurrences & Master Theorem

### Q1: What is the asymptotic solution to $T(n) = 4T(n/2) + n^2$?

> [!TIP]- 💡 Solution & Explanation
> **Answer**: $\Theta(n^2 \log n)$  
> $a=4, b=2 \implies n^{\log_2 4} = n^2$. Since $f(n) = n^2 = \Theta(n^2)$, this falls under **Master Theorem Case 2**.

---

### Q2: Can the Master Theorem solve $T(n) = 2T(n/2) + n \log n$?

> [!TIP]- 💡 Solution & Explanation
> **Answer**: Not under standard 3-case Master Theorem, but yes under Extended Case 2 ($k=1$), giving $\Theta(n \log^2 n)$.

---

## 🔗 Related Concepts
- [[Master-Theorem]]
- [[Recurrence-Relations-and-Master-Theorem]]
""",

    "02-Courses/COMS3110/Exams/Quiz-COMS3110-Dynamic-Programming.md": """---
title: "Quiz: Dynamic Programming Foundations"
type: quiz
course: "[[COMS3110-Overview]]"
tags: [quiz, active-recall, coms3110, algorithms]
created: 2026-08-20
mastery_score: 0%
---

# ⚡ Active Recall Quiz: Dynamic Programming

### Q1: What two properties must a problem have for DP to apply?

> [!TIP]- 💡 Solution & Explanation
> **Answer**:
> 1. Optimal Substructure
> 2. Overlapping Subproblems

---

## 🔗 Related Concepts
- [[Dynamic-Programming]]
""",

    "02-Courses/CPRE2320/Exams/Quiz-CPRE2320-IEEE-ACM-Codes.md": """---
title: "Quiz: IEEE & ACM Codes of Ethics"
type: quiz
course: "[[CPRE2320-Overview]]"
tags: [quiz, active-recall, cpre2320, ethics]
created: 2026-08-20
mastery_score: 0%
---

# ⚡ Active Recall Quiz: IEEE & ACM Codes of Ethics

---

## 🔗 Related Concepts
- [[Codes-of-Ethics]]
- [[Engineering-Ethics-Overview]]
""",

    "02-Courses/CPRE3080/Exams/Quiz-CPRE3080-Processes-and-Threads.md": """---
title: "Quiz: Processes and Threads"
type: quiz
course: "[[CPRE3080-Overview]]"
tags: [quiz, active-recall, cpre3080, operating-systems]
created: 2026-08-20
mastery_score: 0%
---

# ⚡ Active Recall Quiz: Processes & Threads

---

## 🔗 Related Concepts
- [[Process-Management]]
- [[Threads-and-Concurrency]]
""",

    "02-Courses/CPRE3080/Exams/Quiz-CPRE3080-Memory-and-Scheduling.md": """---
title: "Quiz: Memory Management & CPU Scheduling"
type: quiz
course: "[[CPRE3080-Overview]]"
tags: [quiz, active-recall, cpre3080, operating-systems]
created: 2026-08-20
mastery_score: 0%
---

# ⚡ Active Recall Quiz: Memory & Scheduling

---

## 🔗 Related Concepts
- [[CPU-Scheduling]]
- [[Virtual-Memory-and-Paging]]
""",

    "02-Courses/CPRE4370/Exams/Quiz-CPRE4370-WiFi-and-WPA.md": """---
title: "Quiz: Wi-Fi Security & WPA Protocols"
type: quiz
course: "[[CPRE4370-Overview]]"
tags: [quiz, active-recall, cpre4370, wireless-security]
created: 2026-08-20
mastery_score: 0%
---

# ⚡ Active Recall Quiz: Wi-Fi & WPA

---

## 🔗 Related Concepts
- [[WPA2-WPA3-Protocols]]
- [[Wireless-Threat-Models]]
""",

    "02-Courses/CPRE4370/Exams/Quiz-CPRE4370-Cellular-and-Bluetooth.md": """---
title: "Quiz: Cellular & Bluetooth Security"
type: quiz
course: "[[CPRE4370-Overview]]"
tags: [quiz, active-recall, cpre4370, wireless-security]
created: 2026-08-20
mastery_score: 0%
---

# ⚡ Active Recall Quiz: Cellular & Bluetooth

---

## 🔗 Related Concepts
- [[Bluetooth-BLE-Security]]
- [[Cellular-Security-and-IMSI]]
"""
}

def main():
    for name, content in CONCEPTS.items():
        write_note(f"03-Concepts/{name}", content)
    for name, content in LECTURES.items():
        write_note(name, content)
    for name, content in ASSIGNMENTS.items():
        write_note(name, content)
    for name, content in QUIZZES.items():
        write_note(name, content)

if __name__ == "__main__":
    main()
