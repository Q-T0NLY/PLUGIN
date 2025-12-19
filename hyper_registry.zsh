#!/usr/bin/env zsh
################################################################################
# Hyper Registry - Dynamic Universal Registry (SQLite-backed)
# Stores: components, palettes, visuals, animations, aliases, paths, symlinks, commands, prompts
# Usage:
#   source hyper_registry.zsh
#   hyper_registry_init
#   hyper_registry_register_palette "quantum_blue" "38;2;129;161;193"
#   hyper_registry_query "palettes" "quantum%"
#   hyper_registry_export_json ./hyper_registry_export.json
################################################################################

set -euo pipefail

typeset -g HYPER_REGISTRY_DB
HYPER_REGISTRY_DB="${PWD}/.hyper_registry.db"

function _hyper_check_sqlite() {
  if ! command -v sqlite3 >/dev/null 2>&1; then
    printf "sqlite3 not found. Install sqlite3 and retry.\n" >&2
    return 1
  fi
}

function hyper_registry_init() {
  _hyper_check_sqlite || return 1
  mkdir -p "${PWD}"
  sqlite3 "$HYPER_REGISTRY_DB" <<'SQL'
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
SQL

  printf "Hyper Registry initialized at %s\n" "$HYPER_REGISTRY_DB"
}

function hyper_registry_show_tables() {
  _hyper_check_sqlite || return 1
  sqlite3 "$HYPER_REGISTRY_DB" ".tables"
}

function hyper_registry_query() {
  _hyper_check_sqlite || return 1
  local table=$1
  local pattern=${2:-'%'}
  sqlite3 -header -column "$HYPER_REGISTRY_DB" "SELECT * FROM ${table} WHERE name LIKE '${pattern}' OR original LIKE '${pattern}' OR source_path LIKE '${pattern}' LIMIT 200;"
}

# Generic upsert by name for simple tables with 'name'
function _hyper_upsert_name() {
  local table=$1; shift
  local name=$1; shift
  local rest_sql=$*
  sqlite3 "$HYPER_REGISTRY_DB" <<SQL
BEGIN;
INSERT INTO ${table} (name, ${rest_sql%%VALUES*})
VALUES ('${name}', ${rest_sql#*VALUES });
ON CONFLICT(name) DO UPDATE SET ${rest_sql#*VALUES } ;
COMMIT;
SQL
}

function hyper_registry_register_palette() {
  _hyper_check_sqlite || return 1
  local name=$1; local value=$2
  sqlite3 "$HYPER_REGISTRY_DB" "INSERT OR REPLACE INTO palettes(name, value) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")','$(printf "%s" "$value" | sed "s/'/''/g")');"
}

function hyper_registry_register_visual() {
  _hyper_check_sqlite || return 1
  local name=$1; local glyph=${2:-}; local desc=${3:-}
  sqlite3 "$HYPER_REGISTRY_DB" "INSERT OR REPLACE INTO visuals(name,glyph,description) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")','$(printf "%s" "$glyph" | sed "s/'/''/g")','$(printf "%s" "$desc" | sed "s/'/''/g")');"
}

function hyper_registry_register_animation() {
  _hyper_check_sqlite || return 1
  local name=$1; local frames=$2; local fps=${3:-30}; local desc=${4:-}
  sqlite3 "$HYPER_REGISTRY_DB" "INSERT OR REPLACE INTO animations(name,frames,fps,description) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")','$(printf "%s" "$frames" | sed "s/'/''/g")',${fps},'$(printf "%s" "$desc" | sed "s/'/''/g")');"
}

function hyper_registry_register_alias() {
  _hyper_check_sqlite || return 1
  local name=$1; local cmd=$2
  sqlite3 "$HYPER_REGISTRY_DB" "INSERT OR REPLACE INTO aliases(name,command) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")','$(printf "%s" "$cmd" | sed "s/'/''/g")');"
}

function hyper_registry_register_path() {
  _hyper_check_sqlite || return 1
  local original=$1; local normalized=$2; local category=${3:-}; local priority=${4:-0}
  sqlite3 "$HYPER_REGISTRY_DB" "INSERT INTO paths(original,normalized,category,priority) VALUES('$(printf "%s" "$original" | sed "s/'/''/g")','$(printf "%s" "$normalized" | sed "s/'/''/g")','$(printf "%s" "$category" | sed "s/'/''/g")',${priority});"
}

function hyper_registry_register_symlink() {
  _hyper_check_sqlite || return 1
  local src=$1; local tgt=$2; local status=${3:-active}
  sqlite3 "$HYPER_REGISTRY_DB" "INSERT INTO symlinks(source_path,target_path,status) VALUES('$(printf "%s" "$src" | sed "s/'/''/g")','$(printf "%s" "$tgt" | sed "s/'/''/g")','$(printf "%s" "$status" | sed "s/'/''/g")');"
}

function hyper_registry_register_command() {
  _hyper_check_sqlite || return 1
  local name=$1; local cmd=$2; local desc=${3:-}
  sqlite3 "$HYPER_REGISTRY_DB" "INSERT OR REPLACE INTO commands(name,cmd,description) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")','$(printf "%s" "$cmd" | sed "s/'/''/g")','$(printf "%s" "$desc" | sed "s/'/''/g")');"
}

function hyper_registry_register_prompt() {
  _hyper_check_sqlite || return 1
  local name=$1; local template=$2
  sqlite3 "$HYPER_REGISTRY_DB" "INSERT OR REPLACE INTO prompts(name,template) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")','$(printf "%s" "$template" | sed "s/'/''/g")');"
}

function hyper_registry_export_json() {
  _hyper_check_sqlite || return 1
  local out=${1:-./hyper_registry_export.json}
  # Export each table to JSON-ish arrays (simple concatenation)
  sqlite3 -json "$HYPER_REGISTRY_DB" "SELECT * FROM components;" > /tmp/hyper_components.json || true
  sqlite3 -json "$HYPER_REGISTRY_DB" "SELECT * FROM palettes;" > /tmp/hyper_palettes.json || true
  sqlite3 -json "$HYPER_REGISTRY_DB" "SELECT * FROM visuals;" > /tmp/hyper_visuals.json || true
  sqlite3 -json "$HYPER_REGISTRY_DB" "SELECT * FROM animations;" > /tmp/hyper_animations.json || true
  sqlite3 -json "$HYPER_REGISTRY_DB" "SELECT * FROM aliases;" > /tmp/hyper_aliases.json || true
  sqlite3 -json "$HYPER_REGISTRY_DB" "SELECT * FROM paths;" > /tmp/hyper_paths.json || true
  sqlite3 -json "$HYPER_REGISTRY_DB" "SELECT * FROM symlinks;" > /tmp/hyper_symlinks.json || true
  sqlite3 -json "$HYPER_REGISTRY_DB" "SELECT * FROM commands;" > /tmp/hyper_commands.json || true
  sqlite3 -json "$HYPER_REGISTRY_DB" "SELECT * FROM prompts;" > /tmp/hyper_prompts.json || true

  # Merge into single JSON object (best-effort)
  python3 - <<PY > "$out"
import json,sys
def load(p):
    try:
        return json.load(open(p))
    except Exception:
        return []
obj={
    'components': load('/tmp/hyper_components.json'),
    'palettes': load('/tmp/hyper_palettes.json'),
    'visuals': load('/tmp/hyper_visuals.json'),
    'animations': load('/tmp/hyper_animations.json'),
    'aliases': load('/tmp/hyper_aliases.json'),
    'paths': load('/tmp/hyper_paths.json'),
    'symlinks': load('/tmp/hyper_symlinks.json'),
    'commands': load('/tmp/hyper_commands.json'),
    'prompts': load('/tmp/hyper_prompts.json')
}
json.dump(obj, open('$out','w'), indent=2)
print('exported->', '$out')
PY
  printf "Exported registry to %s\n" "$out"
}

# Quick demo helper
function hyper_registry_demo() {
  hyper_registry_init
  hyper_registry_register_palette "quantum_blue" "38;2;129;161;193"
  hyper_registry_register_visual "depth1" "░" "light depth glyph"
  hyper_registry_register_animation "spinner1" "◐ ◓ ◑ ◒" 10 "basic spinner"
  hyper_registry_register_alias "nmenu" "qnti_menu"
  hyper_registry_register_command "hyper-demo" "echo hello" "demo command"
  hyper_registry_register_prompt "nova" "%n@%m %1~ %#"
  printf "Demo entries inserted.\n"
  hyper_registry_show_tables
}

export -f hyper_registry_init hyper_registry_show_tables hyper_registry_query hyper_registry_export_json hyper_registry_demo

# --- Extended schema migration and helpers ---
function hyper_registry_extend_schema() {
  _hyper_check_sqlite || return 1
  sqlite3 "$HYPER_REGISTRY_DB" <<'SQL'
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
  printf "Extended schema applied.\n"
}

# Generic entity registration: stores JSON/meta in 'resources' table keyed by kind:name when appropriate
function hyper_registry_register_entity() {
  _hyper_check_sqlite || return 1
  local kind=$1; local name=$2; local jsondata=$3
  case $kind in
    integration) sqlite3 "$HYPER_REGISTRY_DB" "INSERT OR REPLACE INTO integrations(name,provider,config) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")',NULL,'$(printf "%s" "$jsondata" | sed "s/'/''/g")');" ;;
    model) sqlite3 "$HYPER_REGISTRY_DB" "INSERT OR REPLACE INTO models(name,metadata) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")','$(printf "%s" "$jsondata" | sed "s/'/''/g")');" ;;
    api) sqlite3 "$HYPER_REGISTRY_DB" "INSERT OR REPLACE INTO apis(name,spec) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")','$(printf "%s" "$jsondata" | sed "s/'/''/g")');" ;;
    webhook) sqlite3 "$HYPER_REGISTRY_DB" "INSERT OR REPLACE INTO webhooks(name,url,headers,secret) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")',NULL,NULL,NULL);" ;;
    service) sqlite3 "$HYPER_REGISTRY_DB" "INSERT OR REPLACE INTO services(name,config,status) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")','$(printf "%s" "$jsondata" | sed "s/'/''/g")', 'unknown');" ;;
    plugin) sqlite3 "$HYPER_REGISTRY_DB" "INSERT OR REPLACE INTO plugins(name,metadata) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")','$(printf "%s" "$jsondata" | sed "s/'/''/g")');" ;;
    widget) sqlite3 "$HYPER_REGISTRY_DB" "INSERT OR REPLACE INTO widgets(name,config) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")','$(printf "%s" "$jsondata" | sed "s/'/''/g")');" ;;
    stream) sqlite3 "$HYPER_REGISTRY_DB" "INSERT OR REPLACE INTO streams(name,endpoint,protocol,metadata) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")',NULL,NULL,'$(printf "%s" "$jsondata" | sed "s/'/''/g")');" ;;
    project) sqlite3 "$HYPER_REGISTRY_DB" "INSERT OR REPLACE INTO projects(name,metadata) VALUES('$(printf "%s" "$name" | sed "s/'/''/g")','$(printf "%s" "$jsondata" | sed "s/'/''/g")');" ;;
    *) sqlite3 "$HYPER_REGISTRY_DB" "INSERT OR REPLACE INTO resources(key,value,kind) VALUES('$(printf "%s" "$kind:$name" | sed "s/'/''/g")','$(printf "%s" "$jsondata" | sed "s/'/''/g")','entity');" ;;
  esac
}

function hyper_registry_query_entity() {
  _hyper_check_sqlite || return 1
  local kind=$1; local pattern=${2:-'%'}
  case $kind in
    integration) sqlite3 -header -column "$HYPER_REGISTRY_DB" "SELECT * FROM integrations WHERE name LIKE '${pattern}';" ;;
    model) sqlite3 -header -column "$HYPER_REGISTRY_DB" "SELECT * FROM models WHERE name LIKE '${pattern}';" ;;
    api) sqlite3 -header -column "$HYPER_REGISTRY_DB" "SELECT * FROM apis WHERE name LIKE '${pattern}';" ;;
    webhook) sqlite3 -header -column "$HYPER_REGISTRY_DB" "SELECT * FROM webhooks WHERE name LIKE '${pattern}';" ;;
    service) sqlite3 -header -column "$HYPER_REGISTRY_DB" "SELECT * FROM services WHERE name LIKE '${pattern}';" ;;
    plugin) sqlite3 -header -column "$HYPER_REGISTRY_DB" "SELECT * FROM plugins WHERE name LIKE '${pattern}';" ;;
    widget) sqlite3 -header -column "$HYPER_REGISTRY_DB" "SELECT * FROM widgets WHERE name LIKE '${pattern}';" ;;
    stream) sqlite3 -header -column "$HYPER_REGISTRY_DB" "SELECT * FROM streams WHERE name LIKE '${pattern}';" ;;
    project) sqlite3 -header -column "$HYPER_REGISTRY_DB" "SELECT * FROM projects WHERE name LIKE '${pattern}';" ;;
    *) sqlite3 -header -column "$HYPER_REGISTRY_DB" "SELECT * FROM resources WHERE key LIKE '${pattern}';" ;;
  esac
}

# Dependency and relationship helpers
function hyper_registry_add_dependency() {
  _hyper_check_sqlite || return 1
  local source=$1; local target=$2; local dtype=${3:-uses}; local meta=${4:-}
  sqlite3 "$HYPER_REGISTRY_DB" "INSERT INTO dependencies(source,target,type,metadata) VALUES('$(printf "%s" "$source" | sed "s/'/''/g")','$(printf "%s" "$target" | sed "s/'/''/g")','$(printf "%s" "$dtype" | sed "s/'/''/g")','$(printf "%s" "$meta" | sed "s/'/''/g")');"
}

function hyper_registry_list_dependencies() {
  _hyper_check_sqlite || return 1
  local entity=${1:-'%'}
  sqlite3 -header -column "$HYPER_REGISTRY_DB" "SELECT * FROM dependencies WHERE source LIKE '${entity}' OR target LIKE '${entity}';"
}

function hyper_registry_add_relationship() {
  _hyper_check_sqlite || return 1
  local src=$1; local tgt=$2; local rtype=${3:-related}; local meta=${4:-}
  sqlite3 "$HYPER_REGISTRY_DB" "INSERT INTO relationships(source,target,type,metadata) VALUES('$(printf "%s" "$src" | sed "s/'/''/g")','$(printf "%s" "$tgt" | sed "s/'/''/g")','$(printf "%s" "$rtype" | sed "s/'/''/g")','$(printf "%s" "$meta" | sed "s/'/''/g")');"
}

# Health & lifecycle
function hyper_registry_set_health() {
  _hyper_check_sqlite || return 1
  local subject=$1; local status=$2; local details=${3:-}
  sqlite3 "$HYPER_REGISTRY_DB" "INSERT INTO health(subject,status,details) VALUES('$(printf "%s" "$subject" | sed "s/'/''/g")','$(printf "%s" "$status" | sed "s/'/''/g")','$(printf "%s" "$details" | sed "s/'/''/g")');"
}

function hyper_registry_get_health() {
  _hyper_check_sqlite || return 1
  local subject=${1:-'%'}
  sqlite3 -header -column "$HYPER_REGISTRY_DB" "SELECT * FROM health WHERE subject LIKE '${subject}' ORDER BY checked_at DESC LIMIT 50;"
}

function hyper_registry_record_lifecycle() {
  _hyper_check_sqlite || return 1
  local subject=$1; local action=$2; local status=${3:-}; local details=${4:-}
  sqlite3 "$HYPER_REGISTRY_DB" "INSERT INTO lifecycle(subject,action,status,details) VALUES('$(printf "%s" "$subject" | sed "s/'/''/g")','$(printf "%s" "$action" | sed "s/'/''/g")','$(printf "%s" "$status" | sed "s/'/''/g")','$(printf "%s" "$details" | sed "s/'/''/g")');"
}

# Documentation helpers
function hyper_registry_register_documentation() {
  _hyper_check_sqlite || return 1
  local name=$1; local title=$2; local content=$3; local format=${4:-markdown}
  sqlite3 "$HYPER_REGISTRY_DB" "INSERT OR REPLACE INTO documentations(name,title,content,format) VALUES('$(printf \"%s\" \"$name\" | sed \"s/'/''/g")\'$(printf \"%s\" \"$title\" | sed \"s/'/''/g")\'$(printf \"%s\" \"$content\" | sed \"s/'/''/g")\'$(printf \"%s\" \"$format\" | sed \"s/'/''/g\")');"
}

function hyper_registry_query_documentation() {
  _hyper_check_sqlite || return 1
  local pattern=${1:-'%'}
  sqlite3 -header -column "$HYPER_REGISTRY_DB" "SELECT id, name, title, format, created_at FROM documentations WHERE name LIKE '${pattern}' OR title LIKE '${pattern}';"
}

# Capability helpers
function hyper_registry_register_capability() {
  _hyper_check_sqlite || return 1
  local name=$1; local desc=$2; local features=${3:-}; local status=${4:-available}
  sqlite3 "$HYPER_REGISTRY_DB" "INSERT OR REPLACE INTO capabilities(name,description,features,status) VALUES('$(printf \"%s\" \"$name\" | sed \"s/'/''/g")\'$(printf \"%s\" \"$desc\" | sed \"s/'/''/g")\'$(printf \"%s\" \"$features\" | sed \"s/'/''/g")\'$(printf \"%s\" \"$status\" | sed \"s/'/''/g\")');"
}

function hyper_registry_query_capability() {
  _hyper_check_sqlite || return 1
  local pattern=${1:-'%'}; local status=${2:-'%'}
  sqlite3 -header -column "$HYPER_REGISTRY_DB" "SELECT * FROM capabilities WHERE name LIKE '${pattern}' AND status LIKE '${status}';"
}

# Webhook dispatcher template (simple, safe)
function hyper_registry_dispatch_webhook() {
  _hyper_check_sqlite || return 1
  local webhook_name=$1; local payload=${2:-}
  local url; url=$(sqlite3 "$HYPER_REGISTRY_DB" "SELECT url FROM webhooks WHERE name='$(printf "%s" "$webhook_name" | sed "s/'/''/g")' LIMIT 1;")
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

# Extend export to include new tables
function hyper_registry_export_json() {
  _hyper_check_sqlite || return 1
  local out=${1:-./hyper_registry_export.json}
  local tmp=/tmp/hyper
  mkdir -p "$tmp"
  local tables=(components palettes visuals animations aliases paths symlinks commands prompts integrations models apis webhooks services plugins resources tasks workflows projects widgets hot_swap_components streams events agents propagation_chains subregistries relationships dependencies health lifecycle documentations capabilities)
  for t in "${tables[@]}"; do
    sqlite3 -json "$HYPER_REGISTRY_DB" "SELECT * FROM ${t};" > "$tmp/${t}.json" 2>/dev/null || echo '[]' > "$tmp/${t}.json"
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
  printf "Exported registry to %s\n" "$out"
}

# Update demo to call extended schema and add example entities
function hyper_registry_demo() {
  hyper_registry_init
  hyper_registry_extend_schema
  hyper_registry_register_palette "quantum_blue" "38;2;129;161;193"
  hyper_registry_register_visual "depth1" "░" "light depth glyph"
  hyper_registry_register_animation "spinner1" "◐ ◓ ◑ ◒" 10 "basic spinner"
  hyper_registry_register_alias "nmenu" "qnti_menu"
  hyper_registry_register_command "hyper-demo" "echo hello" "demo command"
  hyper_registry_register_prompt "nova" "%n@%m %1~ %#"
  hyper_registry_register_entity integration "github" '{"provider":"github","token":"REDACTED"}'
  hyper_registry_register_entity api "meta-v1" '{"spec":"openapi:3.0","endpoint":"/v1/meta"}'
  hyper_registry_register_entity model "gpt-mini" '{"type":"llm","version":"1.0"}'
  hyper_registry_register_documentation "hyper-guide" "Hyper Registry Guide" "This is the main documentation for the Hyper Registry system." "markdown"
  hyper_registry_register_documentation "api-spec" "API Specification" "Complete OpenAPI 3.0 specification for all endpoints." "openapi"
  hyper_registry_register_capability "streaming" "Real-time streaming data via WebSocket" "ws,http2,events" "available"
  hyper_registry_register_capability "webhook" "Event-driven webhook dispatching" "post,retry,auth" "available"
  hyper_registry_register_capability "health-check" "Periodic health monitoring" "tcp,http,custom" "available"
  hyper_registry_set_health "github" "ok" "reachable"
  hyper_registry_record_lifecycle "github" "registered" "success" "init"
  printf "Demo extended entries inserted.\n"
  hyper_registry_show_tables
}

export -f hyper_registry_init hyper_registry_show_tables hyper_registry_query hyper_registry_export_json hyper_registry_demo hyper_registry_extend_schema hyper_registry_register_entity hyper_registry_query_entity hyper_registry_add_dependency hyper_registry_list_dependencies hyper_registry_add_relationship hyper_registry_set_health hyper_registry_get_health hyper_registry_record_lifecycle hyper_registry_dispatch_webhook hyper_registry_register_documentation hyper_registry_query_documentation hyper_registry_register_capability hyper_registry_query_capability
