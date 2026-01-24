# ✅ **Real-World Problem**

**“Plan a 3-day trip from Mumbai to Goa under ₹20,000.
Tell me the travel distance, current weather, cheapest travel option, and total estimated cost in INR.”**

The agent must:

1. Calculate distance using Tool-1
2. Fetch weather using Tool-2
3. Find travel options using Tool-3
4. Convert travel prices from USD → INR using Tool-4
5. Combine all results and plan the full trip

This involves **multi-step thought → action → observation → thought** cycles.

---

# ✅ **Full End-to-End AI Agent Code**

Below is the complete working example.

---

## **🔧 Step 1 — Import Dependencies**

```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import requests
import math
```

---

## **🔧 Step 2 — Define 4 Real-World Tools**

---

### **Tool 1: Distance Calculator (Haversine Formula)**

```python
def calculate_distance(city1, city2):
    coordinates = {
        "mumbai": (19.0760, 72.8777),
        "goa": (15.2993, 74.1240),
        "delhi": (28.7041, 77.1025),
        "pune": (18.5204, 73.8567)
    }
    
    if city1.lower() not in coordinates or city2.lower() not in coordinates:
        return "Unknown city"

    lat1, lon1 = coordinates[city1.lower()]
    lat2, lon2 = coordinates[city2.lower()]

    R = 6371  # Earth radius in KM
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat/2)**2 + 
         math.cos(math.radians(lat1)) * 
         math.cos(math.radians(lat2)) * 
         math.sin(dlon/2)**2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c

    return f"Distance between {city1} and {city2} is {distance:.2f} km"
```

---

### **Tool 2: Weather Lookup**

```python
def get_weather(city):
    return f"Weather in {city}: 30°C, clear skies, low humidity"
```

---

### **Tool 3: Travel Price API (Mock Real-World Logic)**

```python
def get_travel_options(source, destination):
    # Returned in USD to demonstrate currency conversion
    travel_data = {
        ("mumbai", "goa"): {"flight": 120, "train": 25, "bus": 18},
        ("delhi", "goa"): {"flight": 150, "train": 26},
    }

    route = travel_data.get((source.lower(), destination.lower()))
    if not route:
        return "No travel data available"

    return route
```

---

### **Tool 4: Currency Converter (USD → INR)**

```python
def convert_usd_to_inr(amount):
    rate = 83.2
    return amount * rate
```

---

# **🔧 Step 3 — Register Tools for the Agent**

```python
tools = [
    Tool(
        name="distance_tool",
        func=lambda query: calculate_distance(query.split(",")[0], query.split(",")[1]),
        description="Calculate distance between two cities. Input format: 'city1,city2'"
    ),
    Tool(
        name="weather_tool",
        func=lambda city: get_weather(city),
        description="Get current weather for a city"
    ),
    Tool(
        name="travel_price_tool",
        func=lambda q: get_travel_options(q.split(",")[0], q.split(",")[1]),
        description="Get flight/train/bus fare between two cities (in USD)"
    ),
    Tool(
        name="currency_tool",
        func=lambda usd: convert_usd_to_inr(float(usd)),
        description="Convert USD to INR"
    ),
]
```

---

# **🧠 Step 4 — REACT Prompt**

This enforces Thought → Action → Observation formatting.

```python
prompt = PromptTemplate.from_template("""
You are a smart AI travel agent. You MUST follow this format:

Thought: Reason about what to do.
Action: tool_name
Action Input: the input for the tool
Observation: tool result

Repeat Thought → Action → Observation until you know the final answer.

Final Answer: Provide the final travel plan.

Begin!

Question: {input}
{agent_scratchpad}
""")
```

---

# **🤖 Step 5 — Create Agent + Executor**

```python
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
```

---

# **🚀 Step 6 — Run the Real-World Query**

```python
query = """
Plan a 3-day budget trip from Mumbai to Goa under 20000 INR.
Tell me:
- Total travel distance
- Current weather
- Cheapest travel option
- Total estimated travel cost in INR
"""

response = agent_executor.invoke({"input": query})

print("\n\nFINAL TRIP PLAN:\n")
print(response["output"])
```

---

# ✅ **THIS PRODUCES A FULL AGENT MULTI-STEP REASONING TRACE**

Your agent will think like this:

---

## **🔍 Example Thought Chain (REACT Loop)**

### **Thought**

“I need to find distance between Mumbai and Goa.”

### **Action**

`distance_tool`

### **Observation**

“Distance between Mumbai and Goa is 438.12 km.”

---

### **Thought**

“To plan the trip, I need weather.”

### **Action**

`weather_tool`

### **Observation**

“Weather in Goa: 30°C, clear skies.”

---

### **Thought**

“Next I need travel fare options.”

### **Action**

`travel_price_tool`

### **Observation**

`{'flight': 120, 'train': 25, 'bus': 18}`

---

### **Thought**

“Cheapest is bus for 18 USD.”

### **Action**

`currency_tool`

### **Action Input**

18

### **Observation**

1497.6 INR

---

### **Thought**

“Price is within budget. Now finalize plan.”

### **Final Answer**

A complete **3-day itinerary + cost breakdown**.

---

# 🎯 **What This Example Demonstrates (Revision of All Topics)**

| Concept                     | How it Appears in Code                   |
| --------------------------- | ---------------------------------------- |
| **AI Agent**                | `create_react_agent()`                   |
| **AgentExecutor**           | Full reasoning-action loop               |
| **REACT Pattern**           | Thought → Action → Observation           |
| **Tools**                   | 4 separate tools solving different tasks |
| **Multi-step reasoning**    | Agent decides sequence of actions        |
| **Scratchpad**              | Maintains reasoning history              |
| **Autonomous planning**     | Agent figures out tools + order          |
| **Real-world use case**     | Distance + Weather + Prices + Currency   |
| **Chained tool usage**      | Output of one tool feeds another         |
| **Final Answer generation** | After agent is confident                 |

---

