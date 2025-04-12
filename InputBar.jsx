import React, { useState } from 'react'
export default function InputBar({ onSend }) {
  const [input, setInput] = useState('')

  const handleSubmit = () => {
    if (input.trim()) {
      onSend(input)
      setInput('')
    }
  }

  return (
    <div className="p-4 bg-gray-800 flex gap-2">
      <input
        className="flex-1 p-2 rounded bg-gray-700 text-white"
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && handleSubmit()}
        placeholder="Введите сообщение..."
      />
      <button onClick={handleSubmit} className="bg-blue-600 px-4 rounded text-white hover:bg-blue-700">Отправить</button>
    </div>
  )
}