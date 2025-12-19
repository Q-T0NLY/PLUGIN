#!/usr/bin/env zsh
# Error Recovery System

: "${ERROR_LOG:=${HOME}/.config/ultra-zsh/logs/errors.log}"

error_handler() {
    local exit_code=$?
    local last_command=$(fc -ln -1)
    
    if [[ ${exit_code} -ne 0 ]]; then
        echo "✗ Command failed: ${last_command} (exit code: ${exit_code})"
        echo "$(date): Command '${last_command}' failed with exit code ${exit_code}" >> "${ERROR_LOG}"
        
        # Attempt recovery
        case "${last_command}" in
            *brew*)
                echo "Attempting to fix Homebrew..."
                brew doctor 2>&1 | tee -a "${ERROR_LOG}"
                ;;
            *git*)
                echo "Checking git status..."
                git status 2>&1 | tee -a "${ERROR_LOG}"
                ;;
        esac
    fi
}

set_error_handler() {
    precmd_functions+=(error_handler)
}

# Enable error recovery by default
set_error_handler

