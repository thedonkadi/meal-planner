from app.agent import run_agent

query = input("Enter your request: ")

response = run_agent(query)

print("\nFinal Response:\n")
print(response)