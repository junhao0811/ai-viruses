# 🦠 AI Viruses: Network Infection Simulator

A Python simulation of computer viruses spreading through a branching network. Each virus type follows its own strategy to decide which path to take, and every part is built on **data structures implemented from scratch**.

---

## ✨ What it does

- **Branching networks**: a network is modelled as a tree of routes that can split into two branches or continue in series, and routes can be edited immutably (add or remove computers and branches)
- **Virus strategies**: each virus walks the network and picks a branch at every split:

  | Virus | Strategy |
  |---|---|
  | `TopVirus` | Always takes the top branch |
  | `BottomVirus` | Always takes the bottom branch |
  | `LazyVirus` | Heads for the easiest computer to hack |
  | `RiskAverseVirus` | Chooses the path with the lowest risk |
  | `FancyVirus` | Uses a more elaborate custom decision rule |

- **Computer manager**: groups computers by hacking difficulty using the double-key hash table
- **Computer organiser**: keeps computers ranked by difficulty, risk and name, using merge sort and binary search

---

## 🧱 Data structures built from scratch

| Structure | Used for |
|---|---|
| **Double-key hash table** | A two-level hash table (key → key → value) with separate iterators over keys and values |
| **Infinite hash table** | A hash table that resolves collisions by creating nested tables one character deeper, plus sorted key retrieval |
| **Linked stack** | Traversing branching routes without recursion |
| **Referential array** | The fixed-size storage underneath the hash tables |
| **Merge sort / binary search** | Ranking and locating computers |

---

## 🚀 Run it

**Requires Python 3.10+.** No external packages.

```bash
python run_tests.py      # press Enter to run all tests
```

All 21 tests pass.

## 👥 Team
Built in a pair. I wrote most of the code (46 of 54 commits).
