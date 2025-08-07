from flow import graph
from colorama import Fore, Style

def main():
    while True:
        prompt = input(Fore.GREEN + "Enter a prompt: " + Style.RESET_ALL)
        if prompt.lower() == "exit":
            break
        res = graph.invoke({"messages": [("user", prompt)]}, config={"configurable": {"thread_id": "1234"}})
        print(Fore.YELLOW + res["messages"][-1].content + Style.RESET_ALL)

if __name__ == "__main__":
    main()