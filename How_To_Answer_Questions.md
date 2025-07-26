# How to Answer the Blockhouse Task Questions

## Question 1: How do you choose to model the temporary impact g_t(x)?

### Your Answer Strategy:

**1. Start with the Problem Statement (2-3 paragraphs)**
- Acknowledge that linear models g_t(x) ≈ β_t x are oversimplifications
- Explain why real market microstructure requires more sophisticated modeling
- Introduce your VWAP-based approach as a data-driven alternative

**2. Present Your Model (1 page)**
```
Mathematical Model:
g_buy(x) = (VWAP_execution(x,t) - Mid_t) / Mid_t
g_sell(x) = (Mid_t - VWAP_execution(x,t)) / Mid_t

Where VWAP_execution simulates walking through the order book
```

**3. Empirical Evidence (1/2 page)**
Use your C++ results to show:
- CRWV: 17.6-20.7 bps impact (moderate liquidity)
- FROG: 26.4-31.5 bps impact (low liquidity)  
- SOUN: 10.9-11.6 bps impact (high liquidity)

**4. Why Linear Models Fail (1/2 page)**
- Order book depth heterogeneity
- Adverse selection effects
- Convexity in real market impact
- Show your charts demonstrating non-linearity

---

## Question 2: Mathematical framework for optimal execution

### Your Answer Strategy:

**1. Problem Formulation (1/2 page)**
```
Objective: minimize Σᵢ g_tᵢ(xᵢ) · xᵢ
Subject to: Σᵢ xᵢ = S
           xᵢ ≥ 0
```

**2. Solution Approach (1 page)**

**Dynamic Programming Framework:**
```
State: (remaining_shares, time, market_state)
Bellman Equation: V(S_t, t) = min_x [g_t(x)·x + E[V(S_t-x, t+1)]]
```

**3. Constraint Handling (1/2 page)**
Three methods to ensure Σᵢ xᵢ = S:

- **Lagrange Multipliers**: Add λ(Σᵢ xᵢ - S) to objective
- **Penalty Method**: Add μ(Σᵢ xᵢ - S)² penalty term
- **Sequential Allocation**: Normalize at each step (your implementation)

**4. Algorithm Implementation (1/2 page)**
```cpp
// Pseudo-code for your C++ approach
for each time_step t_i:
    estimate g_t_i from recent order book data
    calculate optimal x_i considering remaining shares
    ensure Σ x_i = S via normalization
```

---

## Key Files for Submission:

### **Written Report:**
- `Task_Analysis_Report.md` - Your 4-page detailed analysis

### **Code Implementation:**
- `order_book_analysis.cpp` - High-performance C++ implementation
- `blockhouse_analysis.ipynb` - Jupyter notebook for GitHub
- `compile_and_run.bat` - Easy compilation script

### **Results & Visualizations:**
- `cpp_price_impact_analysis.png` - Main impact charts
- `cpp_impact_comparison.png` - Comparison across symbols
- `*_impact.csv` - Detailed numerical results

### **GitHub Repository Structure:**
```
your-repo/
├── README.md (overview)
├── order_book_analysis.cpp
├── blockhouse_analysis.ipynb  
├── results/
│   ├── cpp_price_impact_analysis.png
│   ├── CRWV_buy_impact.csv
│   └── ...
└── docs/
    └── Task_Analysis_Report.md
```

---

## Writing Tips:

### **Question 1 (1-2 pages):**
- **Be specific** about why you chose VWAP over linear models
- **Use your data** - reference the actual results from CRWV, FROG, SOUN
- **Show charts** - include your impact visualizations
- **Mathematical rigor** - include the exact formulas you implemented

### **Question 2 (≤2 pages):**
- **Start with math** - clear objective function and constraints
- **Explain the algorithm** - dynamic programming approach
- **Address the constraint** - how you ensure Σᵢ xᵢ = S
- **Implementation** - reference your C++ code as proof of concept

### **GitHub Link:**
Create a repository and include the link in your submission. Make sure it contains:
- Working code (C++ + Python notebook)
- Clear README with setup instructions
- Results and visualizations
- Mathematical documentation

---

## Your Competitive Advantages:

✅ **High-performance C++ implementation** (2.36 seconds vs much slower Python)  
✅ **Real MBP-10 data parsing** (proper Databento format handling)  
✅ **Comprehensive empirical analysis** (90,000 snapshots processed)  
✅ **Mathematical rigor** (proper VWAP simulation, constraint handling)  
✅ **Professional visualizations** (publication-quality charts)  
✅ **Complete working solution** (compilable, runnable, documented)

This demonstrates both theoretical knowledge and practical implementation skills that are highly valued in quantitative finance roles.
