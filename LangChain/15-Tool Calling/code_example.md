# 🚀 **Real-World Scenario: “Customer Support AI Assistant with Order Tracking + Refund Eligibility + Product Info + Discount Engine”**

A business wants an AI assistant that can:

1. Retrieve customer order details
2. Check delivery status
3. Check refund eligibility
4. Calculate possible refunds or discounts
5. Answer the user with a final summarized response

We will build **four tools** to support this.

---

# ✅ **Real-World Tools**

## **Tool 1 — get_order_details**

Fetches order data from a database/API.

```python
@tool
def get_order_details(order_id: str) -> dict:
    """Return details for the given order ID including product, price, and delivery status."""
    fake_db = {
        "ORD123": {"product": "Wireless Earbuds", "price": 1999, "status": "Delivered"},
        "ORD124": {"product": "Smartwatch", "price": 3499, "status": "In Transit"},
        "ORD125": {"product": "Laptop", "price": 59999, "status": "Delivered"},
    }
    
    if order_id not in fake_db:
        return {"error": "Order not found"}
    
    return fake_db[order_id]
```

---

## **Tool 2 — check_refund_policy**

Checks if the product/order is eligible for refund.

```python
@tool
def check_refund_policy(status: str) -> dict:
    """
    Checks if product is eligible for a refund based on delivery status.
    Allowed refunds only if status == Delivered.
    """
    if status != "Delivered":
        return {"eligible": False, "reason": "Product not delivered yet."}
    
    return {"eligible": True, "reason": "Delivered — Refund eligible within 10 days."}
```

---

## **Tool 3 — calculate_refund_amount**

Computes the actual refund amount based on rules.

```python
@tool
def calculate_refund_amount(price: float) -> dict:
    """Calculate refundable amount after 10% restocking fee."""
    refund = price - (price * 0.10)
    return {"refund_amount": refund}
```

---

## **Tool 4 — get_product_recommendations**

Suggests alternatives to offer during refund conversations.

```python
@tool
def get_product_recommendations(product: str) -> list:
    """Suggest alternative or upgraded products."""
    recommendations = {
        "Wireless Earbuds": ["AirPods 2nd Gen", "Sony WF-1000XM5", "Samsung Buds2 Pro"],
        "Smartwatch": ["Amazfit GTS 4", "Apple Watch SE", "Galaxy Watch 6"],
        "Laptop": ["MacBook Air M2", "Dell XPS 13", "HP Spectre x360"],
    }
    return recommendations.get(product, [])
```

---

# 🔗 **Binding Tools to LLM**

```python
llm = ChatOpenAI(model="gpt-4o-mini")
llm = llm.bind_tools([
    get_order_details, 
    check_refund_policy, 
    calculate_refund_amount,
    get_product_recommendations
])
```

---

# 🧠 **Real-World User Query**

> “I want to check if I can get a refund for my order ORD123. Also tell me if I can get something better as a replacement.”

This requires:

1. Order lookup
2. Refund eligibility check
3. Refund calculation
4. Product recommendations

The LLM will call tools in sequence.

---

# ⚙️ **Simulated Multi-Step LLM Reasoning + Tool Calling**

### **Step 1 — LLM decides:**

“I must get details of this order.”

```json
{
  "tool": "get_order_details",
  "args": { "order_id": "ORD123" }
}
```

### System Executes → Tool Result:

```json
{"product": "Wireless Earbuds", "price": 1999, "status": "Delivered"}
```

---

### **Step 2 — LLM decides:**

“I now know delivery status. Check refund eligibility.”

```json
{
  "tool": "check_refund_policy",
  "args": { "status": "Delivered" }
}
```

### Tool Result:

```json
{"eligible": true, "reason": "Delivered — Refund eligible within 10 days."}
```

---

### **Step 3 — LLM decides:**

“Refund is eligible → calculate refund amount.”

```json
{
  "tool": "calculate_refund_amount",
  "args": { "price": 1999 }
}
```

### Tool Result:

```json
{"refund_amount": 1799.1}
```

---

### **Step 4 — LLM decides:**

“Customer asked for better replacement → fetch alternatives”

```json
{
  "tool": "get_product_recommendations",
  "args": { "product": "Wireless Earbuds" }
}
```

### Tool Result:

```json
["AirPods 2nd Gen", "Sony WF-1000XM5", "Samsung Buds2 Pro"]
```

---

# 🧩 **Final LLM User Response (Generated After All Tool Outputs)**

> Your order **ORD123** for **Wireless Earbuds** has been successfully delivered.
>
> ✅ **Refund Eligibility:** Yes
> **Reason:** Delivered — Refund eligible within 10 days
>
> 💰 **Refund Amount:** ₹1799.10 (after 10% restocking fee)
>
> ⭐ **Recommended Alternatives:**
>
> * AirPods 2nd Gen
> * Sony WF-1000XM5
> * Samsung Buds2 Pro
>
> Would you like to continue with the refund, or explore alternatives?

---

# 🎯 **What Concepts This Example Demonstrates**

### ✔ Multi-Tool Workflow

4 tools used end-to-end.

### ✔ Tool Calling + Tool Chaining

LLM automatically determines correct sequence.

### ✔ Real Business Logic

Order retrieval → policy validation → computation → recommendation engine.

### ✔ Injected Arguments

Tools pull accurate values such as price/status instead of LLM guessing.

### ✔ Enterprise-level Use Case

Customer support automation is one of the top real-world applications of Tool Calling.

---
