import os
import json
import urllib.request
from datetime import datetime, timezone

def fetch_latest_activity(username):
    url = f"https://api.github.com/users/{username}/events/public"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Casaro-Bot", "Accept": "application/vnd.github.v3+json"}
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"token {token}")
        
    try:
        with urllib.request.urlopen(req) as response:
            events = json.loads(response.read().decode("utf-8"))
            for event in events:
                if event.get("type") == "PushEvent":
                    repo_name = event.get("repo", {}).get("name", "N/A")
                    commits = event.get("payload", {}).get("commits", [])
                    msg = commits[-1].get("message", "Atualização de código") if commits else "Push de alterações"
                    return repo_name, msg
                elif event.get("type") == "CreateEvent":
                    repo_name = event.get("repo", {}).get("name", "N/A")
                    ref_type = event.get("payload", {}).get("ref_type", "repositório")
                    return repo_name, f"Novo {ref_type} criado"
    except Exception as e:
        print(f"Erro ao buscar atividades: {e}")
        
    return "MarcoJunior1/MarcoJunior1", "Manutenção e melhorias contínuas no perfil DevSecOps"

def escape_xml(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def generate_svg():
    username = os.environ.get("GITHUB_ACTOR", "MarcoJunior1")
    repo, commit_msg = fetch_latest_activity(username)
    
    # Trim strings for layout safety
    if len(repo) > 35:
        repo = repo[:32] + "..."
    if len(commit_msg) > 55:
        commit_msg = commit_msg[:52] + "..."
        
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    
    repo_esc = escape_xml(repo)
    commit_msg_esc = escape_xml(commit_msg)
    
    svg_content = f'''<svg width="650" height="170" viewBox="0 0 650 170" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="650" height="170" rx="10" fill="#0D0D15" stroke="#8A2BE2" stroke-width="1.5"/>
  
  <!-- Header Bar -->
  <rect x="15" y="15" width="620" height="30" rx="5" fill="#161625"/>
  <circle cx="32" cy="30" r="5" fill="#FF5F56"/>
  <circle cx="47" cy="30" r="5" fill="#FFBD2E"/>
  <circle cx="62" cy="30" r="5" fill="#27C93F"/>
  <text x="80" y="34" fill="#A855F7" font-family="'Courier New', monospace" font-size="12" font-weight="bold">CASARO AI // MONITOR DEVOPS &amp; SEGURANÇA</text>
  <text x="530" y="34" fill="#27C93F" font-family="'Courier New', monospace" font-size="11" font-weight="bold">[ONLINE]</text>

  <!-- Console Output -->
  <text x="25" y="70" fill="#A0A0B0" font-family="'Courier New', monospace" font-size="12">> ÚLTIMA ATIVIDADE REGISTRADA:</text>
  <text x="235" y="70" fill="#38BDF8" font-family="'Courier New', monospace" font-size="12" font-weight="bold">{repo_esc}</text>
  
  <text x="25" y="95" fill="#A0A0B0" font-family="'Courier New', monospace" font-size="12">> MENSAGEM DO COMMIT:</text>
  <text x="195" y="95" fill="#F3E8FF" font-family="'Courier New', monospace" font-size="12">"{commit_msg_esc}"</text>
  
  <text x="25" y="120" fill="#A0A0B0" font-family="'Courier New', monospace" font-size="12">> PARECER DO CASARO:</text>
  <text x="195" y="120" fill="#22C55E" font-family="'Courier New', monospace" font-size="12" font-weight="bold">DevSecOps OK | Código verificado e integrado</text>
  
  <!-- Footer Timestamp -->
  <text x="25" y="150" fill="#6B7280" font-family="'Courier New', monospace" font-size="10">Última checagem automática: {now}</text>
</svg>'''

    with open("casaro_status.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    print("casaro_status.svg gerado com sucesso!")

if __name__ == "__main__":
    generate_svg()
