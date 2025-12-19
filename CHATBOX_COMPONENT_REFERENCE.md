# 🧩 Chatbox Component Reference Guide

**Version**: 1.0.0  
**Status**: Complete  

---

## 📋 Component Index

| Component | File | Lines | Purpose |
|-----------|------|-------|---------|
| ChatboxDesign | `ChatboxDesign.jsx` | 450+ | Main container & orchestration |
| Message | `ChatboxDesign.jsx` | 100+ | Individual message display |
| ChatInput | Styled Component | 80+ | User input area |
| Header | Styled Component | 60+ | Top bar with controls |
| TypingIndicator | Styled Component | 30+ | "Assistant is typing" animation |

---

## 🎯 Component: ChatboxDesign

**Location**: `frontend/src/components/ChatboxDesign.jsx`

**Purpose**: Root container that orchestrates all chat functionality

### Props

```typescript
interface ChatboxDesignProps {
  // Session management
  initialSession?: ChatSession;
  
  // Theming
  theme?: 'cyberpunk' | 'matrix' | 'ocean' | 'midnight' | 'sunset';
  
  // Callbacks
  onMessageSent?: (message: ChatMessage) => void;
  onThemeChange?: (theme: string) => void;
  onError?: (error: Error) => void;
  
  // Configuration
  apiEndpoint?: string;        // Default: '/api/chat'
  enableWebSocket?: boolean;   // Default: false
  maxMessages?: number;        // Default: Infinity
  autoScroll?: boolean;        // Default: true
  showTimestamps?: boolean;    // Default: true
  showTypingIndicator?: boolean; // Default: true
  
  // Styling
  className?: string;
}
```

### Features

✅ **Message Management**
- Display conversation history
- Real-time message streaming
- Optimistic UI updates
- Message status indicators (sent, delivered, error)

✅ **User Interactions**
- Send messages with Enter key
- Multi-line input (Shift+Enter)
- File attachments
- Emoji reactions

✅ **Real-Time Features**
- WebSocket support
- Server-Sent Events (SSE) streaming
- Typing indicators
- Thinking process display

✅ **Theming**
- 5 built-in themes
- Custom theme creation
- Color scheme switching
- CSS variable injection

✅ **Accessibility**
- ARIA labels
- Keyboard navigation
- Focus indicators
- Screen reader support

### State Management

**Internal State**:
```typescript
interface ChatboxState {
  messages: ChatMessage[];        // All messages
  isTyping: boolean;              // Assistant typing
  inputValue: string;             // Current input
  selectedTheme: string;          // Current theme
  sessionId: string | null;       // Session ID
}
```

### Methods

```typescript
// Lifecycle
componentDidMount(): void;        // Initialize session
componentDidUpdate(): void;       // Auto-scroll on new messages

// Message Handling
handleSendMessage(content): void;
handleDeleteMessage(id): void;
handleEditMessage(id, content): void;
handleReaction(id, emoji): void;

// Theme Management
handleThemeChange(theme): void;

// Utilities
scrollToBottom(): void;
formatMessage(content): string;
getThemeColors(): ThemeColors;
```

### Example Usage

```jsx
import ChatboxDesign from './components/ChatboxDesign';
import './styles/chatbox.css';

export default function App() {
  return (
    <ChatboxDesign
      theme="cyberpunk"
      apiEndpoint="https://api.example.com/chat"
      enableWebSocket={true}
      maxMessages={500}
      onMessageSent={(msg) => {
        console.log('Message sent:', msg);
        // Track analytics, etc.
      }}
      onError={(err) => {
        console.error('Chat error:', err);
        // Show error notification
      }}
    />
  );
}
```

---

## 💬 Component: Message

**Location**: `frontend/src/components/ChatboxDesign.jsx` (nested component)

**Purpose**: Displays a single chat message with metadata and actions

### Props

```typescript
interface MessageProps {
  message: ChatMessage;
  theme: ThemeColors;
  
  // Callbacks
  onDelete?: (id: string) => void;
  onEdit?: (id: string, content: string) => void;
  onReact?: (id: string, emoji: string) => void;
  onReply?: (id: string) => void;
  
  // Options
  showActions?: boolean;        // Show edit/delete buttons
  showAvatar?: boolean;         // Show user avatar
  className?: string;
}
```

### ChatMessage Type

```typescript
interface ChatMessage {
  id: string;                           // Unique identifier
  role: 'user' | 'assistant' | 'system'; // Message sender
  content: string;                      // Message text
  timestamp: Date;                      // When sent
  status: 'sent' | 'delivered' | 'streaming' | 'error';
  
  // Optional fields
  thinking_process?: string;            // AI reasoning
  confidence_score?: number;            // 0.0 - 1.0
  tokens_used?: number;                 // Token count
  metadata?: Record<string, any>;       // Custom data
  reactions?: MessageReaction[];        // Emoji reactions
  replies?: string[];                   // Reply message IDs
}
```

### Styling

The Message component uses role-based styling:

```css
/* User messages */
.message-bubble.user {
  background: var(--color-user-bubble);
  border-color: var(--color-user-bubble);
  justify-content: flex-end;
}

/* Assistant messages */
.message-bubble.assistant {
  background: var(--color-assistant-bubble);
  border-color: var(--color-assistant-bubble);
  justify-content: flex-start;
}

/* System messages */
.message-bubble.system {
  background: var(--color-system-bubble);
  border-color: var(--color-system-bubble);
  justify-content: center;
}
```

### Features

**Display**:
- Syntax highlighting (code blocks)
- Markdown formatting
- Link previews
- Image thumbnails
- File previews

**Metadata**:
- Timestamp
- Read receipts (✓ sent, ✓✓ delivered)
- Confidence score display
- Processing time

**Thinking Process**:
```jsx
{message.thinking_process && (
  <ThinkingBubble>
    <ThinkingHeader>
      🧠 Thinking Process <span className="pulse"></span>
    </ThinkingHeader>
    {message.thinking_process}
  </ThinkingBubble>
)}
```

**Actions Menu**:
- Edit message (user only)
- Delete message (user only)
- React with emoji
- Reply to message
- Copy message
- Forward message

### Example Usage

```jsx
<Message
  message={{
    id: '1',
    role: 'assistant',
    content: 'Hello! How can I help you today?',
    timestamp: new Date(),
    status: 'delivered',
    confidence_score: 0.98,
    thinking_process: 'User greeted me, should respond warmly...'
  }}
  theme={currentTheme}
  onDelete={(id) => deleteMessage(id)}
  onReact={(id, emoji) => reactToMessage(id, emoji)}
  showActions={true}
/>
```

---

## ⌨️ Component: ChatInput

**Location**: Styled component in `ChatboxDesign.jsx`

**Purpose**: User input field with formatting and file attachments

### Props

```typescript
interface ChatInputProps {
  value: string;
  onChange: (value: string) => void;
  onSend: (message: string) => void;
  onAttach?: (files: File[]) => void;
  
  // Options
  placeholder?: string;         // Default: "Type your message..."
  disabled?: boolean;           // Disable input
  maxLength?: number;           // Character limit
  theme: ThemeColors;
  enableFormatting?: boolean;   // Show format toolbar
  enableEmojiPicker?: boolean;  // Show emoji picker
  className?: string;
}
```

### Features

✅ **Text Input**
- Multi-line support (grows with content)
- Character counter
- Max length enforcement
- Placeholder text

✅ **Keyboard Shortcuts**
- `Enter`: Send message
- `Shift+Enter`: New line
- `Ctrl+Z`: Undo
- `Ctrl+Y`: Redo
- `Ctrl+B`: Bold
- `Ctrl+I`: Italic
- `Ctrl+K`: Insert link

✅ **Formatting Toolbar**
- Bold, Italic, Underline, Strikethrough
- Code block insertion
- Link insertion
- List creation

✅ **File Attachments**
- Drag & drop support
- File picker
- Multi-file upload
- File type restrictions
- Size validation

✅ **Emoji Picker**
- Emoji search
- Recent emojis
- Category filtering
- Skin tone variants

### Styling

```css
.chatbox-input {
  flex: 1;
  background: var(--color-background);
  border: 2px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--spacing-md) var(--spacing-lg);
  color: var(--color-text-primary);
  font-size: var(--font-size-md);
  resize: none;
  max-height: 100px;
}

.chatbox-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 10px rgba(var(--color-primary), 0.4);
}
```

### Example Usage

```jsx
<ChatInput
  value={inputValue}
  onChange={(val) => setInputValue(val)}
  onSend={(msg) => {
    sendMessage(msg);
    setInputValue('');
  }}
  onAttach={(files) => uploadFiles(files)}
  placeholder="Ask me anything..."
  enableFormatting={true}
  enableEmojiPicker={true}
  theme={currentTheme}
/>
```

---

## 🎪 Component: Header

**Location**: Styled component in `ChatboxDesign.jsx`

**Purpose**: Top navigation bar with conversation info and controls

### Props

```typescript
interface HeaderProps {
  title: string;                // Conversation title
  status: 'online' | 'offline' | 'away';
  onlineCount?: number;         // Number of online users
  theme: ThemeColors;
  
  // Actions
  onSettings?: () => void;
  onInfo?: () => void;
  onThemeClick?: () => void;
  onMenuClick?: () => void;
}
```

### Features

✅ **Display**
- Conversation title
- Online status indicator
- User count
- Last update timestamp

✅ **Action Buttons**
- Settings (⚙️)
- Info (ℹ️)
- Theme selector (🎨)
- Menu (☰)

✅ **Styling**
- Gradient background
- Neon glow effect
- Responsive layout
- Mobile-optimized

### Styling

```css
.chatbox-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-lg) var(--spacing-xl);
  background: linear-gradient(
    90deg,
    var(--color-primary),
    var(--color-secondary)
  );
  border-bottom: 2px solid var(--color-border);
  box-shadow: var(--shadow-lg);
}

.chatbox-header-actions button {
  background: transparent;
  border: none;
  color: var(--color-text-primary);
  font-size: var(--font-size-xl);
  cursor: pointer;
  transition: all var(--transition-normal);
}

.chatbox-header-actions button:hover {
  transform: scale(1.1);
  filter: brightness(1.2);
}
```

### Example Usage

```jsx
<header className="chatbox-header">
  <div className="chatbox-header-info">
    <h2>💬 Enterprise AI Chat</h2>
    <p>Online • 42 messages</p>
  </div>
  <div className="chatbox-header-actions">
    <button onClick={handleSettings}>⚙️</button>
    <button onClick={handleInfo}>ℹ️</button>
    <button onClick={handleTheme}>🎨</button>
  </div>
</header>
```

---

## ⏳ Component: TypingIndicator

**Location**: Styled component in `ChatboxDesign.jsx`

**Purpose**: Animated indicator showing assistant is typing

### Props

```typescript
interface TypingIndicatorProps {
  theme: ThemeColors;
  message?: string;    // Custom message (default: blank)
}
```

### Features

✅ **Animation**
- Pulsing dots
- Smooth transition
- Customizable speed
- Accessible animation

✅ **Display**
- Shows assistant is thinking
- Inline with messages
- Clear visual feedback

### Styling & Animation

```css
.typing-indicator {
  display: flex;
  gap: var(--spacing-xs);
  align-items: center;
}

.typing-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-primary);
  animation: typing 1.4s infinite;
}

@keyframes typing {
  0%, 60%, 100% {
    opacity: 0.3;
  }
  30% {
    opacity: 1;
  }
}
```

### Example Usage

```jsx
{isTyping && <TypingIndicator theme={currentTheme} />}
```

---

## 🧠 Component: ThinkingBubble

**Location**: Styled component in `ChatboxDesign.jsx`

**Purpose**: Display AI reasoning process with visual feedback

### Props

```typescript
interface ThinkingBubbleProps {
  content: string;           // Thinking text
  theme: ThemeColors;
}
```

### Features

✅ **Display**
- Distinguishes thinking from response
- Shows step-by-step reasoning
- Visual pulsing indicator
- Collapsed/expanded toggle

✅ **Styling**
- Bordered container
- Italic text
- Different color scheme
- Animation on appear

### Styling & Animation

```css
.thinking-bubble {
  background: color-mix(in srgb, var(--color-accent) 15%, transparent);
  border-left: 3px solid var(--color-accent);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  font-style: italic;
  color: var(--color-text-secondary);
  animation: expandIn 0.5s ease-out;
}

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
```

### Example Usage

```jsx
{message.thinking_process && (
  <ThinkingBubble
    content={message.thinking_process}
    theme={currentTheme}
  />
)}
```

---

## 🎬 Animations

### Available Keyframes

| Name | Duration | Effect |
|------|----------|--------|
| fadeInScale | 0.3s | Fade in with scale |
| typing | 1.4s | Pulsing dots |
| expandIn | 0.5s | Vertical expand |
| slideIn | 0.3s | Slide from left |
| slideUp | 0.3s | Slide from bottom |
| glow | Infinite | Box shadow glow |
| pulse | 1.5s | Opacity pulse |

### Using Animations

```css
.my-element {
  animation: fadeInScale 0.3s ease-out;
}

.my-element.infinite {
  animation: pulse 1.5s infinite;
}
```

---

## 🌈 Theme Colors in Components

### CSS Variables Used

```css
/* Primary Colors */
--color-primary
--color-secondary
--color-accent

/* Backgrounds */
--color-background
--color-surface

/* Text */
--color-text-primary
--color-text-secondary

/* Message Bubbles */
--color-user-bubble
--color-assistant-bubble
--color-system-bubble

/* Status Colors */
--color-success
--color-warning
--color-error

/* Effects */
--color-border
--shadow-lg
```

### Dynamic Theme Application

```typescript
// Set theme via hook
const { applyTheme } = useTheme();
applyTheme('matrix');

// Or directly in component
<ChatboxDesign theme="ocean" />

// Or create custom
const { createCustomTheme } = useTheme();
createCustomTheme('custom', {
  primary: '#FF0000',
  secondary: '#00FF00'
});
```

---

## 📱 Responsive Behavior

### Breakpoints

| Size | Width | Changes |
|------|-------|---------|
| Desktop | > 1024px | Full UI, max message width 70% |
| Tablet | 768-1024px | Adjusted padding, 85% width |
| Mobile | < 768px | Stack layout, 95% width |
| Small | < 480px | Minimal padding, full width |

### Mobile-Specific Changes

```css
@media (max-width: 768px) {
  .message-bubble {
    max-width: 85%;
  }
  
  .chatbox-input-container {
    flex-wrap: wrap;
  }
}

@media (max-width: 480px) {
  .message-bubble {
    max-width: 95%;
  }
  
  .chatbox-header {
    flex-direction: column;
  }
}
```

---

## ♿ Accessibility Features

### ARIA Labels

```jsx
<div role="region" aria-label="Chat messages" aria-live="polite">
  {messages.map(msg => (
    <div role="article" aria-label={`${msg.role}: ${msg.content}`}>
      {msg.content}
    </div>
  ))}
</div>
```

### Focus Management

```css
.action-button:focus-visible {
  outline: 2px solid var(--color-secondary);
  outline-offset: 2px;
}

.chatbox-input:focus-visible {
  outline: 2px solid var(--color-primary);
}
```

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 📊 Performance Tips

### Optimization Techniques

1. **Memoization**
```jsx
const Message = React.memo(({ message, theme }) => (
  // Component
), (prev, next) => prev.message.id === next.message.id);
```

2. **Lazy Loading**
```jsx
const ChatboxDesign = React.lazy(() => import('./ChatboxDesign'));
```

3. **Virtual Scrolling**
```jsx
<FixedSizeList height={600} itemCount={1000} itemSize={100}>
  {Row}
</FixedSizeList>
```

4. **Code Splitting**
```jsx
const ThemeSelector = lazy(() => import('./ThemeSelector'));
```

---

## 🧪 Testing Examples

### Unit Tests

```typescript
describe('ChatboxDesign', () => {
  it('renders messages', () => {
    const { getByText } = render(
      <ChatboxDesign initialSession={{ messages: [...] }} />
    );
    expect(getByText('Hello')).toBeInTheDocument();
  });

  it('sends messages on Enter', async () => {
    const onSend = jest.fn();
    const { getByRole } = render(
      <ChatboxDesign onMessageSent={onSend} />
    );
    const input = getByRole('textbox');
    fireEvent.change(input, { target: { value: 'Hello' } });
    fireEvent.keyPress(input, { key: 'Enter' });
    expect(onSend).toHaveBeenCalled();
  });
});
```

---

## 🚀 Quick Reference

| Task | Code |
|------|------|
| Create chatbox | `<ChatboxDesign theme="cyberpunk" />` |
| Send message | `await sendMessage('Hello')` |
| Switch theme | `applyTheme('matrix')` |
| Create custom theme | `createCustomTheme('my', { primary: '#F00' })` |
| Clear chat | `clearConversation()` |
| Export chat | `exportConversation('json')` |
| Delete message | `deleteMessage(id)` |
| Edit message | `editMessage(id, newContent)` |

---

**End of Component Reference** 📖
