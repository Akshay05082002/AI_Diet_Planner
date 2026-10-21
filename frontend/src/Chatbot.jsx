import React, { useState, useEffect, useRef } from 'react'
import axios from 'axios'

export default function Chatbot() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [exporting, setExporting] = useState(false)
  const messagesEndRef = useRef(null)

  // Fetch chat history on mount
  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await axios.get('http://localhost:5001/api/chat-history', { withCredentials: true })
        setMessages(res.data.messages || [])
      } catch (err) {
        console.error('Failed to load chat history:', err)
      }
    }
    fetchHistory()
  }, [])

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async (e) => {
    e.preventDefault()
    if (!input.trim()) return

    setLoading(true)
    try {
      const res = await axios.post('http://localhost:5001/api/chat', { message: input }, { withCredentials: true })
      setMessages([...messages, { user: input, ai: res.data.ai, timestamp: res.data.timestamp }])
      setInput('')
    } catch (err) {
      console.error('Chat error:', err)
      alert('Failed to send message')
    } finally {
      setLoading(false)
    }
  }

  const exportPDF = async () => {
    setExporting(true)
    try {
      const res = await axios.post('http://localhost:5001/api/export-pdf', {}, { 
        withCredentials: true,
        responseType: 'blob'
      })
      // Create blob URL and trigger download
      const url = window.URL.createObjectURL(new Blob([res.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'diet-planner-report.pdf')
      document.body.appendChild(link)
      link.click()
      link.parentNode.removeChild(link)
      window.URL.revokeObjectURL(url)
    } catch (err) {
      console.error('PDF export error:', err)
      alert('PDF export failed. Make sure reportlab is installed: pip install reportlab')
    } finally {
      setExporting(false)
    }
  }

  const clearChat = async () => {
    if (!window.confirm('Clear all chat messages?')) return
    try {
      await axios.post('http://localhost:5001/api/clear-chat', {}, { withCredentials: true })
      setMessages([])
    } catch (err) {
      console.error('Clear chat error:', err)
    }
  }

  return (
    <div style={{maxWidth:800, margin:'20px auto', fontFamily:'Segoe UI, Tahoma, Geneva, sans-serif'}}>
      <div style={{background:'linear-gradient(135deg, #667eea, #764ba2)', color:'white', padding:'20px', borderRadius:'12px', marginBottom:20}}>
        <h2 style={{margin:'0 0 10px 0'}}>🤖 AI Nutrition Coach</h2>
        <p style={{margin:'0', fontSize:'0.9rem', opacity:0.9}}>Ask me for diet tips, calorie advice, meal planning, fitness tips, and more!</p>
      </div>

      {/* Chat messages */}
      <div style={{
        border:'1px solid #ddd',
        borderRadius:'12px',
        height:'400px',
        overflowY:'auto',
        padding:'15px',
        marginBottom:'15px',
        background:'#f9f9f9'
      }}>
        {messages.length === 0 && (
          <p style={{textAlign:'center', color:'#999', paddingTop:'100px'}}>Start a conversation with the AI coach! 💪</p>
        )}
        {messages.map((msg, idx) => (
          <div key={idx} style={{marginBottom:'15px'}}>
            <div style={{textAlign:'right', marginBottom:'5px'}}>
              <span style={{background:'#667eea', color:'white', padding:'8px 12px', borderRadius:'8px', display:'inline-block', maxWidth:'70%', wordWrap:'break-word'}}>
                {msg.user}
              </span>
            </div>
            <div style={{textAlign:'left', marginBottom:'10px'}}>
              <span style={{background:'#e8e8e8', color:'#333', padding:'8px 12px', borderRadius:'8px', display:'inline-block', maxWidth:'70%', wordWrap:'break-word'}}>
                {msg.ai}
              </span>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <form onSubmit={sendMessage} style={{display:'flex', gap:'10px', marginBottom:'15px'}}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask me anything about diet, calories, fitness..."
          disabled={loading}
          style={{
            flex:1,
            padding:'10px 12px',
            border:'2px solid #667eea',
            borderRadius:'8px',
            fontSize:'0.95rem',
            outline:'none'
          }}
        />
        <button type="submit" disabled={loading} style={{
          background:'#667eea',
          color:'white',
          border:'none',
          padding:'10px 20px',
          borderRadius:'8px',
          cursor:'pointer',
          fontWeight:'600',
          opacity: loading ? 0.6 : 1
        }}>
          {loading ? '...' : 'Send'}
        </button>
      </form>

      {/* Actions */}
      <div style={{display:'flex', gap:'10px'}}>
        <button onClick={exportPDF} disabled={exporting} style={{
          flex:1,
          background:'#764ba2',
          color:'white',
          border:'none',
          padding:'10px 15px',
          borderRadius:'8px',
          cursor:'pointer',
          fontWeight:'600',
          opacity: exporting ? 0.6 : 1
        }}>
          📥 {exporting ? 'Generating...' : 'Export to PDF'}
        </button>
        <button onClick={clearChat} style={{
          flex:1,
          background:'#ef5350',
          color:'white',
          border:'none',
          padding:'10px 15px',
          borderRadius:'8px',
          cursor:'pointer',
          fontWeight:'600'
        }}>
          🗑️ Clear Chat
        </button>
      </div>
    </div>
  )
}
