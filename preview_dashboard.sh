#!/bin/bash
# Quick preview of the NEXUS AI Studio dashboard

# Source the modules
source /workspaces/ZSH/ZSH-main/zsh-config/ultra-zsh/modules/ai_chatbox.zsh

# Mock metrics for demo
metrics="25.5:74.5:8.2:16.0:99.99"

echo "════════════════════════════════════════════════════════════════════════════════"
echo "                    🚀 NEXUS AI STUDIO DASHBOARD PREVIEW"
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""
echo "This is the main dashboard interface you'll see when launching:"
echo "  $ nexus-chat"
echo ""
echo "────────────────────────────────────────────────────────────────────────────────"
echo ""

# Render dashboard
_nexus_render_dashboard_with_chat "$metrics"

echo ""
echo "────────────────────────────────────────────────────────────────────────────────"
echo ""
echo "Key Features Shown:"
echo "  ✅ 3D ASCII Art Header with NEXUS branding"
echo "  ✅ System Metadata (file, path, version, theme)"
echo "  ✅ Live Telemetry (GEFS, Health, Risk, Performance, Uptime)"
echo "  ✅ AI Conversation Section (for real-time chat)"
echo "  ✅ Prompt Input Area (DoneDeal@Dons-MBP prompt)"
echo "  ✅ Sharp frame rendering with box-drawing characters"
echo "  ✅ Perfect symmetry and centered content"
echo "  ✅ Auto-scaling to terminal width"
echo "  ✅ 16-bit RGB color compatibility"
echo ""
echo "Interactive Commands:"
echo "  • Type any question or command"
echo "  • /help   - Show available commands"
echo "  • /models - Switch AI provider/model"
echo "  • /clear  - Clear conversation history"
echo "  • /exit   - Exit chatbox"
echo ""
echo "════════════════════════════════════════════════════════════════════════════════"
