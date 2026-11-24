# Deep Learning Fundamentals & Mathematical Grounding for Time Series Forecasting

## 1. Classical Recurrent Neural Networks (RNNs)

### 1.1 Recurrence Formulation
A standard Recurrent Neural Network processes an input sequence $(x_1, x_2, \dots, x_T)$ step-by-step by updating a continuous internal memory vector (hidden state $h_t \in \mathbb{R}^d$):

$$h_t = \tanh(W_{hh} h_{t-1} + W_{xh} x_t + b_h)$$
$$\hat{y}_t = W_{hy} h_t + b_y$$

Where:
- $x_t \in \mathbb{R}^p$: Feature input vector at time step $t$
- $h_{t-1} \in \mathbb{R}^d$: Prior hidden state representing accumulated temporal context
- $W_{xh} \in \mathbb{R}^{d \times p}$: Input-to-hidden weight transformation matrix
- $W_{hh} \in \mathbb{R}^{d \times d}$: Hidden-to-hidden recurrent transition matrix
- $b_h \in \mathbb{R}^d$: Hidden layer bias vector
- $W_{hy} \in \mathbb{R}^{k \times d}$: Hidden-to-output projection matrix

---

### 1.2 Backpropagation Through Time (BPTT) and The Vanishing Gradient Problem
Given a sequence loss $\mathcal{L} = \sum_{t=1}^T \mathcal{L}_t$, the gradient with respect to recurrent weights $W_{hh}$ requires applying the multivariate chain rule across temporal unrolling:

$$\frac{\partial \mathcal{L}}{\partial W_{hh}} = \sum_{t=1}^T \frac{\partial \mathcal{L}_t}{\partial W_{hh}}$$

Evaluating the gradient of the loss at step $T$ with respect to the hidden state at an early step $t$:

$$\frac{\partial \mathcal{L}_T}{\partial h_t} = \frac{\partial \mathcal{L}_T}{\partial h_T} \frac{\partial h_T}{\partial h_t} = \frac{\partial \mathcal{L}_T}{\partial h_T} \prod_{j=t+1}^T \frac{\partial h_j}{\partial h_{j-1}}$$

The Jacobian matrix of the hidden state transition is:

$$\frac{\partial h_j}{\partial h_{j-1}} = \operatorname{diag}\left(1 - \tanh^2(W_{hh} h_{j-1} + W_{xh} x_j + b_h)\right) W_{hh}^T$$

As the temporal distance $(T - t)$ increases:
1. Since the derivative of the hyperbolic tangent $\tanh'(z) \in (0, 1]$, the continuous diagonal product rapidly decays below unity.
2. If the largest eigenvalue $\lambda_{\max}(W_{hh}) < 1$, the continuous matrix power product:
   $$\lim_{(T-t) \to \infty} \prod_{j=t+1}^T W_{hh}^T = 0$$
   This causes the gradient $\frac{\partial \mathcal{L}_T}{\partial h_t}$ to vanish exponentially, preventing the network from learning dependencies beyond 8–10 time steps.
3. Conversely, if $\lambda_{\max}(W_{hh}) > 1$, the gradient explodes towards $\pm \infty$ (causing numeric `NaN` or overflow), necessitating gradient clipping.

---

## 2. Long Short-Term Memory (LSTM) Architecture

To eliminate the vanishing gradient problem, Hochreiter & Schmidhuber (1997) introduced the **Long Short-Term Memory (LSTM)** network. It separates memory into two distinct pathways:
1. **Cell State ($C_t$)**: The linear, unobstructed conveyor belt ("Constant Error Carousel").
2. **Hidden State ($h_t$)**: The gated, nonlinear short-term output exposed to downstream layers.

```
                    ┌────────────────────────────┐
   C_{t-1} ─────────► (x) ────────── (+) ────────► C_t
                     ▲                ▲
                     │ f_t            │ (i_t * \tilde{C}_t)
                     │          ┌─────┴─────┐
                     │          │           │
                     │         (x)          │
                     │          ▲           │
             ┌───────┴──────┐   │ i_t       │ \tilde{C}_t
             │ Forget Gate  │ ┌─┴─────────┐ │
             │  \sigma      │ │Input Gate │ │ \tanh
             └───────▲──────┘ │  \sigma   │ └─▲───┘
                     │        └───▲───────┘   │
                     │            │           │
   h_{t-1} ──────────┼────────────┼───────────┼───────► (x) ────────► h_t
   x_t     ──────────┴────────────┴───────────┘          ▲
                                                         │ o_t
                                                  ┌──────┴──────┐
                                                  │ Output Gate │
                                                  │   \sigma    │
                                                  └─────────────┘
```

### 2.1 The Gate Equations

1. **Forget Gate ($f_t$)**: Regulates what portion of previous cell memory $C_{t-1}$ to discard.
   $$f_t = \sigma\left(W_f \cdot [h_{t-1}, x_t] + b_f\right)$$

2. **Input Gate ($i_t$)**: Determines which new candidate information will be admitted into the cell state.
   $$i_t = \sigma\left(W_i \cdot [h_{t-1}, x_t] + b_i\right)$$

3. **Candidate Memory State ($\tilde{C}_t$)**: Computes new feature representations from the current input and prior state.
   $$\tilde{C}_t = \tanh\left(W_c \cdot [h_{t-1}, x_t] + b_c\right)$$

4. **Cell State Update ($C_t$)**: Modulates prior memory linearly by the forget gate and adds scaled new candidate memory.
   $$C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$$

5. **Output Gate ($o_t$)**: Computes which portions of the updated cell state to emit to the hidden state.
   $$o_t = \sigma\left(W_o \cdot [h_{t-1}, x_t] + b_o\right)$$

6. **Hidden State ($h_t$)**: Applies squashing activation to the updated cell state and scales by the output gate.
   $$h_t = o_t \odot \tanh(C_t)$$

### 2.2 Mathematical Proof of Gradient Preservation
Evaluating the gradient propagation through the cell state:

$$\frac{\partial C_t}{\partial C_{t-1}} = f_t$$

Because the update is purely additive ($C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$), the gradient error vector propagates across time via:

$$\frac{\partial \mathcal{L}}{\partial C_{t-1}} = \frac{\partial \mathcal{L}}{\partial C_t} \frac{\partial C_t}{\partial C_{t-1}} = \frac{\partial \mathcal{L}}{\partial C_t} \cdot f_t$$

When the forget gate $f_t \approx 1$ (which is initialized by setting forget gate biases $b_f \approx 1.0$), the error gradient flows back through hundreds of time steps with **zero exponential decay**.

---

## 3. Gated Recurrent Unit (GRU) Architecture

Proposed by Cho et al. (2014), the **Gated Recurrent Unit (GRU)** streamlines the LSTM architecture by:
1. Merging the separate cell state $C_t$ and hidden state $h_t$ into a single vector $h_t$.
2. Combining the forget and input gates into a single **Update Gate ($z_t$)**.
3. Controlling dependency on prior context using a **Reset Gate ($r_t$)**.

### 3.1 Mathematical Formulation

1. **Update Gate ($z_t$)**: Decides how much of past information should be carried forward versus overwritten.
   $$z_t = \sigma\left(W_z \cdot [h_{t-1}, x_t] + b_z\right)$$

2. **Reset Gate ($r_t$)**: Decides how much of the past hidden state to ignore when computing candidate state.
   $$r_t = \sigma\left(W_r \cdot [h_{t-1}, x_t] + b_r\right)$$

3. **Candidate Hidden State ($\tilde{h}_t$)**: Computes new context using the reset-modulated prior state.
   $$\tilde{h}_t = \tanh\left(W_h \cdot [r_t \odot h_{t-1}, x_t] + b_h\right)$$

4. **Hidden State Output ($h_t$)**: Linearly interpolates between the previous state $h_{t-1}$ and candidate $\tilde{h}_t$.
   $$h_t = (1 - z_t) \odot h_{t-1} + z_t \odot \tilde{h}_t$$

---

## 4. LSTM vs. GRU: Architectural & Operational Comparison

| Attribute | Standard RNN | Long Short-Term Memory (LSTM) | Gated Recurrent Unit (GRU) |
| :--- | :--- | :--- | :--- |
| **State Vectors** | 1 ($h_t$) | 2 ($C_t$ Cell State, $h_t$ Hidden State) | 1 ($h_t$ Hidden State) |
| **Number of Gates** | 0 | 3 (Forget $f$, Input $i$, Output $o$) | 2 (Reset $r$, Update $z$) |
| **Trainable Parameter Count** | $d^2 + d \cdot p + d$ | $4 \times (d^2 + d \cdot p + d)$ | $3 \times (d^2 + d \cdot p + d)$ |
| **Computational Overhead** | Lowest ($O(1)$) | Highest ($\approx 33\%$ more than GRU) | Moderate |
| **Gradient Preservation** | Degrades in 5–10 steps | Stable over 100+ steps | Stable over 100+ steps |
| **Small-Data Sample Efficiency**| Poor | Prone to overfitting on small data | Highly sample-efficient |
| **Best Use Case** | Trivial short sequences | Complex multi-frequency sequences | Rapid prototyping & moderate tabular series |

---

## 5. Bidirectional Sequence Modeling (BiLSTM / BiGRU)

In standard causal forecasting, time flows strictly forward ($t=1 \to T$). However, during sequence representation learning, a **Bidirectional Recurrent Neural Network** unrolls the sequence in both directions:
- Forward layer: $\vec{h}_t = \operatorname{LSTM}(x_t, \vec{h}_{t-1})$
- Backward layer: $\overleftarrow{h}_t = \operatorname{LSTM}(x_t, \overleftarrow{h}_{t+1})$
- Combined feature representation: $h_t = [\vec{h}_t \,\|\, \overleftarrow{h}_t]$

This architecture captures both leading indicators and lagging recovery patterns across supermarket promotional cycles.
