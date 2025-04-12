import React, { useState } from 'react'
import Header from './components/Header'
import ChatWindow from './components/ChatWindow'
import InputBar from './components/InputBar'

function App() {
  const [messages, setMessages] = useState([])

  const handleSend = async (prompt) => {
    setMessages([...messages, { role: 'user', text: prompt }])
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt })
    })
    const data = await res.json()
    setMessages(prev => [...prev, { role: 'bot', text: data.response }])
  }

  return (
    <div className="flex flex-col h-screen">
      <Header />
      <ChatWindow messages={messages} />
      <InputBar onSend={handleSend} />
    </div>
  )
}

export default App