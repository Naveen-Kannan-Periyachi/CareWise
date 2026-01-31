import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Heart, Menu, Plus, MessageSquare, LogOut, Send, 
  ChevronLeft, ChevronRight, Trash2, User 
} from 'lucide-react';
import axios from 'axios';
import AIInput from '../components/AIInput';
import ProcessingSteps from '../components/ProcessingSteps';
import './Dashboard.css';

// Expandable Source Card Component
const ExpandableSourceCard = ({ evidence, rank }) => {
  const [expanded, setExpanded] = useState(false);

  const getSourceColor = (source) => {
    const colors = {
      'PubMed': '#3b82f6',
      'ClinicalTrials': '#10b981',
      'FDA': '#f59e0b',
      'MedlinePlus': '#8b5cf6',
      'CDC': '#ec4899',
      'WHO': '#06b6d4'
    };
    return colors[source] || '#6b7280';
  };

  return (
    <div 
      className={`expandable-source-card ${expanded ? 'expanded' : ''}`}
      onMouseEnter={() => setExpanded(true)}
      onMouseLeave={() => setExpanded(false)}
    >
      <div className="expandable-card-header">
        <span className="expandable-rank">#{rank}</span>
        <span 
          className="expandable-source-name"
          style={{ color: getSourceColor(evidence.source) }}
        >
          {evidence.source}
        </span>
        {evidence.score && (
          <span className="expandable-score">{(evidence.score * 100).toFixed(0)}%</span>
        )}
      </div>
      <div className="expandable-card-title">{evidence.title}</div>
      {expanded && evidence.content && (
        <div className="expandable-card-content">
          {evidence.content}
        </div>
      )}
      {expanded && evidence.metadata?.year && (
        <div className="expandable-card-meta">
          Published: {evidence.metadata.year}
        </div>
      )}
    </div>
  );
};

const Dashboard = ({ setIsAuthenticated }) => {
  const navigate = useNavigate();
  const [sidebarPinned, setSidebarPinned] = useState(false);
  const [sidebarHovered, setSidebarHovered] = useState(false);
  const sidebarExpanded = sidebarPinned || sidebarHovered;
  const [chats, setChats] = useState([]);
  const [currentChatId, setCurrentChatId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [currentStatus, setCurrentStatus] = useState('analyzing');
  const [user, setUser] = useState(null);

  useEffect(() => {
    const userData = JSON.parse(localStorage.getItem('carewise_user'));
    if (userData) {
      setUser(userData);
      loadChats(userData.email);
    } else {
      // No user logged in, redirect to login
      navigate('/login');
    }
  }, [navigate]);

  const loadChats = (email) => {
    const savedChats = JSON.parse(localStorage.getItem(`carewise_chats_${email}`) || '[]');
    setChats(savedChats);
    
    if (savedChats.length === 0) {
      // Create initial chat when user data is available
      const newChat = {
        id: Date.now().toString(),
        name: 'New Chat',
        createdAt: new Date().toISOString(),
        messages: []
      };
      const initialChats = [newChat];
      localStorage.setItem(`carewise_chats_${email}`, JSON.stringify(initialChats));
      setChats(initialChats);
      setCurrentChatId(newChat.id);
      setMessages([]);
    } else {
      setCurrentChatId(savedChats[0].id);
      setMessages(savedChats[0].messages || []);
    }
  };

  const saveChats = (updatedChats) => {
    if (user && user.email) {
      localStorage.setItem(`carewise_chats_${user.email}`, JSON.stringify(updatedChats));
      setChats(updatedChats);
    }
  };

  const createNewChat = () => {
    if (!user || !user.email) return;
    
    const newChat = {
      id: Date.now().toString(),
      name: 'New Chat',
      createdAt: new Date().toISOString(),
      messages: []
    };
    const updatedChats = [newChat, ...chats];
    saveChats(updatedChats);
    setCurrentChatId(newChat.id);
    setMessages([]);
  };

  const selectChat = (chatId) => {
    setCurrentChatId(chatId);
    const chat = chats.find(c => c.id === chatId);
    setMessages(chat?.messages || []);
  };

  const deleteChat = (chatId) => {
    const updatedChats = chats.filter(c => c.id !== chatId);
    saveChats(updatedChats);
    
    if (chatId === currentChatId) {
      if (updatedChats.length > 0) {
        selectChat(updatedChats[0].id);
      } else {
        createNewChat();
      }
    }
  };

  const updateChatName = (chatId, firstMessage) => {
    const updatedChats = chats.map(chat => {
      if (chat.id === chatId && chat.name === 'New Chat') {
        return {
          ...chat,
          name: firstMessage.substring(0, 30) + (firstMessage.length > 30 ? '...' : '')
        };
      }
      return chat;
    });
    saveChats(updatedChats);
  };

  const handleSendMessage = async (message = inputMessage) => {
    if (!message.trim() || loading) return;

    const userMessage = {
      type: 'user',
      content: message,
      timestamp: new Date().toISOString()
    };

    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInputMessage('');
    setLoading(true);
    setCurrentStatus('analyzing');

    // Update chat name if first message
    if (messages.length === 0) {
      updateChatName(currentChatId, message);
    }

    try {
      // Use EventSource for real-time status updates
      const eventSource = new EventSource(
        `http://localhost:8000/query-stream?query=${encodeURIComponent(message)}`
      );

      eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log('Received status:', data);
        
        if (data.status === 'analyzing') {
          setCurrentStatus('analyzing');
        } else if (data.status === 'plan_complete') {
          setCurrentStatus('selecting_sources');
        } else if (data.status === 'selecting_sources') {
          setCurrentStatus('selecting_sources');
        } else if (data.status === 'searching') {
          setCurrentStatus('searching');
        } else if (data.status === 'generating') {
          setCurrentStatus('generating');
        } else if (data.status === 'complete') {
          // Close the connection
          eventSource.close();
          setLoading(false);

          const botMessage = {
            type: 'bot',
            content: data.data.answer.answer,
            plan: data.data.plan,
            evidence: data.data.top_sources,
            timestamp: new Date().toISOString()
          };

          const updatedMessages = [...newMessages, botMessage];
          setMessages(updatedMessages);

          // Save to chat history
          const updatedChats = chats.map(chat => {
            if (chat.id === currentChatId) {
              return { ...chat, messages: updatedMessages };
            }
            return chat;
          });
          saveChats(updatedChats);
        } else if (data.status === 'error') {
          eventSource.close();
          setLoading(false);
          
          const errorMessage = {
            type: 'error',
            content: `Error: ${data.message}`,
            timestamp: new Date().toISOString()
          };
          setMessages([...newMessages, errorMessage]);
        }
      };

      eventSource.onerror = (error) => {
        console.error('EventSource error:', error);
        eventSource.close();
        setLoading(false);
        
        const errorMessage = {
          type: 'error',
          content: 'Sorry, I encountered an error. Please make sure the backend server is running.',
          timestamp: new Date().toISOString()
        };
        setMessages([...newMessages, errorMessage]);
      };

    } catch (error) {
      console.error('Error:', error);
      setLoading(false);
      
      const errorMessage = {
        type: 'error',
        content: 'Sorry, I encountered an error. Please make sure the backend server is running.',
        timestamp: new Date().toISOString()
      };
      setMessages([...newMessages, errorMessage]);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('carewise_user');
    setIsAuthenticated(false);
    navigate('/');
  };

  return (
    <div className="dashboard">
      {/* Sidebar */}
      <div 
        className={`sidebar ${sidebarExpanded || sidebarHovered ? 'expanded' : 'collapsed'}`}
        onMouseEnter={() => setSidebarHovered(true)}
        onMouseLeave={() => setSidebarHovered(false)}
      >
        <div className="sidebar-header">
          <div className="sidebar-logo">
            <Heart className="logo-icon" />
            {sidebarExpanded && <span>CareWise</span>}
          </div>
          {sidebarHovered && (
            <button 
              className="sidebar-toggle"
              onClick={() => setSidebarPinned(!sidebarPinned)}
            >
              {sidebarPinned ? <ChevronLeft size={20} /> : <ChevronRight size={20} />}
            </button>
          )}
        </div>

        <button className="new-chat-btn" onClick={createNewChat}>
          <Plus size={20} />
          {(sidebarExpanded || sidebarHovered) && <span>New Chat</span>}
        </button>

        <div className="chat-history">
          {(sidebarExpanded || sidebarHovered) && <div className="history-label">History</div>}
          <div className="chat-list">
            {chats.map(chat => (
              <div
                key={chat.id}
                className={`chat-item ${chat.id === currentChatId ? 'active' : ''}`}
                onClick={() => selectChat(chat.id)}
              >
                <MessageSquare size={18} />
                {(sidebarExpanded || sidebarHovered) && (
                  <>
                    <span className="chat-name">{chat.name}</span>
                    <button
                      className="delete-chat-btn"
                      onClick={(e) => {
                        e.stopPropagation();
                        deleteChat(chat.id);
                      }}
                    >
                      <Trash2 size={16} />
                    </button>
                  </>
                )}
              </div>
            ))}
          </div>
        </div>

        <div className="sidebar-footer">
          <div className="user-info">
            <User size={20} />
            {sidebarExpanded && (
              <div className="user-details">
                <div className="user-name">{user?.name}</div>
                <div className="user-email">{user?.email}</div>
              </div>
            )}
          </div>
          <button className="logout-btn" onClick={handleLogout}>
            <LogOut size={20} />
            {sidebarExpanded && <span>Logout</span>}
          </button>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="main-chat">
        <div className="chat-header">
          <button 
            className="mobile-menu-btn"
            onClick={() => setSidebarPinned(!sidebarPinned)}
          >
            <Menu size={24} />
          </button>
          <h2>{chats.find(c => c.id === currentChatId)?.name || 'New Chat'}</h2>
        </div>

        <div className="chat-messages">
          {messages.length === 0 ? (
            <div className="empty-state">
              <Heart size={64} className="empty-icon" />
              <h3>Start a New Conversation</h3>
              <p>Ask me anything about health, diseases, treatments, or medical research</p>
              <div className="example-queries">
                <button onClick={() => handleSendMessage("What are the symptoms of diabetes?")}>
                  What are the symptoms of diabetes?
                </button>
                <button onClick={() => handleSendMessage("Any ongoing trials for cancer?")}>
                  Any ongoing trials for cancer?
                </button>
                <button onClick={() => handleSendMessage("Side effects of aspirin")}>
                  Side effects of aspirin
                </button>
              </div>
            </div>
          ) : (
            messages.map((msg, index) => (
              <div key={index} className={`message ${msg.type}`}>
                <div className="message-avatar">
                  {msg.type === 'user' ? <User size={20} /> : <Heart size={20} />}
                </div>
                <div className="message-content">
                  {/* AI Generated Answer */}
                  <div className="message-text">{msg.content}</div>
                  
                  {/* Plan/Intent Meta Info */}
                  {msg.plan && (
                    <div className="message-meta">
                      <span className="meta-badge">Intent: {msg.plan.intent}</span>
                      <span className="meta-badge">Sources: {msg.plan.sources.join(', ')}</span>
                    </div>
                  )}
                  
                  {/* Evidence Sources */}
                  {msg.evidence && msg.evidence.length > 0 && (
                    <div className="evidence-container">
                      {/* Top Ranked Evidence - Full Display */}
                      <div className="top-evidence">
                        <div className="top-evidence-header">
                          <span className="rank-badge-top">#1 Top Source</span>
                          <span className="source-badge-top">{msg.evidence[0].source}</span>
                          {msg.evidence[0].score && (
                            <span className="score-badge-top">
                              {(msg.evidence[0].score * 100).toFixed(0)}% Match
                            </span>
                          )}
                        </div>
                        <h4 className="top-evidence-title">{msg.evidence[0].title}</h4>
                        <p className="top-evidence-content">
                          {msg.evidence[0].content}
                        </p>
                      </div>

                      {/* Remaining Sources - Expandable List */}
                      {msg.evidence.length > 1 && (
                        <div className="remaining-sources">
                          <div className="remaining-sources-label">Other Relevant Sources:</div>
                          <div className="remaining-sources-list">
                            {msg.evidence.slice(1).map((ev, idx) => (
                              <ExpandableSourceCard
                                key={idx}
                                evidence={ev}
                                rank={idx + 2}
                              />
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
          {loading && (
            <div className="message bot">
              <div className="message-avatar">
                <Heart size={20} />
              </div>
              <div className="message-content">
                <ProcessingSteps currentStatus={currentStatus} />
              </div>
            </div>
          )}
        </div>

        <div className="chat-input-area">
          <AIInput
            placeholder="Ask about health, research, or medical information..."
            onSubmit={handleSendMessage}
            disabled={loading}
            loadingDuration={2000}
          />
          <div className="input-hint">
            Powered by CareWise AI • 6 Medical Sources
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
