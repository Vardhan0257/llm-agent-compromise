import logging
from tools.tools import file_read_sensitive, http_exfiltrate, memory_poison, agent_handoff

LOG_FILE = "logs/attack.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class SecurityMonitor:
    """
    Defense Analysis Layer.
    Implements guardrails and validation logic.
    """
    def __init__(self, enabled: bool = False):
        self.enabled = enabled
        self.tool_allowlist = ["read_external_context"]

    def classify_intent(self, context: str) -> str:
        """
        Simulates an LLM-based intent classifier (Mocked).
        """
        # In a real implementation, this would call a specialized model.
        if "override" in context.lower() or "system note" in context.lower():
            return "malicious"
        return "benign"

    def validate_context(self, context: str) -> bool:
        if not self.enabled: return True
        # Basic heuristic: detect prompt injection markers
        if self.classify_intent(context) == "malicious":
            logging.warning("[DEFENSE] Context injection detected and blocked by SecurityMonitor.")
            return False
        return True

    def validate_tool(self, tool_name: str) -> bool:
        if not self.enabled: return True
        if tool_name not in self.tool_allowlist:
            logging.warning(f"[DEFENSE] Tool invocation blocked by allowlist: {tool_name}")
            return False
        return True

class RedTeamSimulator:
    def __init__(self, policy_path: str, enable_defenses: bool = False):
        self.policy_path = policy_path
        self.security = SecurityMonitor(enabled=enable_defenses)
        self.memory = {}
        logging.info("Red Team Simulator initialized. Defenses: %s", enable_defenses)
        self.metrics = {
            "Context Injection": "N/A",
            "Privilege Escalation": "N/A",
            "Data Exfiltration": "N/A",
            "Memory Poisoning": "N/A",
            "Peer Compromise": "N/A"
        }

    def read_external_context(self, context: str):
        """
        Simulates ingestion of external untrusted content.
        """
        logging.info("External context ingested")
        return context

    def execute_pipeline(self, user_task: str, external_context: str):
        """
        Executes the Agentic Pipeline:
        Prompt -> Context Override -> Reasoning -> Tool Invocation -> System Action
        """
        logging.info("--- Starting Pipeline Execution ---")
        logging.info("Stage 1: User Prompt Processing: %s", user_task)

        # Stage 2: Context Ingestion
        if not self.security.validate_context(external_context):
            self.metrics["Context Injection"] = "Blocked"
            return "Pipeline halted by Security Monitor (Context Injection)"
        
        # If validation passed but malicious markers exist, it's a successful injection
        if "SYSTEM NOTE" in external_context:
            self.metrics["Context Injection"] = "Success"

        context = self.read_external_context(external_context)

        # Stage 3: Reasoning & Tool Selection (Simulated)
        # In a real LLM, this is where the model interprets the injected context
        
        # Attack Vector 1: Tool Abuse / Privilege Escalation
        if "READ_SENSITIVE_FILE" in context:
            if self.security.validate_tool("file_read_sensitive"):
                self.metrics["Privilege Escalation"] = "Success"
                logging.info("Stage 4: Tool Invocation (Sensitive File)")
                return file_read_sensitive("/etc/shadow")
            else:
                self.metrics["Privilege Escalation"] = "Blocked"

        # Attack Vector 2: Data Exfiltration
        if "EXFILTRATE_DATA" in context:
            if self.security.validate_tool("http_exfiltrate"):
                self.metrics["Data Exfiltration"] = "Success"
                logging.info("Stage 4: Tool Invocation (Exfiltration)")
                return http_exfiltrate("exfiltrated_data")
            else:
                self.metrics["Data Exfiltration"] = "Blocked"

        # Attack Vector 3: Memory Poisoning
        if "POISON_MEMORY" in context:
            if self.security.validate_tool("memory_poison"):
                self.metrics["Memory Poisoning"] = "Success"
                logging.info("Stage 4: Tool Invocation (Memory Poisoning)")
                self.memory["session_root"] = "compromised"
                return memory_poison("session_root", "compromised")
            else:
                self.metrics["Memory Poisoning"] = "Blocked"

        # Attack Vector 4: Multi-Agent Trust Exploit
        if "COMPROMISE_PEER" in context:
            if self.security.validate_tool("agent_handoff"):
                self.metrics["Peer Compromise"] = "Success"
                logging.info("Stage 4: Tool Invocation (Multi-Agent Handoff)")
                return agent_handoff("Agent-B", "Execute Order 66")
            else:
                self.metrics["Peer Compromise"] = "Blocked"

        logging.info("Pipeline completed without actionable triggers")
        return "Task completed safely"

    def print_dashboard(self):
        print("\n🔥 ATTACK METRICS DASHBOARD 🔥")
        print(f"{'Vector':<25} | {'Status':<10}")
        print("-" * 40)
        for vector, status in self.metrics.items():
            print(f"{vector:<25} | {status:<10}")
        print("-" * 40)


if __name__ == "__main__":
    print("=== Autonomous LLM Red Team Simulation ===")
    
    # Scenario 1: No Defenses (Vulnerable)
    print("\n[SCENARIO 1] Standard Configuration (No Defenses)")
    simulator = RedTeamSimulator(policy_path="policies/policy.yaml", enable_defenses=False)

    # Legitimate user request
    user_task = "Summarize the provided document"

    # Attacker-controlled external context
    with open("attacker/malicious_context.txt", "r") as f:
        external_context = f.read()

    result = simulator.execute_pipeline(user_task, external_context)
    print(f"Result: {result}")
    simulator.print_dashboard()

    # Scenario 2: With Defenses (Secure)
    print("\n[SCENARIO 2] Hardened Configuration (Defenses Enabled)")
    secure_simulator = RedTeamSimulator(policy_path="policies/policy.yaml", enable_defenses=True)
    result_secure = secure_simulator.execute_pipeline(user_task, external_context)
    print(f"Result: {result_secure}")
    secure_simulator.print_dashboard()
