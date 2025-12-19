#!/usr/bin/env zsh
# Advanced TODO System

: "${TODO_FILE:=${HOME}/.config/ultra-zsh/todo/todos.json}"
: "${TODO_STATS:=${HOME}/.config/ultra-zsh/todo/stats.json}"

# Initialize TODO file if it doesn't exist
[[ ! -f "${TODO_FILE}" ]] && echo '[]' > "${TODO_FILE}"

todo_add() {
    local task="$1"
    local priority="${2:-medium}"
    local due_date="$3"
    local tags="$4"
    local assignee="$5"
    
    if [[ -z "${task}" ]]; then
        echo "Usage: todo_add <task> [priority] [due_date] [tags] [assignee]"
        echo "Priorities: low, medium, high, critical"
        return 1
    fi
    
    local id=$(date +%s)
    local created=$(date -Iseconds)
    local todo_json=$(cat "${TODO_FILE}")
    
    # Add new TODO using jq
    if command -v jq >/dev/null 2>&1; then
        echo "${todo_json}" | jq ". + [{
            \"id\": ${id},
            \"task\": \"${task}\",
            \"priority\": \"${priority}\",
            \"status\": \"pending\",
            \"due_date\": \"${due_date:-}\",
            \"tags\": \"${tags:-}\",
            \"assignee\": \"${assignee:-}\",
            \"created\": \"${created}\",
            \"completed\": null
        }]" > "${TODO_FILE}"
        echo "✓ Added TODO: ${task}"
    else
        echo "Error: jq is required for TODO system"
        return 1
    fi
}

todo_list() {
    local filter="$1"
    
    if command -v jq >/dev/null 2>&1; then
        case "${filter}" in
            pending)
                jq -r '.[] | select(.status == "pending") | "\(.id) [\(.priority)] \(.task)"' "${TODO_FILE}"
                ;;
            completed)
                jq -r '.[] | select(.status == "completed") | "\(.id) ✓ \(.task)"' "${TODO_FILE}"
                ;;
            high|critical)
                jq -r ".[] | select(.priority == \"${filter}\" and .status == \"pending\") | \"\(.id) [\(.priority)] \(.task)\"" "${TODO_FILE}"
                ;;
            *)
                jq -r '.[] | "\(.id) [\(.priority)] \(.status) - \(.task)"' "${TODO_FILE}"
                ;;
        esac
    else
        echo "Error: jq is required for TODO system"
        return 1
    fi
}

todo_complete() {
    local id="$1"
    
    if [[ -z "${id}" ]]; then
        echo "Usage: todo_complete <id>"
        return 1
    fi
    
    if command -v jq >/dev/null 2>&1; then
        local todo_json=$(cat "${TODO_FILE}")
        echo "${todo_json}" | jq "(.[] | select(.id == ${id}) | .status) = \"completed\" | (.[] | select(.id == ${id}) | .completed) = \"$(date -Iseconds)\"" > "${TODO_FILE}"
        echo "✓ Completed TODO ${id}"
    else
        echo "Error: jq is required for TODO system"
        return 1
    fi
}

todo_stats() {
    if command -v jq >/dev/null 2>&1; then
        local total=$(jq '. | length' "${TODO_FILE}")
        local pending=$(jq '[.[] | select(.status == "pending")] | length' "${TODO_FILE}")
        local completed=$(jq '[.[] | select(.status == "completed")] | length' "${TODO_FILE}")
        local progress=$((completed * 100 / total))
        
        echo "TODO Statistics:"
        echo "  Total: ${total}"
        echo "  Pending: ${pending}"
        echo "  Completed: ${completed}"
        echo "  Progress: ${progress}%"
    else
        echo "Error: jq is required for TODO system"
        return 1
    fi
}

todo_export() {
    local format="${1:-json}"
    local output_file="$2"
    
    if [[ -z "${output_file}" ]]; then
        output_file="${HOME}/.config/ultra-zsh/todo/export_$(date +%Y%m%d_%H%M%S).${format}"
    fi
    
    case "${format}" in
        json)
            cp "${TODO_FILE}" "${output_file}"
            ;;
        csv)
            if command -v jq >/dev/null 2>&1; then
                jq -r '["id","task","priority","status","due_date","tags","assignee","created","completed"], (.[] | [.id, .task, .priority, .status, .due_date, .tags, .assignee, .created, .completed]) | @csv' "${TODO_FILE}" > "${output_file}"
            fi
            ;;
    esac
    
    echo "✓ Exported TODOs to ${output_file}"
}

