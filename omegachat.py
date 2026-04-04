import os
import time
import pickle
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn
from sentence_transformers import SentenceTransformer, util

# --- CONFIG ---
MODEL_CORE = "all-MiniLM-L6-v2"
VAULT_FILE = "neural_vault.pkl"
DEFAULT_DATA = "data.txt"
console = Console()

class OmegaBot:
    def __init__(self):
        self.encoder = None
        self.memory = {"qs": [], "as": [], "vecs": None}
        self.context = [] # Short-term chat history
        
    def startup(self):
        with console.status("[bold magenta]⚡ Booting Neural Systems...", spinner="dots12"):
            self.encoder = SentenceTransformer(MODEL_CORE)
            if os.path.exists(VAULT_FILE):
                with open(VAULT_FILE, 'rb') as f:
                    self.memory = pickle.load(f)
                msg = f"Vault Access Granted: {len(self.memory['qs'])} nodes active."
            else:
                msg = self.learn_logic(DEFAULT_DATA)
        
        console.print(Panel(f"[bold cyan]OMEGA CORE V3.0[/bold cyan]\n[dim]{msg}[/dim]", border_style="magenta"))

    def learn_logic(self, filename):
        if not os.path.exists(filename):
            return f"Notice: {filename} not found. Awaiting input."
        
        qs, ans = [], []
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                if '|' in line:
                    parts = line.strip().split('|')
                    qs.append(parts[0]); ans.append(parts[1])
        
        if not qs: return "Source file empty."

        # Generate Neural Vectors
        vecs = self.encoder.encode(qs, convert_to_tensor=True)
        
        # Merge with existing knowledge (No overwriting!)
        self.memory["qs"].extend(qs)
        self.memory["as"].extend(ans)
        
        # Re-encode total knowledge for accuracy
        self.memory["vecs"] = self.encoder.encode(self.memory["qs"], convert_to_tensor=True)
        
        with open(VAULT_FILE, 'wb') as f:
            pickle.dump(self.memory, f)
            
        return f"Neural absorption complete. {len(qs)} new nodes added."

    def process(self, user_input):
        # 1. Semantic Vectorization
        # We mix current input with recent context for 'smarter' recall
        chat_context = " ".join(self.context[-1:]) + " " + user_input
        input_vec = self.encoder.encode(chat_context, convert_to_tensor=True)
        
        # 2. Search the Knowledge Vault
        results = util.semantic_search(input_vec, self.memory['vecs'], top_k=1)
        score = results[0][0]['score']
        idx = results[0][0]['corpus_id']

        # 3. Decision Logic
        if score > 0.40:
            response = self.memory['as'][idx]
            self.context.append(user_input)
            if len(self.context) > 5: self.context.pop(0)
            return response, score
        
        return "Query does not align with current neural training data.", score

# --- EXECUTION LOOP ---
bot = OmegaBot()
bot.startup()

console.print("[dim]MODES: [bold cyan]/learn file.txt[/bold cyan] | [bold magenta]/clear[/bold magenta] (Reset Memory) | [bold red]exit[/bold red][/dim]\n")

while True:
    try:
        user_in = Prompt.ask("[bold cyan]USER[/bold cyan]")
        
        if user_in.lower() in ['exit', 'quit']:
            console.print("[italic red]Closing neural links...[/italic red]")
            break

        # Command: /learn
        if user_in.startswith("/learn"):
            try:
                target = user_in.split(" ")[1]
                with console.status("[bold yellow]Absorbing new data...", spinner="aesthetic"):
                    report = bot.learn_logic(target)
                console.print(f"[bold green]✔[/bold green] {report}")
            except:
                console.print("[bold red]![/bold red] Usage: /learn yourfile.txt")
            continue
            
        # Command: /clear
        if user_in == "/clear":
            bot.context = []
            console.print("[bold yellow]Short-term context wiped.[/bold yellow]")
            continue

        # Thinking Animation
        with console.status("[bold magenta]Analyzing Intention...", spinner="simpleDots"):
            time.sleep(0.4) 
            reply, conf = bot.process(user_in)

        # Build Response UI
        bar_len = int(conf * 20)
        conf_bar = "█" * bar_len + "░" * (20 - bar_len)
        
        console.print(f"\n[bold magenta]OMEGA-AI[/bold magenta] [dim]Confidence: {conf:.2%}[/dim]")
        console.print(f"[cyan][{conf_bar}][/cyan]")
        console.print(Panel(reply, border_style="cyan" if conf > 0.6 else "yellow", title="[dim]Response[/dim]"))
        console.print(" ")

    except Exception as e:
        console.print(f"[bold red]CRITICAL ERROR:[/bold red] {e}")
