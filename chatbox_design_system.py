"""
🎨 ADVANCED ENTERPRISE CHATBOX DESIGN SYSTEM
Multi-Modal Chat Interface with 3D Animations, Real-time Streaming,
and Advanced Visual Feedback Components
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime


class ChatMessageRole(Enum):
    """Chat message roles"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    AGENT = "agent"


class MessageStatusEnum(Enum):
    """Message delivery status"""
    SENDING = "sending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"


@dataclass
class ChatMessage:
    """Enhanced chat message with metadata"""
    id: str
    role: ChatMessageRole
    content: str
    timestamp: datetime
    status: MessageStatusEnum = MessageStatusEnum.SENT
    metadata: Dict[str, Any] = None
    embedded_attachments: List[Dict[str, Any]] = None
    thinking_process: Optional[str] = None
    confidence_score: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status.value,
            "metadata": self.metadata or {},
            "attachments": self.embedded_attachments or [],
            "thinking": self.thinking_process,
            "confidence": self.confidence_score
        }


@dataclass
class ChatSession:
    """Chat session management"""
    session_id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    messages: List[ChatMessage] = None
    title: str = "New Chat"
    theme: str = "cyberpunk"
    language: str = "en"
    archived: bool = False
    
    def __post_init__(self):
        if self.messages is None:
            self.messages = []


class ChatboxDesignSpec:
    """Comprehensive chatbox design specification"""
    
    # ==================== 🎨 COLOR SCHEMES ====================
    THEMES = {
        "cyberpunk": {
            "primary": "#FF00FF",
            "secondary": "#00FFFF",
            "accent": "#FFFF00",
            "background": "#0A0A0A",
            "surface": "#1A1A2E",
            "user_bubble": "#FF00FF",
            "assistant_bubble": "#00FFFF",
            "system_bubble": "#FFD700",
            "success": "#00FF00",
            "warning": "#FFA500",
            "error": "#FF0000",
            "text_primary": "#FFFFFF",
            "text_secondary": "#B0B0B0",
            "border": "#FF00FF",
            "shadow": "0 0 20px rgba(255, 0, 255, 0.5)"
        },
        "matrix": {
            "primary": "#00FF41",
            "secondary": "#008F11",
            "accent": "#00FF41",
            "background": "#000000",
            "surface": "#0A0A0A",
            "user_bubble": "#00FF41",
            "assistant_bubble": "#008F11",
            "system_bubble": "#00FF41",
            "success": "#00FF41",
            "warning": "#FFFF00",
            "error": "#FF0000",
            "text_primary": "#00FF41",
            "text_secondary": "#008F11",
            "border": "#00FF41",
            "shadow": "0 0 15px rgba(0, 255, 65, 0.4)"
        },
        "ocean": {
            "primary": "#00B4D8",
            "secondary": "#0077B6",
            "accent": "#90E0EF",
            "background": "#000B1A",
            "surface": "#001D3D",
            "user_bubble": "#00B4D8",
            "assistant_bubble": "#0077B6",
            "system_bubble": "#90E0EF",
            "success": "#38B000",
            "warning": "#FFD000",
            "error": "#FF0054",
            "text_primary": "#E0F7FF",
            "text_secondary": "#90E0EF",
            "border": "#00B4D8",
            "shadow": "0 0 15px rgba(0, 180, 216, 0.3)"
        },
        "forest": {
            "primary": "#2D6A4F",
            "secondary": "#40916C",
            "accent": "#52B788",
            "background": "#081C15",
            "surface": "#1B4332",
            "user_bubble": "#2D6A4F",
            "assistant_bubble": "#40916C",
            "system_bubble": "#52B788",
            "success": "#52B788",
            "warning": "#D4A574",
            "error": "#E63946",
            "text_primary": "#E8F5E9",
            "text_secondary": "#A8D5BA",
            "border": "#52B788",
            "shadow": "0 0 15px rgba(45, 106, 79, 0.3)"
        },
        "minimal": {
            "primary": "#2C2C2C",
            "secondary": "#4A4A4A",
            "accent": "#6C6C6C",
            "background": "#F5F5F5",
            "surface": "#FFFFFF",
            "user_bubble": "#2C2C2C",
            "assistant_bubble": "#4A4A4A",
            "system_bubble": "#6C6C6C",
            "success": "#4CAF50",
            "warning": "#FF9800",
            "error": "#F44336",
            "text_primary": "#212121",
            "text_secondary": "#757575",
            "border": "#E0E0E0",
            "shadow": "0 2px 8px rgba(0, 0, 0, 0.1)"
        }
    }
    
    # ==================== 📐 LAYOUT SPECIFICATIONS ====================
    LAYOUT_SPECS = {
        "desktop": {
            "width": "100%",
            "max_width": "1200px",
            "height": "600px",
            "sidebar_width": "280px",
            "input_height": "80px",
            "message_max_width": "70%",
            "font_size": "14px",
            "border_radius": "12px"
        },
        "tablet": {
            "width": "100%",
            "max_width": "100%",
            "height": "500px",
            "sidebar_width": "240px",
            "input_height": "70px",
            "message_max_width": "80%",
            "font_size": "13px",
            "border_radius": "10px"
        },
        "mobile": {
            "width": "100%",
            "max_width": "100%",
            "height": "100vh",
            "sidebar_width": "0px",
            "input_height": "60px",
            "message_max_width": "90%",
            "font_size": "12px",
            "border_radius": "8px"
        }
    }
    
    # ==================== 🎬 ANIMATION SPECS ====================
    ANIMATIONS = {
        "message_appear": {
            "duration": "0.3s",
            "timing": "ease-out",
            "effect": "fadeInScale"
        },
        "typing_indicator": {
            "duration": "1.4s",
            "timing": "ease-in-out",
            "effect": "bounce"
        },
        "message_send": {
            "duration": "0.2s",
            "timing": "ease-in",
            "effect": "slideUp"
        },
        "thought_bubble": {
            "duration": "0.5s",
            "timing": "ease-out",
            "effect": "expandIn"
        },
        "glow_pulse": {
            "duration": "2s",
            "timing": "ease-in-out",
            "effect": "glowPulse"
        }
    }
    
    # ==================== 🎯 COMPONENT SIZES ====================
    COMPONENT_SIZES = {
        "avatar": {
            "small": "28px",
            "medium": "36px",
            "large": "48px"
        },
        "icons": {
            "small": "16px",
            "medium": "20px",
            "large": "24px"
        },
        "spacing": {
            "xs": "4px",
            "sm": "8px",
            "md": "12px",
            "lg": "16px",
            "xl": "24px"
        }
    }


# ==================== 🎨 VISUAL COMPONENTS ====================

class TypingIndicator:
    """Advanced typing indicator with animations"""
    
    STYLES = {
        "dots": {
            "html": '<span class="dot"></span><span class="dot"></span><span class="dot"></span>',
            "animation": "typing 1.4s infinite"
        },
        "wave": {
            "html": '<span class="wave"></span><span class="wave"></span><span class="wave"></span>',
            "animation": "wave 1.4s infinite"
        },
        "pulse": {
            "html": '<span class="pulse"></span>',
            "animation": "pulse 2s infinite"
        },
        "morph": {
            "html": '<span class="morph-dot"></span>',
            "animation": "morph 1.4s infinite"
        }
    }
    
    def __init__(self, style: str = "dots"):
        self.style = style
    
    def to_html(self) -> str:
        """Generate HTML for typing indicator"""
        style_spec = self.STYLES.get(self.style, self.STYLES["dots"])
        return f"""
        <div class="typing-indicator" style="animation: {style_spec['animation']}">
            {style_spec['html']}
        </div>
        """


class MessageBubble:
    """Message bubble component with rich styling"""
    
    def __init__(self, message: ChatMessage, theme: str = "cyberpunk"):
        self.message = message
        self.theme = theme
        self.colors = ChatboxDesignSpec.THEMES[theme]
    
    def to_html(self) -> str:
        """Generate HTML for message bubble"""
        bubble_color = (
            self.colors["user_bubble"] if self.message.role == ChatMessageRole.USER
            else self.colors["assistant_bubble"] if self.message.role == ChatMessageRole.ASSISTANT
            else self.colors["system_bubble"]
        )
        
        align = "flex-end" if self.message.role == ChatMessageRole.USER else "flex-start"
        
        html = f"""
        <div class="message-container" style="display: flex; justify-content: {align}; margin: 12px 0;">
            <div class="message-bubble" style="
                background: {bubble_color}20;
                border: 2px solid {bubble_color};
                border-radius: 12px;
                padding: 12px 16px;
                max-width: 70%;
                box-shadow: 0 0 10px {bubble_color}40;
                animation: fadeInScale 0.3s ease-out;
            ">
                <div class="message-content" style="
                    color: {self.colors['text_primary']};
                    word-wrap: break-word;
                    line-height: 1.5;
                ">
                    {self.message.content}
                </div>
                <div class="message-meta" style="
                    font-size: 11px;
                    color: {self.colors['text_secondary']};
                    margin-top: 6px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                ">
                    <span>{self.message.timestamp.strftime('%H:%M')}</span>
                    {self._render_status_icon()}
                </div>
                {self._render_confidence_score()}
            </div>
        </div>
        """
        return html
    
    def _render_status_icon(self) -> str:
        """Render message status indicator"""
        icons = {
            MessageStatusEnum.SENDING: "⏳",
            MessageStatusEnum.SENT: "✓",
            MessageStatusEnum.DELIVERED: "✓✓",
            MessageStatusEnum.READ: "✓✓",
            MessageStatusEnum.FAILED: "✗"
        }
        return f"<span>{icons.get(self.message.status, '')}</span>"
    
    def _render_confidence_score(self) -> str:
        """Render confidence score if applicable"""
        if self.message.role == ChatMessageRole.ASSISTANT and self.message.confidence_score < 1.0:
            confidence_pct = int(self.message.confidence_score * 100)
            color = (
                self.colors["success"] if confidence_pct > 80
                else self.colors["warning"] if confidence_pct > 60
                else self.colors["error"]
            )
            return f"""
            <div class="confidence-score" style="
                margin-top: 8px;
                padding-top: 8px;
                border-top: 1px solid {color}40;
                font-size: 11px;
                color: {color};
            ">
                🎯 Confidence: {confidence_pct}%
            </div>
            """
        return ""


class ThinkingProcess:
    """Display AI thinking process"""
    
    def __init__(self, thinking_text: str, theme: str = "cyberpunk"):
        self.thinking_text = thinking_text
        self.theme = theme
        self.colors = ChatboxDesignSpec.THEMES[theme]
    
    def to_html(self) -> str:
        """Generate HTML for thinking process"""
        return f"""
        <div class="thinking-process" style="
            background: {self.colors['accent']}15;
            border-left: 3px solid {self.colors['accent']};
            border-radius: 8px;
            padding: 12px;
            margin: 8px 0;
            font-size: 12px;
            color: {self.colors['text_secondary']};
            font-style: italic;
            animation: expandIn 0.5s ease-out;
        ">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                <span>🧠 Thinking Process</span>
                <span class="pulse" style="
                    width: 8px;
                    height: 8px;
                    border-radius: 50%;
                    background: {self.colors['accent']};
                    animation: pulse 1.5s infinite;
                "></span>
            </div>
            <div>{self.thinking_text}</div>
        </div>
        """


class InputField:
    """Advanced chat input field"""
    
    def __init__(self, theme: str = "cyberpunk", placeholder: str = "Type your message..."):
        self.theme = theme
        self.placeholder = placeholder
        self.colors = ChatboxDesignSpec.THEMES[theme]
    
    def to_html(self) -> str:
        """Generate HTML for input field"""
        return f"""
        <div class="input-container" style="
            display: flex;
            gap: 8px;
            padding: 16px;
            background: {self.colors['surface']};
            border-top: 1px solid {self.colors['border']}40;
        ">
            <!-- Text Input -->
            <input 
                type="text"
                placeholder="{self.placeholder}"
                class="chat-input"
                style="
                    flex: 1;
                    background: {self.colors['background']};
                    border: 2px solid {self.colors['border']};
                    border-radius: 8px;
                    padding: 12px;
                    color: {self.colors['text_primary']};
                    font-size: 14px;
                    transition: all 0.2s ease;
                "
            />
            
            <!-- Action Buttons -->
            <div class="input-actions" style="display: flex; gap: 8px;">
                <!-- Attachment Button -->
                <button class="action-btn" title="Attach file" style="
                    background: {self.colors['primary']}20;
                    border: 2px solid {self.colors['primary']};
                    border-radius: 8px;
                    width: 40px;
                    height: 40px;
                    cursor: pointer;
                    color: {self.colors['primary']};
                    font-size: 18px;
                    transition: all 0.2s ease;
                ">
                    📎
                </button>
                
                <!-- Send Button -->
                <button class="send-btn" title="Send message" style="
                    background: linear-gradient(135deg, {self.colors['primary']}, {self.colors['secondary']});
                    border: none;
                    border-radius: 8px;
                    width: 40px;
                    height: 40px;
                    cursor: pointer;
                    color: {self.colors['text_primary']};
                    font-size: 18px;
                    transition: all 0.2s ease;
                    box-shadow: 0 0 10px {self.colors['primary']}40;
                ">
                    🚀
                </button>
            </div>
        </div>
        """


class ChatHeader:
    """Chat header with session info"""
    
    def __init__(self, session: ChatSession):
        self.session = session
        self.colors = ChatboxDesignSpec.THEMES[session.theme]
    
    def to_html(self) -> str:
        """Generate HTML for chat header"""
        return f"""
        <div class="chat-header" style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px;
            background: linear-gradient(90deg, {self.colors['primary']}, {self.colors['secondary']});
            border-bottom: 2px solid {self.colors['border']};
            box-shadow: {self.colors['shadow']};
        ">
            <div class="header-info">
                <h2 style="
                    margin: 0;
                    color: {self.colors['text_primary']};
                    font-size: 18px;
                    font-weight: 600;
                ">{self.session.title}</h2>
                <p style="
                    margin: 4px 0 0 0;
                    color: {self.colors['text_secondary']};
                    font-size: 12px;
                ">{len(self.session.messages)} messages</p>
            </div>
            
            <div class="header-actions" style="display: flex; gap: 8px;">
                <button title="Settings" style="
                    background: transparent;
                    border: none;
                    color: {self.colors['text_primary']};
                    font-size: 18px;
                    cursor: pointer;
                ">⚙️</button>
                
                <button title="Info" style="
                    background: transparent;
                    border: none;
                    color: {self.colors['text_primary']};
                    font-size: 18px;
                    cursor: pointer;
                ">ℹ️</button>
            </div>
        </div>
        """


class ChatSidebar:
    """Chat history sidebar"""
    
    def __init__(self, sessions: List[ChatSession], theme: str = "cyberpunk"):
        self.sessions = sessions
        self.theme = theme
        self.colors = ChatboxDesignSpec.THEMES[theme]
    
    def to_html(self) -> str:
        """Generate HTML for sidebar"""
        sessions_html = "\n".join([
            f"""
            <div class="session-item" style="
                padding: 12px;
                margin: 8px 0;
                background: {self.colors['surface']}60;
                border-left: 3px solid {self.colors['primary']};
                border-radius: 6px;
                cursor: pointer;
                transition: all 0.2s ease;
            ">
                <div style="color: {self.colors['text_primary']}; font-weight: 600;">{session.title}</div>
                <div style="color: {self.colors['text_secondary']}; font-size: 11px; margin-top: 4px;">
                    {len(session.messages)} messages
                </div>
            </div>
            """
            for session in self.sessions
        ])
        
        return f"""
        <div class="chat-sidebar" style="
            width: 280px;
            height: 100%;
            background: {self.colors['background']};
            border-right: 1px solid {self.colors['border']};
            overflow-y: auto;
            padding: 16px;
        ">
            <div class="sidebar-header" style="margin-bottom: 20px;">
                <button style="
                    width: 100%;
                    background: linear-gradient(135deg, {self.colors['primary']}, {self.colors['secondary']});
                    border: none;
                    border-radius: 8px;
                    padding: 12px;
                    color: {self.colors['text_primary']};
                    cursor: pointer;
                    font-weight: 600;
                    transition: all 0.2s ease;
                ">
                    ➕ New Chat
                </button>
            </div>
            
            <div class="sessions-list">
                {sessions_html}
            </div>
        </div>
        """


class FullChatInterface:
    """Complete chatbox interface"""
    
    def __init__(self, session: ChatSession):
        self.session = session
        self.colors = ChatboxDesignSpec.THEMES[session.theme]
    
    def to_html(self) -> str:
        """Generate complete chat interface HTML"""
        # Build message list
        messages_html = "\n".join([
            MessageBubble(msg, self.session.theme).to_html()
            for msg in self.session.messages
        ])
        
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Enterprise AI Chatbox</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: {self.colors['background']};
                    color: {self.colors['text_primary']};
                    overflow: hidden;
                }}
                
                .chat-container {{
                    display: flex;
                    height: 100vh;
                    background: {self.colors['background']};
                }}
                
                .chat-main {{
                    flex: 1;
                    display: flex;
                    flex-direction: column;
                }}
                
                .messages-container {{
                    flex: 1;
                    overflow-y: auto;
                    padding: 20px;
                    background: {self.colors['background']};
                    scroll-behavior: smooth;
                }}
                
                .messages-container::-webkit-scrollbar {{
                    width: 8px;
                }}
                
                .messages-container::-webkit-scrollbar-track {{
                    background: {self.colors['surface']};
                }}
                
                .messages-container::-webkit-scrollbar-thumb {{
                    background: {self.colors['primary']};
                    border-radius: 4px;
                }}
                
                @keyframes fadeInScale {{
                    from {{
                        opacity: 0;
                        transform: scale(0.95);
                    }}
                    to {{
                        opacity: 1;
                        transform: scale(1);
                    }}
                }}
                
                @keyframes typing {{
                    0%, 60%, 100% {{ opacity: 0.3; }}
                    30% {{ opacity: 1; }}
                }}
                
                @keyframes wave {{
                    0%, 100% {{ transform: translateY(0px); }}
                    50% {{ transform: translateY(-10px); }}
                }}
                
                @keyframes pulse {{
                    0%, 100% {{ opacity: 1; }}
                    50% {{ opacity: 0.5; }}
                }}
                
                @keyframes expandIn {{
                    from {{
                        opacity: 0;
                        transform: scaleY(0);
                        transform-origin: top;
                    }}
                    to {{
                        opacity: 1;
                        transform: scaleY(1);
                    }}
                }}
                
                @keyframes glowPulse {{
                    0%, 100% {{
                        box-shadow: 0 0 10px {self.colors['primary']}40;
                    }}
                    50% {{
                        box-shadow: 0 0 20px {self.colors['primary']}80;
                    }}
                }}
                
                .dot {{
                    animation: typing 1.4s infinite;
                    margin: 0 2px;
                }}
                
                .dot:nth-child(2) {{
                    animation-delay: 0.2s;
                }}
                
                .dot:nth-child(3) {{
                    animation-delay: 0.4s;
                }}
            </style>
        </head>
        <body>
            <div class="chat-container">
                <div class="chat-main">
                    {ChatHeader(self.session).to_html()}
                    
                    <div class="messages-container">
                        {messages_html}
                    </div>
                    
                    {InputField(self.session.theme).to_html()}
                </div>
            </div>
        </body>
        </html>
        """


# ==================== 📊 DESIGN EXPORT ====================

if __name__ == "__main__":
    import json
    
    # Export design specification
    design_export = {
        "themes": ChatboxDesignSpec.THEMES,
        "layouts": ChatboxDesignSpec.LAYOUT_SPECS,
        "animations": ChatboxDesignSpec.ANIMATIONS,
        "components": ChatboxDesignSpec.COMPONENT_SIZES
    }
    
    print(json.dumps(design_export, indent=2))
