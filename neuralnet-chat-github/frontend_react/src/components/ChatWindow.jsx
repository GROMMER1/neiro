import React from 'react'
export default function ChatWindow({ messages }) {
  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-2 bg-gray-900">
      {messages.map((msg, i) => (
        <div key={i} className={msg.role === 'user' ? 'text-right' : 'text-left'}>
          <div className={\`\${msg.role === 'user' ? 'bg-blue-600' : 'bg-gray-700'} inline-block p-2 rounded-xl max-w-md\`}>
            {msg.text}
          </div>
        </div>
      ))}
    </div>
  )
}