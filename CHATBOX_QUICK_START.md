# 🚀 Chatbox Quick Start Integration Guide

**Status**: Ready for Production  
**Last Updated**: 2024  
**Time to Integration**: ~30 minutes  

---

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies

```bash
npm install styled-components react-window react-dom
npm install --save-dev @types/styled-components @types/react-window
```

### Step 2: Copy Files to Your Project

```bash
# Copy component files
cp frontend/src/components/ChatboxDesign.jsx your-project/src/components/
cp frontend/src/hooks/useChat.ts your-project/src/hooks/
cp frontend/src/types/chatbox.ts your-project/src/types/

# Copy styling
cp frontend/styles/chatbox.css your-project/src/styles/
```

### Step 3: Add to Your React App

```jsx
import React from 'react';
import ChatboxDesign from './components/ChatboxDesign';
import './styles/chatbox.css';

function App() {
  return (
    <ChatboxDesign
      theme="cyberpunk"
      apiEndpoint="/api/chat"
      enableWebSocket={true}
    />
  );
}

export default App;
```

### Step 4: Run Your App

```bash
npm start
```

**✅ Chatbox is live!**

---

## 📦 File Structure

```
your-project/
├── src/
│   ├── components/
│   │   ├── ChatboxDesign.jsx
│   │   └── ...
│   ├── hooks/
│   │   └── useChat.ts
│   ├── types/
│   │   └── chatbox.ts
│   ├── styles/
│   │   └── chatbox.css
│   ├── App.jsx
│   └── index.jsx
├── public/
└── package.json
```

---

## 🔌 Backend API Setup

### Required Endpoints

Your backend needs to implement these REST API endpoints:

#### 1. Session Management

```http
POST /api/chat/session
Content-Type: application/json

{
  "context": {
    "user_id": "user123",
    "features": ["streaming", "thinking"]
  }
}

Response:
{
  "session_id": "sess_abc123",
  "created_at": "2024-01-01T12:00:00Z"
}
```

#### 2. Send Message (Streaming)

```http
POST /api/chat/message/stream
Content-Type: application/json

{
  "message": "Hello, how are you?",
  "session_id": "sess_abc123"
}

Response: Server-Sent Events
data: {"type": "content", "content": "I'm doing well, thank you"}
data: {"type": "thinking", "thinking": "User greeted me..."}
data: {"type": "metadata", "confidence_score": 0.95}
```

#### 3. Regular Message (Non-Streaming)

```http
POST /api/chat/message
Content-Type: application/json

{
  "message": "Hello, how are you?",
  "session_id": "sess_abc123"
}

Response:
{
  "id": "msg_xyz",
  "content": "I'm doing well, thank you",
  "confidence_score": 0.95,
  "thinking_process": "User greeted me..."
}
```

#### 4. Delete Message

```http
DELETE /api/chat/message/{message_id}

Response:
{
  "success": true,
  "deleted_id": "msg_xyz"
}
```

#### 5. Update Message

```http
PUT /api/chat/message/{message_id}
Content-Type: application/json

{
  "content": "Updated message"
}

Response:
{
  "id": "msg_xyz",
  "content": "Updated message"
}
```

### Python FastAPI Example

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import json

app = FastAPI()

@app.post("/api/chat/session")
async def create_session(request: dict):
    return {
        "session_id": "sess_abc123",
        "created_at": datetime.now().isoformat()
    }

@app.post("/api/chat/message/stream")
async def send_message_stream(request: dict):
    message = request.get("message")
    
    async def generate():
        # Send content chunks
        yield 'data: {"type": "content", "content": "Hello"}\n\n'
        
        # Send thinking process
        yield 'data: {"type": "thinking", "thinking": "Processing..."}\n\n'
        
        # Send metadata
        yield 'data: {"type": "metadata", "confidence_score": 0.95}\n\n'
    
    return StreamingResponse(generate(), media_type="text/event-stream")

@app.post("/api/chat/message")
async def send_message(request: dict):
    return {
        "id": "msg_xyz",
        "content": f"Response to: {request.get('message')}",
        "confidence_score": 0.95,
        "thinking_process": "Processing user message..."
    }
```

### Node.js Express Example

```javascript
const express = require('express');
const app = express();

app.post('/api/chat/session', (req, res) => {
  res.json({
    session_id: 'sess_abc123',
    created_at: new Date().toISOString()
  });
});

app.post('/api/chat/message/stream', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  
  // Send streaming data
  res.write('data: {"type": "content", "content": "Hello"}\n\n');
  res.write('data: {"type": "thinking", "thinking": "Processing..."}\n\n');
  res.write('data: {"type": "metadata", "confidence_score": 0.95}\n\n');
  
  res.end();
});

app.post('/api/chat/message', (req, res) => {
  res.json({
    id: 'msg_xyz',
    content: `Response to: ${req.body.message}`,
    confidence_score: 0.95,
    thinking_process: 'Processing user message...'
  });
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

---

## 🎨 Theme Customization

### Using Built-in Themes

```jsx
import ChatboxDesign from './components/ChatboxDesign';

function App() {
  return (
    <>
      {/* Cyberpunk */}
      <ChatboxDesign theme="cyberpunk" />
      
      {/* Matrix */}
      <ChatboxDesign theme="matrix" />
      
      {/* Ocean */}
      <ChatboxDesign theme="ocean" />
      
      {/* Midnight */}
      <ChatboxDesign theme="midnight" />
      
      {/* Sunset */}
      <ChatboxDesign theme="sunset" />
    </>
  );
}
```

### Creating Custom Themes

```jsx
import { useTheme } from './hooks/useChat';

function App() {
  const { createCustomTheme, applyTheme } = useTheme('cyberpunk');
  
  // Create custom theme
  createCustomTheme('myCustomTheme', {
    primary: '#FF00FF',
    secondary: '#00FFFF',
    accent: '#FFFF00',
    background: '#0A0A0A',
    surface: '#1A1A2E',
    text_primary: '#FFFFFF',
    text_secondary: '#B0B0B0',
    user_bubble: '#FF00FF',
    assistant_bubble: '#00FFFF',
    system_bubble: '#FFD700',
    success: '#00FF00',
    warning: '#FFA500',
    error: '#FF0000',
    border: '#FF00FF'
  });
  
  // Apply theme
  applyTheme('myCustomTheme');
  
  return <ChatboxDesign theme="myCustomTheme" />;
}
```

---

## 🪝 Using Hooks Independently

### useChat Hook

```jsx
import { useChat } from './hooks/useChat';

function MyComponent() {
  const {
    messages,
    isLoading,
    error,
    sendMessage,
    deleteMessage,
    clearConversation,
    exportConversation
  } = useChat('/api/chat');
  
  const handleSend = async () => {
    await sendMessage('Hello!');
  };
  
  const handleExport = () => {
    const json = exportConversation('json');
    console.log(json);
  };
  
  return (
    <div>
      {messages.map(msg => (
        <div key={msg.id}>
          {msg.role}: {msg.content}
          <button onClick={() => deleteMessage(msg.id)}>Delete</button>
        </div>
      ))}
      <button onClick={handleSend}>Send</button>
      <button onClick={handleExport}>Export</button>
    </div>
  );
}
```

### useTheme Hook

```jsx
import { useTheme } from './hooks/useChat';

function ThemeSwitcher() {
  const { 
    currentTheme, 
    applyTheme, 
    getAvailableThemes,
    createCustomTheme
  } = useTheme('cyberpunk');
  
  return (
    <div>
      <select value={currentTheme} onChange={(e) => applyTheme(e.target.value)}>
        {getAvailableThemes().map(theme => (
          <option key={theme} value={theme}>
            {theme.charAt(0).toUpperCase() + theme.slice(1)}
          </option>
        ))}
      </select>
      
      <button onClick={() => {
        createCustomTheme('custom', {
          primary: '#FF0000',
          secondary: '#00FF00'
        });
        applyTheme('custom');
      }}>
        Create Custom Theme
      </button>
    </div>
  );
}
```

### useWebSocket Hook

```jsx
import { useWebSocket } from './hooks/useChat';

function LiveChat() {
  const { 
    status, 
    messages, 
    send, 
    on, 
    disconnect 
  } = useWebSocket('ws://localhost:8000/chat');
  
  useEffect(() => {
    on('message', {
      onMessage: (data) => {
        console.log('Received:', data);
      },
      onConnect: () => {
        console.log('Connected');
      },
      onError: (err) => {
        console.error('Error:', err);
      }
    });
  }, [on]);
  
  return (
    <div>
      <p>Status: {status}</p>
      <button onClick={() => send({ type: 'chat', content: 'Hello' })}>
        Send
      </button>
      <button onClick={disconnect}>Disconnect</button>
    </div>
  );
}
```

---

## 🧪 Testing Setup

### Jest Configuration

```javascript
// jest.config.js
module.exports = {
  testEnvironment: 'jsdom',
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
  },
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.ts'],
  transform: {
    '^.+\\.(ts|tsx|js|jsx)$': 'babel-jest',
  }
};
```

### Example Unit Tests

```typescript
import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import ChatboxDesign from '../components/ChatboxDesign';

describe('ChatboxDesign', () => {
  it('renders chat container', () => {
    const { getByRole } = render(<ChatboxDesign />);
    expect(getByRole('textbox')).toBeInTheDocument();
  });

  it('sends message on Enter key', async () => {
    const { getByRole } = render(<ChatboxDesign />);
    const input = getByRole('textbox');
    
    fireEvent.change(input, { target: { value: 'Hello' } });
    fireEvent.keyPress(input, { key: 'Enter' });
    
    await waitFor(() => {
      expect(input.value).toBe('');
    });
  });

  it('switches themes', async () => {
    const { getByDisplayValue } = render(<ChatboxDesign theme="cyberpunk" />);
    const select = getByDisplayValue('cyberpunk');
    
    fireEvent.change(select, { target: { value: 'matrix' } });
    
    await waitFor(() => {
      expect(document.documentElement.style.getPropertyValue('--color-primary')).toBe('#00FF41');
    });
  });
});
```

---

## 🔒 Security Considerations

### CORS Configuration

```javascript
// server.js
const cors = require('cors');

app.use(cors({
  origin: 'https://yourdomain.com',
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
```

### Rate Limiting

```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});

app.post('/api/chat/message', limiter, (req, res) => {
  // Handle request
});
```

### Input Validation

```javascript
const { body, validationResult } = require('express-validator');

app.post('/api/chat/message', 
  body('message')
    .trim()
    .isLength({ min: 1, max: 5000 })
    .escape(),
  (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    // Process message
  }
);
```

---

## 📊 Performance Optimization

### Code Splitting

```jsx
import { lazy, Suspense } from 'react';

const ChatboxDesign = lazy(() => import('./components/ChatboxDesign'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <ChatboxDesign />
    </Suspense>
  );
}
```

### Lazy Image Loading

```jsx
<img src="..." loading="lazy" />
```

### Message Virtualization

```jsx
import { FixedSizeList } from 'react-window';

function MessageList({ messages }) {
  return (
    <FixedSizeList
      height={600}
      itemCount={messages.length}
      itemSize={100}
      width="100%"
    >
      {({ index, style }) => (
        <div style={style}>
          <Message message={messages[index]} />
        </div>
      )}
    </FixedSizeList>
  );
}
```

---

## 🐛 Troubleshooting

### Issue: Messages not sending

**Solution**: Check backend endpoint and CORS settings
```bash
# Verify endpoint
curl -X POST http://localhost:3000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'
```

### Issue: WebSocket not connecting

**Solution**: Verify WebSocket URL format
```javascript
// ❌ Wrong
useWebSocket('http://localhost:8000/chat');

// ✅ Correct
useWebSocket('ws://localhost:8000/chat');
```

### Issue: Theme colors not applying

**Solution**: Ensure CSS is imported
```jsx
import ChatboxDesign from './components/ChatboxDesign';
import './styles/chatbox.css'; // Must import CSS!
```

### Issue: Typing indicator not showing

**Solution**: Check `showTypingIndicator` prop
```jsx
<ChatboxDesign showTypingIndicator={true} />
```

### Issue: Messages not auto-scrolling

**Solution**: Enable `autoScroll`
```jsx
<ChatboxDesign autoScroll={true} />
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `CHATBOX_DESIGN_GUIDE.md` | Complete design system documentation |
| `CHATBOX_COMPONENT_REFERENCE.md` | Detailed component API reference |
| `CHATBOX_QUICK_START.md` | This file - quick integration guide |

---

## 🚀 Next Steps

1. ✅ Copy component files to your project
2. ✅ Install dependencies with npm
3. ✅ Implement backend API endpoints
4. ✅ Customize theme colors
5. ✅ Add authentication if needed
6. ✅ Set up analytics tracking
7. ✅ Configure CORS and security
8. ✅ Write unit tests
9. ✅ Deploy to production
10. ✅ Monitor performance and errors

---

## 💬 Support & Resources

- **Issues**: Check troubleshooting section above
- **API Reference**: See `CHATBOX_COMPONENT_REFERENCE.md`
- **Design Guide**: See `CHATBOX_DESIGN_GUIDE.md`
- **Examples**: Check `examples/AdvancedChatboxApp.tsx`

---

## 📋 Checklist for Production

- ✅ All files copied to project
- ✅ Dependencies installed
- ✅ Backend API implemented
- ✅ CORS configured
- ✅ Rate limiting enabled
- ✅ Input validation added
- ✅ Logging configured
- ✅ Error handling implemented
- ✅ Tests written and passing
- ✅ Performance optimized
- ✅ Accessibility tested
- ✅ Mobile responsiveness verified
- ✅ SSL/HTTPS enabled
- ✅ Monitoring set up
- ✅ Documentation updated

---

**Happy integrating! 🎉**
