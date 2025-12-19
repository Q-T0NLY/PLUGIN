import React, { useState, useRef, useEffect } from 'react';
import styled from 'styled-components';
import ModelSelector from '../../../frontend/src/components/ModelSelector';
import EnsembleGauges from '../../../frontend/src/components/EnsembleGauges';

// ==================== 🎨 STYLED COMPONENTS ====================

const ChatContainer = styled.div`
  display: flex;
  height: 100vh;
  background: ${props => props.theme.background};
  color: ${props => props.theme.text_primary};
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  overflow: hidden;
`;

const ChatMain = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  background: ${props => props.theme.background};
`;

const ChatHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(90deg, ${props => props.theme.primary}, ${props => props.theme.secondary});
  border-bottom: 2px solid ${props => props.theme.border};
  box-shadow: ${props => props.theme.shadow};
`;

const HeaderInfo = styled.div`
  h2 {
    margin: 0;
    color: ${props => props.theme.text_primary};
    font-size: 18px;
    font-weight: 600;
  }
  
  p {
    margin: 4px 0 0 0;
    color: ${props => props.theme.text_secondary};
    font-size: 12px;
  }
`;

const HeaderActions = styled.div`
  display: flex;
  gap: 12px;
  
  button {
    background: transparent;
    border: none;
    color: ${props => props.theme.text_primary};
    font-size: 18px;
    cursor: pointer;
    transition: all 0.2s ease;
    
    &:hover {
      transform: scale(1.1);
      filter: brightness(1.2);
    }
  }
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: ${props => props.theme.background};
  scroll-behavior: smooth;
  
  &::-webkit-scrollbar {
    width: 8px;
  }
  
  &::-webkit-scrollbar-track {
    background: ${props => props.theme.surface};
  }
  
  &::-webkit-scrollbar-thumb {
    background: ${props => props.theme.primary};
    border-radius: 4px;
    
    &:hover {
      background: ${props => props.theme.secondary};
    }
  }
`;

const MessageRow = styled.div`
  display: flex;
  justify-content: ${props => props.isUser ? 'flex-end' : 'flex-start'};
  margin: 12px 0;
  animation: fadeInScale 0.3s ease-out;
  
  @keyframes fadeInScale {
    from {
      opacity: 0;
      transform: scale(0.95);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }
`;

const MessageBubble = styled.div`
  background: ${props => props.color}20;
  border: 2px solid ${props => props.color};
  border-radius: 12px;
  padding: 12px 16px;
  max-width: 70%;
  box-shadow: 0 0 10px ${props => props.color}40;
  backdrop-filter: blur(10px);
`;

const MessageContent = styled.div`
  color: ${props => props.theme.text_primary};
  word-wrap: break-word;
  line-height: 1.5;
  font-size: 14px;
`;

const MessageMeta = styled.div`
  font-size: 11px;
  color: ${props => props.theme.text_secondary};
  margin-top: 6px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
`;

const TypingIndicator = styled.div`
  display: flex;
  gap: 4px;
  align-items: center;
  
  .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: ${props => props.theme.primary};
    animation: typing 1.4s infinite;
    
    &:nth-child(2) {
      animation-delay: 0.2s;
    }
    
    &:nth-child(3) {
      animation-delay: 0.4s;
    }
  }
  
  @keyframes typing {
    0%, 60%, 100% {
      opacity: 0.3;
    }
    30% {
      opacity: 1;
    }
  }
`;

const InputContainer = styled.div`
  display: flex;
  gap: 8px;
  padding: 16px 20px;
  background: ${props => props.theme.surface};
  border-top: 1px solid ${props => props.theme.border}40;
`;

const ChatInput = styled.input`
  flex: 1;
  background: ${props => props.theme.background};
  border: 2px solid ${props => props.theme.border};
  border-radius: 8px;
  padding: 12px 16px;
  color: ${props => props.theme.text_primary};
  font-size: 14px;
  font-family: inherit;
  transition: all 0.2s ease;
  
  &:focus {
    outline: none;
    border-color: ${props => props.theme.primary};
    box-shadow: 0 0 10px ${props => props.theme.primary}40;
  }
  
  &::placeholder {
    color: ${props => props.theme.text_secondary}60;
  }
`;

const ActionButtons = styled.div`
  display: flex;
  gap: 8px;
`;

const ActionButton = styled.button`
  background: ${props => props.color}20;
  border: 2px solid ${props => props.color};
  border-radius: 8px;
  width: 40px;
  height: 40px;
  cursor: pointer;
  color: ${props => props.color};
  font-size: 18px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  
  &:hover {
    background: ${props => props.color}40;
    box-shadow: 0 0 10px ${props => props.color}60;
    transform: scale(1.05);
  }
  
  &:active {
    transform: scale(0.95);
  }
`;

const SendButton = styled(ActionButton)`
  background: linear-gradient(135deg, ${props => props.theme.primary}, ${props => props.theme.secondary});
  border: none;
  color: ${props => props.theme.text_primary};
`;

const Sidebar = styled.aside`
  width: 320px;
  background: ${props => props.theme.surface};
  border-right: 1px solid ${props => props.theme.border};
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  box-shadow: ${props => props.theme.shadow};
`;

const ThinkingBubble = styled.div`
  background: ${props => props.theme.accent}15;
  border-left: 3px solid ${props => props.theme.accent};
  border-radius: 8px;
  padding: 12px;
  margin: 8px 0;
  font-size: 12px;
  color: ${props => props.theme.text_secondary};
  font-style: italic;
  animation: expandIn 0.5s ease-out;
  
  @keyframes expandIn {
    from {
      opacity: 0;
      transform: scaleY(0);
      transform-origin: top;
    }
    to {
      opacity: 1;
      transform: scaleY(1);
    }
  }
`;

const ThinkingHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  
  .pulse {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: ${props => props.theme.accent};
    animation: pulse 1.5s infinite;
  }
  
  @keyframes pulse {
    0%, 100% {
      opacity: 1;
    }
    50% {
      opacity: 0.5;
    }
  }
`;

// ==================== ⚛️ REACT COMPONENTS ====================

const Message = ({ message, theme }) => {
  const isUser = message.role === 'user';
  const bubbleColor = isUser 
    ? theme.user_bubble 
    : message.role === 'assistant' 
    ? theme.assistant_bubble 
    : theme.system_bubble;

  return (
    <>
      <MessageRow isUser={isUser}>
        <MessageBubble color={bubbleColor}>
          <MessageContent theme={theme}>
            {message.content}
          </MessageContent>
          
          <MessageMeta theme={theme}>
            <span>{new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
            {isUser && <span>{message.status === 'delivered' ? '✓✓' : message.status === 'sent' ? '✓' : '⏳'}</span>}
          </MessageMeta>
          
          {message.confidence_score && message.confidence_score < 1.0 && (
            <div style={{ marginTop: '8px', paddingTop: '8px', borderTop: `1px solid ${bubbleColor}40`, fontSize: '11px', color: bubbleColor }}>
              🎯 Confidence: {Math.round(message.confidence_score * 100)}%
            </div>
          )}
        </MessageBubble>
      </MessageRow>
      
      {message.thinking_process && (
        <ThinkingBubble theme={theme}>
          <ThinkingHeader theme={theme}>
            <span>🧠 Thinking Process</span>
            <span className="pulse"></span>
          </ThinkingHeader>
          {message.thinking_process}
        </ThinkingBubble>
      )}
    </>
  );
};

const TypingIndicatorComponent = ({ theme }) => (
  <MessageRow isUser={false}>
    <MessageBubble color={theme.assistant_bubble}>
      <TypingIndicator theme={theme}>
        <div className="dot"></div>
        <div className="dot"></div>
        <div className="dot"></div>
      </TypingIndicator>
    </MessageBubble>
  </MessageRow>
);

const ChatboxDesign = ({ initialSession = null, theme = 'cyberpunk' }) => {
  const themes = {
    cyberpunk: {
      primary: '#FF00FF',
      secondary: '#00FFFF',
      accent: '#FFFF00',
      background: '#0A0A0A',
      surface: '#1A1A2E',
      user_bubble: '#FF00FF',
      assistant_bubble: '#00FFFF',
      system_bubble: '#FFD700',
      success: '#00FF00',
      warning: '#FFA500',
      error: '#FF0000',
      text_primary: '#FFFFFF',
      text_secondary: '#B0B0B0',
      border: '#FF00FF',
      shadow: '0 0 20px rgba(255, 0, 255, 0.5)'
    },
    matrix: {
      primary: '#00FF41',
      secondary: '#008F11',
      accent: '#00FF41',
      background: '#000000',
      surface: '#0A0A0A',
      user_bubble: '#00FF41',
      assistant_bubble: '#008F11',
      system_bubble: '#00FF41',
      success: '#00FF41',
      warning: '#FFFF00',
      error: '#FF0000',
      text_primary: '#00FF41',
      text_secondary: '#008F11',
      border: '#00FF41',
      shadow: '0 0 15px rgba(0, 255, 65, 0.4)'
    },
    ocean: {
      primary: '#00B4D8',
      secondary: '#0077B6',
      accent: '#90E0EF',
      background: '#000B1A',
      surface: '#001D3D',
      user_bubble: '#00B4D8',
      assistant_bubble: '#0077B6',
      system_bubble: '#90E0EF',
      success: '#38B000',
      warning: '#FFD000',
      error: '#FF0054',
      text_primary: '#E0F7FF',
      text_secondary: '#90E0EF',
      border: '#00B4D8',
      shadow: '0 0 15px rgba(0, 180, 216, 0.3)'
    }
  };

  const currentTheme = themes[theme] || themes.cyberpunk;

  const [messages, setMessages] = useState(initialSession?.messages || []);
  const [isTyping, setIsTyping] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [selectedModel, setSelectedModel] = useState(null);
  const [ensembleInput, setEnsembleInput] = useState(null);
  const messagesEndRef = useRef(null);

  const handleModelChange = (cfg) => {
    // cfg: { model_id, weights, ensemble }
    setSelectedModel(cfg?.model_id || null);
    if (cfg?.ensemble) {
      // build a simple model_scores object for the gauges (use weights normalized)
      const weights = cfg.weights || {};
      const max = Math.max(...Object.values(weights || {}).map(v => Number(v) || 0), 1);
      const model_scores = {};
      Object.keys(weights || {}).forEach(k => {
        model_scores[k] = Math.max(0, Math.min(1, (weights[k] || 0) / max));
      });
      setEnsembleInput({ model_scores, weights });
    } else {
      setEnsembleInput(null);
    }
  };

  // Auto-scroll to latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!inputValue.trim()) return;

    // Add user message
    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
      status: 'sent'
    };

    setMessages([...messages, userMessage]);
    setInputValue('');
    setIsTyping(true);

    // Simulate API response
    setTimeout(() => {
      const conf_base = selectedModel ? 0.94 : 0.9;
      const assistantMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `Model: ${selectedModel || 'default'} — Response to: "${inputValue}"`,
        timestamp: new Date(),
        status: 'delivered',
        confidence_score: conf_base,
        thinking_process: `Using model ${selectedModel || 'default'} — Analyzing input... Generating response... Validating output...`
      };

      setMessages(prev => [...prev, assistantMessage]);
      setIsTyping(false);
    }, 1500);
  };

  return (
    <ChatContainer theme={currentTheme}>
      <Sidebar theme={currentTheme}>
        <ModelSelector onChange={handleModelChange} />
        <EnsembleGauges apiInput={ensembleInput} />
      </Sidebar>
      <ChatMain>
        <ChatHeader theme={currentTheme}>
          <HeaderInfo theme={currentTheme}>
            <h2>💬 Enterprise AI Chat</h2>
            <p>{messages.length} messages</p>
          </HeaderInfo>
          <HeaderActions theme={currentTheme}>
            <button title="Settings">⚙️</button>
            <button title="Info">ℹ️</button>
            <button title="Theme">🎨</button>
          </HeaderActions>
        </ChatHeader>

        <MessagesContainer theme={currentTheme}>
          {messages.map(msg => (
            <Message key={msg.id} message={msg} theme={currentTheme} />
          ))}
          {isTyping && <TypingIndicatorComponent theme={currentTheme} />}
          <div ref={messagesEndRef} />
        </MessagesContainer>

        <InputContainer theme={currentTheme}>
          <ChatInput
            type="text"
            placeholder="Type your message..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage(e)}
            theme={currentTheme}
          />
          <ActionButtons>
            <ActionButton
              color={currentTheme.primary}
              title="Attach file"
              onClick={() => console.log('Attach')}
            >
              📎
            </ActionButton>
            <SendButton
              theme={currentTheme}
              title="Send message"
              onClick={handleSendMessage}
            >
              🚀
            </SendButton>
          </ActionButtons>
        </InputContainer>
      </ChatMain>
    </ChatContainer>
  );
};

export default ChatboxDesign;
