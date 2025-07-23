from agent import run_agent_goal

def repl():
    print("\n🤖 AI Shell Copilot (Autonomous Mode)")
    print("Type ':exit' to quit\n")

    while True:
        try:
            user_input = input("💬 > ")

            if user_input.strip() == ":exit":
                print("👋 Exiting...")
                break

            print("⚙️ Agent thinking...")
            output = run_agent_goal(user_input)

            print("🧾 Output:\n", output)

        except KeyboardInterrupt:
            print("\n⏹️ Interrupted.")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    repl()
