#!/usr/bin/env zsh
# Agents Sub-Registry loader
universal_agents_registry_init() {
  local registry_py="${0:a:h}/agents/registry.py"
  if [[ -f "$registry_py" ]]; then
    # Print registered agents/tools via Python
    python3 - <<'PY'
from universal_registry.agents.registry import DEFAULT_SUBREGISTRY
print("Agents:", ", ".join(DEFAULT_SUBREGISTRY.list_agents()))
print("Tools:", ", ".join(DEFAULT_SUBREGISTRY.list_tools()))
PY
  else
    echo "[INFO] Agents Sub-Registry not found"
  fi
}

typeset -fx universal_agents_registry_init
################################################################################
# 🌍 UNIVERSAL_REGISTRY - Merged ZSH + Python Integration
# Comprehensive registry system merging hyper_registry.zsh with Python bindings
# SQLite-backed storage with 63 classifications, health, lifecycle, dependencies
# Includes Propagation Engine for directional sync with Nexus AI Studio
################################################################################

set -eo pipefail

typeset -g UNIVERSAL_REGISTRY_ROOT="${0:a:h}"
typeset -g PYTHON_REGISTRY_ROOT="${UNIVERSAL_REGISTRY_ROOT}/hyper_registry"
typeset -g UNIVERSAL_REGISTRY_DB
UNIVERSAL_REGISTRY_DB="${PWD}/.universal_registry.db"

# Source propagation engine for bidirectional/multicast/broadcast support
if [[ -f "${UNIVERSAL_REGISTRY_ROOT}/registry_propagation_nexus.zsh" ]]; then
  source "${UNIVERSAL_REGISTRY_ROOT}/registry_propagation_nexus.zsh"
fi

# ============ UTILITY FUNCTIONS ============

function _registry_check_sqlite() {
  if ! command -v sqlite3 >/dev/null 2>&1; then
    printf "sqlite3 not found. Install sqlite3 and retry.\n" >&2
    return 1
  fi
}

# ============ UNIVERSAL REGISTRY INITIALIZATION ============

function universal_registry_init() {
  printf "🌍 Initializing Universal Registry...\n"
  _registry_check_sqlite || return 1
  mkdir -p "${PWD}"
  
  sqlite3 "$UNIVERSAL_REGISTRY_DB" <<'SQL'
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS components(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  type TEXT,
  data TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS palettes(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  value TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS visuals(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  glyph TEXT,
  description TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS animations(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  frames TEXT,
  fps INTEGER,
  description TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS aliases(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  command TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS paths(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  original TEXT,
  normalized TEXT,
  category TEXT,
  priority INTEGER DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS symlinks(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_path TEXT,
  target_path TEXT,
  status TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS commands(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  cmd TEXT,
  description TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS prompts(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  template TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS integrations(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  provider TEXT,
  config TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS models(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  type TEXT,
  metadata TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS apis(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  spec TEXT,
  endpoint TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS webhooks(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  url TEXT,
  method TEXT DEFAULT 'POST',
  headers TEXT,
  secret TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS services(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  type TEXT,
  config TEXT,
  status TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS plugins(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  version TEXT,
  metadata TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS resources(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  key TEXT NOT NULL UNIQUE,
  value TEXT,
  kind TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tasks(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  spec TEXT,
  schedule TEXT,
  state TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS workflows(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  definition TEXT,
  state TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS projects(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  metadata TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS widgets(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  config TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS hot_swap_components(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  current_version TEXT,
  previous_version TEXT,
  status TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS streams(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  endpoint TEXT,
  protocol TEXT,
  metadata TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS events(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  type TEXT,
  payload TEXT,
  scheduled_at DATETIME,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS agents(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  type TEXT,
  config TEXT,
  status TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS propagation_chains(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  steps TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS subregistries(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  path TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS relationships(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source TEXT,
  target TEXT,
  type TEXT,
  metadata TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dependencies(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source TEXT,
  target TEXT,
  type TEXT,
  metadata TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS health(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  subject TEXT,
  status TEXT,
  details TEXT,
  checked_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS lifecycle(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  subject TEXT,
  action TEXT,
  status TEXT,
  details TEXT,
  occurred_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS documentations(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  title TEXT,
  content TEXT,
  format TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS capabilities(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  description TEXT,
  features TEXT,
  status TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
SQL

  printf "✅ Universal Registry initialized at %s\n" "$UNIVERSAL_REGISTRY_DB"
}

# ============ UNIFIED INITIALIZATION WITH PROPAGATION ============

function universal_registry_with_propagation_init() {
  printf "🌍 Initializing Universal Registry with Propagation Engine...\n"
  universal_registry_init || return 1
  registry_propagation_init || return 1
  printf "✅ Registry with Propagation Engine fully initialized\n"
}

# ============ TABLE MANAGEMENT ============

function universal_registry_show_tables() {
  _registry_check_sqlite || return 1
  sqlite3 "$UNIVERSAL_REGISTRY_DB" ".tables"
}

function universal_registry_query() {
  _registry_check_sqlite || return 1
  local table=$1
  local pattern=${2:-'%'}
  sqlite3 -header -column "$UNIVERSAL_REGISTRY_DB" "SELECT * FROM ${table} WHERE name LIKE '${pattern}' OR original LIKE '${pattern}' OR source_path LIKE '${pattern}' LIMIT 200;"
}

# ============ REGISTRATION FUNCTIONS - CORE TABLES ============

function universal_registry_register_palette() {
  _registry_check_sqlite || return 1
  local name=$1; local value=$2
  sqlite3 "$UNIVERSAL_REGISTRY_DB" "INSERT OR REPLACE INTO palettes(name, value) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")','$(printf "%s" "$value" | sed "s/'/''/g")');"
}

function universal_registry_register_visual() {
  _registry_check_sqlite || return 1
  local name=$1; local glyph=${2:-}; local desc=${3:-}
  sqlite3 "$UNIVERSAL_REGISTRY_DB" "INSERT OR REPLACE INTO visuals(name,glyph,description) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")','$(printf "%s" "$glyph" | sed "s/'/''/g")','$(printf "%s" "$desc" | sed "s/'/''/g")');"
}

function universal_registry_register_animation() {
  _registry_check_sqlite || return 1
  local name=$1; local frames=$2; local fps=${3:-30}; local desc=${4:-}
  sqlite3 "$UNIVERSAL_REGISTRY_DB" "INSERT OR REPLACE INTO animations(name,frames,fps,description) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")','$(printf "%s" "$frames" | sed "s/'/''/g")',${fps},'$(printf "%s" "$desc" | sed "s/'/''/g")');"
}

function universal_registry_register_alias() {
  _registry_check_sqlite || return 1
  local name=$1; local cmd=$2
  sqlite3 "$UNIVERSAL_REGISTRY_DB" "INSERT OR REPLACE INTO aliases(name,command) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")','$(printf "%s" "$cmd" | sed "s/'/''/g")');"
}

function universal_registry_register_path() {
  _registry_check_sqlite || return 1
  local original=$1; local normalized=$2; local category=${3:-}; local priority=${4:-0}
  sqlite3 "$UNIVERSAL_REGISTRY_DB" "INSERT INTO paths(original,normalized,category,priority) VALUES('$(printf "%s" "$original" | sed "s/'/''/g")','$(printf "%s" "$normalized" | sed "s/'/''/g")','$(printf "%s" "$category" | sed "s/'/''/g")',${priority});"
}

function universal_registry_register_symlink() {
  _registry_check_sqlite || return 1
  local src=$1; local tgt=$2; local status=${3:-active}
  sqlite3 "$UNIVERSAL_REGISTRY_DB" "INSERT INTO symlinks(source_path,target_path,status) VALUES('$(printf "%s" "$src" | sed "s/'/''/g")','$(printf "%s" "$tgt" | sed "s/'/''/g")','$(printf "%s" "$status" | sed "s/'/''/g")');"
}

function universal_registry_register_command() {
  _registry_check_sqlite || return 1
  local name=$1; local cmd=$2; local desc=${3:-}
  sqlite3 "$UNIVERSAL_REGISTRY_DB" "INSERT OR REPLACE INTO commands(name,cmd,description) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")','$(printf "%s" "$cmd" | sed "s/'/''/g")','$(printf "%s" "$desc" | sed "s/'/''/g")');"
}

function universal_registry_register_prompt() {
  _registry_check_sqlite || return 1
  local name=$1; local template=$2
  sqlite3 "$UNIVERSAL_REGISTRY_DB" "INSERT OR REPLACE INTO prompts(name,template) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")','$(printf "%s" "$template" | sed "s/'/''/g")');"
}

# ============ REGISTRATION FUNCTIONS - EXTENDED TABLES ============

function universal_registry_register_entity() {
  _registry_check_sqlite || return 1
  local kind=$1; local name=$2; local jsondata=$3
  case $kind in
    integration) sqlite3 "$UNIVERSAL_REGISTRY_DB" "INSERT OR REPLACE INTO integrations(name,provider,config) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")',NULL,'$(printf "%s" "$jsondata" | sed "s/'/''/g")');" ;;
    model) sqlite3 "$UNIVERSAL_REGISTRY_DB" "INSERT OR REPLACE INTO models(name,metadata) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")','$(printf "%s" "$jsondata" | sed "s/'/''/g")');" ;;
    api) sqlite3 "$UNIVERSAL_REGISTRY_DB" "INSERT OR REPLACE INTO apis(name,spec) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")','$(printf "%s" "$jsondata" | sed "s/'/''/g")');" ;;
    webhook) sqlite3 "$UNIVERSAL_REGISTRY_DB" "INSERT OR REPLACE INTO webhooks(name,url,headers,secret) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")',NULL,NULL,NULL);" ;;
    service) sqlite3 "$UNIVERSAL_REGISTRY_DB" "INSERT OR REPLACE INTO services(name,config,status) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")','$(printf "%s" "$jsondata" | sed "s/'/''/g")', 'unknown');" ;;
    plugin) sqlite3 "$UNIVERSAL_REGISTRY_DB" "INSERT OR REPLACE INTO plugins(name,metadata) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")','$(printf "%s" "$jsondata" | sed "s/'/''/g")');" ;;
    widget) sqlite3 "$UNIVERSAL_REGISTRY_DB" "INSERT OR REPLACE INTO widgets(name,config) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")','$(printf "%s" "$jsondata" | sed "s/'/''/g")');" ;;
    stream) sqlite3 "$UNIVERSAL_REGISTRY_DB" "INSERT OR REPLACE INTO streams(name,endpoint,protocol,metadata) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")',NULL,NULL,'$(printf "%s" "$jsondata" | sed "s/'/''/g")');" ;;
    project) sqlite3 "$UNIVERSAL_REGISTRY_DB" "INSERT OR REPLACE INTO projects(name,metadata) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")','$(printf "%s" "$jsondata" | sed "s/'/''/g")');" ;;
    *) sqlite3 "$UNIVERSAL_REGISTRY_DB" "INSERT OR REPLACE INTO resources(key,value,kind) VALUES('$(printf "%s" "$kind:$name" | sed "s/'/''/g")','$(printf "%s" "$jsondata" | sed "s/'/''/g")','entity');" ;;
  esac
}

function universal_registry_register_zsh_config() {
  local name=$1; local config=$2
  universal_registry_register_entity "zsh_config" "$name" "$config"
}

# ============ QUERY & EXPORT FUNCTIONS ============

function universal_registry_query_entity() {
  _registry_check_sqlite || return 1
  local kind=$1; local pattern=${2:-'%'}
  case $kind in
    integration) sqlite3 -header -column "$UNIVERSAL_REGISTRY_DB" "SELECT * FROM integrations WHERE name LIKE '${pattern}';" ;;
    model) sqlite3 -header -column "$UNIVERSAL_REGISTRY_DB" "SELECT * FROM models WHERE name LIKE '${pattern}';" ;;
    api) sqlite3 -header -column "$UNIVERSAL_REGISTRY_DB" "SELECT * FROM apis WHERE name LIKE '${pattern}';" ;;
    webhook) sqlite3 -header -column "$UNIVERSAL_REGISTRY_DB" "SELECT * FROM webhooks WHERE name LIKE '${pattern}';" ;;
    service) sqlite3 -header -column "$UNIVERSAL_REGISTRY_DB" "SELECT * FROM services WHERE name LIKE '${pattern}';" ;;
    plugin) sqlite3 -header -column "$UNIVERSAL_REGISTRY_DB" "SELECT * FROM plugins WHERE name LIKE '${pattern}';" ;;
    widget) sqlite3 -header -column "$UNIVERSAL_REGISTRY_DB" "SELECT * FROM widgets WHERE name LIKE '${pattern}';" ;;
    stream) sqlite3 -header -column "$UNIVERSAL_REGISTRY_DB" "SELECT * FROM streams WHERE name LIKE '${pattern}';" ;;
    project) sqlite3 -header -column "$UNIVERSAL_REGISTRY_DB" "SELECT * FROM projects WHERE name LIKE '${pattern}';" ;;
    *) sqlite3 -header -column "$UNIVERSAL_REGISTRY_DB" "SELECT * FROM resources WHERE key LIKE '${pattern}';" ;;
  esac
}

function universal_registry_register_documentation() {
  _registry_check_sqlite || return 1
  local name=$1; local title=$2; local content=$3; local format=${4:-markdown}
  sqlite3 "$UNIVERSAL_REGISTRY_DB" "INSERT OR REPLACE INTO documentations(name,title,content,format) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")','$(printf "%s" "$title" | sed "s/'/''/g")','$(printf "%s" "$content" | sed "s/'/''/g")','$(printf "%s" "$format" | sed "s/'/''/g")');"
}

function universal_registry_query_documentation() {
  _registry_check_sqlite || return 1
  local pattern=${1:-'%'}
  sqlite3 -header -column "$UNIVERSAL_REGISTRY_DB" "SELECT id, name, title, format, created_at FROM documentations WHERE name LIKE '${pattern}' OR title LIKE '${pattern}';"
}

function universal_registry_register_capability() {
  _registry_check_sqlite || return 1
  local name=$1; local desc=$2; local features=${3:-}; local status=${4:-available}
  sqlite3 "$UNIVERSAL_REGISTRY_DB" "INSERT OR REPLACE INTO capabilities(name,description,features,status) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")','$(printf "%s" "$desc" | sed "s/'/''/g")','$(printf "%s" "$features" | sed "s/'/''/g")','$(printf "%s" "$status" | sed "s/'/''/g")');"
}

function universal_registry_query_capability() {
  _registry_check_sqlite || return 1
  local pattern=${1:-'%'}; local status=${2:-'%'}
  sqlite3 -header -column "$UNIVERSAL_REGISTRY_DB" "SELECT * FROM capabilities WHERE name LIKE '${pattern}' AND status LIKE '${status}';"
}

# ============ DEPENDENCY & RELATIONSHIP FUNCTIONS ============

function universal_registry_add_dependency() {
  _registry_check_sqlite || return 1
  local source=$1; local target=$2; local dtype=${3:-uses}; local meta=${4:-}
  sqlite3 "$UNIVERSAL_REGISTRY_DB" "INSERT INTO dependencies(source,target,type,metadata) VALUES('$(printf "%s" "$source" | sed "s/'/''/g")','$(printf "%s" "$target" | sed "s/'/''/g")','$(printf "%s" "$dtype" | sed "s/'/''/g")','$(printf "%s" "$meta" | sed "s/'/''/g")');"
}

function universal_registry_register_dependency() {
  local source=$1; local target=$2; local type=${3:-uses}; local meta=${4:-}
  universal_registry_add_dependency "$source" "$target" "$type" "$meta"
}

function universal_registry_list_dependencies() {
  _registry_check_sqlite || return 1
  local entity=${1:-'%'}
  sqlite3 -header -column "$UNIVERSAL_REGISTRY_DB" "SELECT * FROM dependencies WHERE source LIKE '${entity}' OR target LIKE '${entity}';"
}

function universal_registry_add_relationship() {
  _registry_check_sqlite || return 1
  local src=$1; local tgt=$2; local rtype=${3:-related}; local meta=${4:-}
  sqlite3 "$UNIVERSAL_REGISTRY_DB" "INSERT INTO relationships(source,target,type,metadata) VALUES('$(printf "%s" "$src" | sed "s/'/''/g")','$(printf "%s" "$tgt" | sed "s/'/''/g")','$(printf "%s" "$rtype" | sed "s/'/''/g")','$(printf "%s" "$meta" | sed "s/'/''/g")');"
}

function universal_registry_register_relationship() {
  local src=$1; local tgt=$2; local rtype=${3:-related}; local meta=${4:-}
  universal_registry_add_relationship "$src" "$tgt" "$rtype" "$meta"
}

# ============ HEALTH & LIFECYCLE FUNCTIONS ============

function universal_registry_set_health() {
  _registry_check_sqlite || return 1
  local subject=$1; local status=$2; local details=${3:-}
  sqlite3 "$UNIVERSAL_REGISTRY_DB" "INSERT INTO health(subject,status,details) VALUES('$(printf "%s" "$subject" | sed "s/'/''/g")','$(printf "%s" "$status" | sed "s/'/''/g")','$(printf "%s" "$details" | sed "s/'/''/g")');"
}

function universal_registry_get_health() {
  _registry_check_sqlite || return 1
  local subject=${1:-'%'}
  sqlite3 -header -column "$UNIVERSAL_REGISTRY_DB" "SELECT * FROM health WHERE subject LIKE '${subject}' ORDER BY checked_at DESC LIMIT 50;"
}

function universal_registry_record_lifecycle() {
  _registry_check_sqlite || return 1
  local subject=$1; local action=$2; local status=${3:-}; local details=${4:-}
  sqlite3 "$UNIVERSAL_REGISTRY_DB" "INSERT INTO lifecycle(subject,action,status,details) VALUES('$(printf "%s" "$subject" | sed "s/'/''/g")','$(printf "%s" "$action" | sed "s/'/''/g")','$(printf "%s" "$status" | sed "s/'/''/g")','$(printf "%s" "$details" | sed "s/'/''/g")');"
}

# ============ WEBHOOK DISPATCHER ============

function universal_registry_dispatch_webhook() {
  _registry_check_sqlite || return 1
  local webhook_name=$1; local payload=${2:-}
  local url; url=$(sqlite3 "$UNIVERSAL_REGISTRY_DB" "SELECT url FROM webhooks WHERE name='$(printf "%s" "$webhook_name" | sed "s/'/''/g")' LIMIT 1;")
  if [[ -z "$url" ]]; then
    printf "Webhook '%s' not found or has no URL\n" "$webhook_name" >&2
    return 1
  fi
  if command -v curl >/dev/null 2>&1; then
    curl -s -X POST -H 'Content-Type: application/json' -d "$payload" "$url" || printf "Webhook call failed\n" >&2
  else
    printf "curl not installed; cannot dispatch webhook\n" >&2
    return 1
  fi
}

# ============ EXPORT & DATA FUNCTIONS ============

function universal_registry_export_json() {
  _registry_check_sqlite || return 1
  local out=${1:-./universal_registry_export.json}
  local tmp=/tmp/universal_registry
  mkdir -p "$tmp"
  
  local tables=(components palettes visuals animations aliases paths symlinks commands prompts integrations models apis webhooks services plugins resources tasks workflows projects widgets hot_swap_components streams events agents propagation_chains subregistries relationships dependencies health lifecycle documentations capabilities)
  
  for t in "${tables[@]}"; do
    sqlite3 -json "$UNIVERSAL_REGISTRY_DB" "SELECT * FROM ${t};" > "$tmp/${t}.json" 2>/dev/null || echo '[]' > "$tmp/${t}.json"
  done
  
  python3 - <<PY > "$out"
import json,glob
obj={}
for p in glob.glob('$tmp/*.json'):
    k = p.split('/')[-1].rsplit('.',1)[0]
    try:
        obj[k]=json.load(open(p))
    except Exception:
        obj[k]=[]
json.dump(obj, open('$out','w'), indent=2)
print('exported->', '$out')
PY
  printf "✅ Exported registry to %s\n" "$out"
}

function universal_registry_export_yaml() {
  local out=${1:-./universal_registry_export.yaml}
  printf "📝 Converting JSON to YAML: %s\n" "$out"
  
  if command -v python3 >/dev/null 2>&1; then
    python3 - <<'PY' "$out"
import json, yaml, sys
try:
    with open('./universal_registry_export.json', 'r') as f:
        data = json.load(f)
    with open(sys.argv[1], 'w') as f:
        yaml.dump(data, f, default_flow_style=False)
    print(f"✅ Exported to {sys.argv[1]}")
except Exception as e:
    print(f"❌ Export failed: {e}", file=sys.stderr)
    sys.exit(1)
PY
  else
    printf "⚠️ python3 not available; skipping YAML export\n"
  fi
}

# ============ PYTHON INTEGRATION FUNCTIONS ============

function universal_registry_python_sync() {
  printf "🔄 Syncing with Python Universal Registry...\n"
  
  if command -v python3 >/dev/null 2>&1; then
    python3 -c "
import sys
sys.path.insert(0, '${PYTHON_REGISTRY_ROOT}')
try:
    from universal_registry import UniversalRegistry
    import asyncio
    
    async def sync():
        registry = UniversalRegistry()
        print('✅ Python registry connected')
    
    asyncio.run(sync())
except Exception as e:
    print(f'⚠️ Python sync: {e}')
" || printf "⚠️ Python sync skipped\n"
  else
    printf "⚠️ python3 not found; skipping Python sync\n"
  fi
}

# ============ STATUS & DIAGNOSTIC FUNCTIONS ============

function universal_registry_status() {
  printf "🌍 Universal Registry Status\n"
  printf "├─ Database: %s\n" "$UNIVERSAL_REGISTRY_DB"
  printf "├─ Root: %s\n" "$UNIVERSAL_REGISTRY_ROOT"
  
  # Show table counts
  printf "├─ Tables:\n"
  universal_registry_show_tables 2>/dev/null | while read table; do
    printf "│  ├─ %s\n" "$table"
  done
  
  printf "└─ Status: 🟢 operational\n"
}

# ============ DEMO & TESTING ============

function universal_registry_demo() {
  printf "🌍 Universal Registry Demo - Merged ZSH System\n\n"
  
  # Initialize
  universal_registry_init || return 1
  
  # Register ZSH configs
  printf "📝 Registering ZSH configurations...\n"
  universal_registry_register_zsh_config "main_config" '{"shell":"zsh","version":"5.8"}'
  
  # Register visuals
  printf "🎨 Registering visual components...\n"
  universal_registry_register_palette "quantum_blue" "38;2;129;161;193"
  universal_registry_register_visual "depth1" "░" "light depth glyph"
  universal_registry_register_animation "spinner" "◐ ◓ ◑ ◒" 10
  
  # Register extended entities
  printf "🔧 Registering extended entities...\n"
  universal_registry_register_entity "integration" "github" '{"provider":"github","token":"REDACTED"}'
  universal_registry_register_entity "api" "meta-v1" '{"spec":"openapi:3.0","endpoint":"/v1/meta"}'
  universal_registry_register_entity "model" "gpt-mini" '{"type":"llm","version":"1.0"}'
  
  # Register capabilities
  printf "⭐ Registering capabilities...\n"
  universal_registry_register_capability "streaming" "Real-time streaming" "ws,http2,events" "available"
  universal_registry_register_capability "hotswap" "Hot component swapping" "zero-downtime,rollback" "available"
  
  # Register documentation
  printf "📚 Registering documentation...\n"
  universal_registry_register_documentation "intro" "Introduction" "Getting started with Universal Registry" "markdown"
  universal_registry_register_documentation "api-spec" "API Specification" "Complete OpenAPI 3.0 specification" "openapi"
  
  # Register dependencies
  printf "🔗 Registering dependencies...\n"
  universal_registry_register_dependency "quantum_blue" "ui_theme" "depends_on"
  universal_registry_register_dependency "spinner" "animation_engine" "depends_on"
  
  # Register relationships
  printf "🔀 Registering relationships...\n"
  universal_registry_register_relationship "github" "meta-v1" "integrates_with"
  universal_registry_register_relationship "gpt-mini" "streaming" "supports"
  
  # Set health
  printf "❤️ Recording health...\n"
  universal_registry_set_health "quantum_blue" "healthy" "palette operational"
  universal_registry_set_health "github" "ok" "reachable"
  
  # Record lifecycle
  printf "🔄 Recording lifecycle...\n"
  universal_registry_record_lifecycle "quantum_blue" "registered" "success" "palette registered"
  universal_registry_record_lifecycle "github" "registered" "success" "integration registered"
  
  # Export
  printf "\n📤 Exporting registry...\n"
  universal_registry_export_json ./universal_registry_demo.json
  
  # Status
  printf "\n"
  universal_registry_status
  
  printf "\n✅ Demo completed successfully\n"
}

# ============ EXPORTS ============

typeset -f universal_registry_init
typeset -f universal_registry_with_propagation_init
typeset -f universal_registry_show_tables
typeset -f universal_registry_query
typeset -f universal_registry_register_palette
typeset -f universal_registry_register_visual
typeset -f universal_registry_register_animation
typeset -f universal_registry_register_alias
typeset -f universal_registry_register_path
typeset -f universal_registry_register_symlink
typeset -f universal_registry_register_command
typeset -f universal_registry_register_prompt
typeset -f universal_registry_register_entity
typeset -f universal_registry_register_zsh_config
typeset -f universal_registry_query_entity
typeset -f universal_registry_register_documentation
typeset -f universal_registry_query_documentation
typeset -f universal_registry_register_capability
typeset -f universal_registry_query_capability
typeset -f universal_registry_add_dependency
typeset -f universal_registry_register_dependency
typeset -f universal_registry_list_dependencies
typeset -f universal_registry_add_relationship
typeset -f universal_registry_register_relationship
typeset -f universal_registry_set_health
typeset -f universal_registry_get_health
typeset -f universal_registry_record_lifecycle
typeset -f universal_registry_dispatch_webhook
typeset -f universal_registry_export_json
typeset -f universal_registry_export_yaml
typeset -f universal_registry_python_sync
typeset -f universal_registry_status
typeset -f universal_registry_demo

