import { useState, useEffect, useCallback } from 'react'
import { createApi } from './api'
import type { Contact, CallRecord, MessageRecord } from './types'

function formatDate(iso: string | null): string {
  if (!iso) return ''
  try {
    return new Date(iso).toLocaleString()
  } catch {
    return iso
  }
}

function Card({
  title,
  hint,
  children,
}: { title: string; hint: string; children: React.ReactNode }) {
  return (
    <section className="rounded-lg border border-[#2d3a4d] bg-[#1a2332] p-5">
      <h2 className="text-lg font-semibold">{title}</h2>
      <p className="mb-4 text-sm text-[#8b949e]">{hint}</p>
      {children}
    </section>
  )
}

function ContactsSection({ apiBase }: { apiBase: string }) {
  const [contacts, setContacts] = useState<Contact[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(() => {
    setLoading(true)
    setError(null)
    createApi(apiBase)
      .getContacts()
      .then(setContacts)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [apiBase])

  useEffect(() => {
    load()
  }, [load])

  if (loading) return <p className="mb-3 text-sm">Loading…</p>
  if (error) return <p className="mb-3 text-sm text-[#f85149]">{error}</p>
  return (
    <>
      <table className="mb-3 w-full table-auto border-collapse text-sm">
        <thead>
          <tr className="text-left text-xs uppercase tracking-wider text-[#8b949e]">
            <th className="border-b border-[#2d3a4d] px-3 py-2">#</th>
            <th className="border-b border-[#2d3a4d] px-3 py-2">Name</th>
            <th className="border-b border-[#2d3a4d] px-3 py-2">Phone</th>
          </tr>
        </thead>
        <tbody>
          {contacts.map((c) => (
            <tr key={c.id} className="border-b border-[#2d3a4d]">
              <td className="px-3 py-2">{c.id}</td>
              <td className="px-3 py-2">{c.name}</td>
              <td className="px-3 py-2">{c.phone}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <button
        type="button"
        onClick={load}
        className="rounded border border-[#2d3a4d] bg-transparent px-4 py-2 text-sm font-medium text-[#8b949e] hover:border-[#8b949e] hover:text-[#e6edf3]"
      >
        Refresh
      </button>
    </>
  )
}

function CallsSection({ apiBase }: { apiBase: string }) {
  const [calls, setCalls] = useState<CallRecord[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(() => {
    setLoading(true)
    setError(null)
    createApi(apiBase)
      .getCalls()
      .then(setCalls)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [apiBase])

  useEffect(() => {
    load()
  }, [load])

  if (loading) return <p className="mb-3 text-sm">Loading…</p>
  if (error) return <p className="mb-3 text-sm text-[#f85149]">{error}</p>
  return (
    <>
      <table className="mb-3 w-full table-auto border-collapse text-sm">
        <thead>
          <tr className="text-left text-xs uppercase tracking-wider text-[#8b949e]">
            <th className="border-b border-[#2d3a4d] px-3 py-2">From</th>
            <th className="border-b border-[#2d3a4d] px-3 py-2">To</th>
            <th className="border-b border-[#2d3a4d] px-3 py-2">Status</th>
            <th className="border-b border-[#2d3a4d] px-3 py-2">Direction</th>
            <th className="border-b border-[#2d3a4d] px-3 py-2">Date</th>
          </tr>
        </thead>
        <tbody>
          {calls.map((c) => (
            <tr key={c.sid} className="border-b border-[#2d3a4d]">
              <td className="px-3 py-2">{c.from}</td>
              <td className="px-3 py-2">{c.to}</td>
              <td className="px-3 py-2">{c.status}</td>
              <td className="px-3 py-2">{c.direction}</td>
              <td className="px-3 py-2">{formatDate(c.date_created)}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <button
        type="button"
        onClick={load}
        className="rounded border border-[#2d3a4d] bg-transparent px-4 py-2 text-sm font-medium text-[#8b949e] hover:border-[#8b949e] hover:text-[#e6edf3]"
      >
        Refresh
      </button>
    </>
  )
}

function MessagesSection({ apiBase }: { apiBase: string }) {
  const [messages, setMessages] = useState<MessageRecord[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(() => {
    setLoading(true)
    setError(null)
    createApi(apiBase)
      .getMessages()
      .then(setMessages)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [apiBase])

  useEffect(() => {
    load()
  }, [load])

  if (loading) return <p className="mb-3 text-sm">Loading…</p>
  if (error) return <p className="mb-3 text-sm text-[#f85149]">{error}</p>
  return (
    <>
      <table className="mb-3 w-full table-auto border-collapse text-sm">
        <thead>
          <tr className="text-left text-xs uppercase tracking-wider text-[#8b949e]">
            <th className="border-b border-[#2d3a4d] px-3 py-2">From</th>
            <th className="border-b border-[#2d3a4d] px-3 py-2">To</th>
            <th className="max-w-[200px] border-b border-[#2d3a4d] px-3 py-2">Body</th>
            <th className="border-b border-[#2d3a4d] px-3 py-2">Status</th>
            <th className="border-b border-[#2d3a4d] px-3 py-2">Date</th>
          </tr>
        </thead>
        <tbody>
          {messages.map((m) => (
            <tr key={m.sid} className="border-b border-[#2d3a4d]">
              <td className="px-3 py-2">{m.from}</td>
              <td className="px-3 py-2">{m.to}</td>
              <td className="max-w-[200px] truncate px-3 py-2">{(m.body || '').slice(0, 80)}{(m.body || '').length > 80 ? '…' : ''}</td>
              <td className="px-3 py-2">{m.status}</td>
              <td className="px-3 py-2">{formatDate(m.date_created)}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <button
        type="button"
        onClick={load}
        className="rounded border border-[#2d3a4d] bg-transparent px-4 py-2 text-sm font-medium text-[#8b949e] hover:border-[#8b949e] hover:text-[#e6edf3]"
      >
        Refresh
      </button>
    </>
  )
}

function TestCallSection({ apiBase, onSuccess }: { apiBase: string; onSuccess: () => void }) {
  const [to, setTo] = useState('')
  const [status, setStatus] = useState<'idle' | 'loading' | 'ok' | 'err'>('idle')
  const [message, setMessage] = useState('')

  const submit = () => {
    const num = to.trim()
    if (!num) {
      setMessage('Enter a phone number (e.g. +15551234567).')
      setStatus('err')
      return
    }
    setStatus('loading')
    setMessage('')
    createApi(apiBase)
      .testCall(num)
      .then((r) => {
        setMessage('Call started. SID: ' + (r.sid || ''))
        setStatus('ok')
        onSuccess()
      })
      .catch((e) => {
        setMessage('Error: ' + e.message)
        setStatus('err')
      })
  }

  return (
    <div className="space-y-2">
      <div className="flex flex-wrap items-center gap-3">
        <input
          type="tel"
          value={to}
          onChange={(e) => setTo(e.target.value)}
          placeholder="+15551234567"
          className="rounded border border-[#2d3a4d] bg-[#0f1419] px-3 py-2 text-sm text-[#e6edf3] placeholder:text-[#8b949e]"
        />
        <button
          type="button"
          onClick={submit}
          disabled={status === 'loading'}
          className="rounded bg-[#58a6ff] px-4 py-2 text-sm font-medium text-[#0f1419] hover:bg-[#79b8ff] disabled:opacity-50"
        >
          {status === 'loading' ? 'Placing…' : 'Place test call'}
        </button>
      </div>
      {message && (
        <p className={`text-sm ${status === 'ok' ? 'text-[#3fb950]' : status === 'err' ? 'text-[#f85149]' : ''}`}>
          {message}
        </p>
      )}
    </div>
  )
}

function TestSmsSection({ apiBase, onSuccess }: { apiBase: string; onSuccess: () => void }) {
  const [to, setTo] = useState('')
  const [body, setBody] = useState('Test message from admin dashboard')
  const [status, setStatus] = useState<'idle' | 'loading' | 'ok' | 'err'>('idle')
  const [message, setMessage] = useState('')

  const submit = () => {
    const num = to.trim()
    if (!num) {
      setMessage('Enter a phone number.')
      setStatus('err')
      return
    }
    setStatus('loading')
    setMessage('')
    createApi(apiBase)
      .testSms(num, body.trim() || 'Test message from admin dashboard')
      .then(() => {
        setMessage('SMS sent to ' + num)
        setStatus('ok')
        onSuccess()
      })
      .catch((e) => {
        setMessage('Error: ' + e.message)
        setStatus('err')
      })
  }

  return (
    <div className="flex max-w-md flex-col gap-2">
      <input
        type="tel"
        value={to}
        onChange={(e) => setTo(e.target.value)}
        placeholder="To: +15551234567"
        className="rounded border border-[#2d3a4d] bg-[#0f1419] px-3 py-2 text-sm text-[#e6edf3] placeholder:text-[#8b949e]"
      />
      <textarea
        value={body}
        onChange={(e) => setBody(e.target.value)}
        rows={2}
        placeholder="Message body"
        className="min-h-[60px] resize-y rounded border border-[#2d3a4d] bg-[#0f1419] px-3 py-2 text-sm text-[#e6edf3] placeholder:text-[#8b949e]"
      />
      <button
        type="button"
        onClick={submit}
        disabled={status === 'loading'}
        className="rounded bg-[#58a6ff] px-4 py-2 text-sm font-medium text-[#0f1419] hover:bg-[#79b8ff] disabled:opacity-50"
      >
        {status === 'loading' ? 'Sending…' : 'Send test SMS'}
      </button>
      {message && (
        <p className={`text-sm ${status === 'ok' ? 'text-[#3fb950]' : status === 'err' ? 'text-[#f85149]' : ''}`}>
          {message}
        </p>
      )}
    </div>
  )
}

export default function App() {
  const [apiBaseInput, setApiBaseInput] = useState('')
  const apiBase = apiBaseInput.trim().replace(/\/$/, '') || window.location.origin
  const [callsRefresh, setCallsRefresh] = useState(0)
  const [messagesRefresh, setMessagesRefresh] = useState(0)

  return (
    <div className="mx-auto max-w-4xl p-6">
      <header className="border-b border-[#2d3a4d] pb-6">
        <h1 className="text-xl font-semibold">Call/SMS Directory</h1>
        <p className="text-sm text-[#8b949e]">Admin Dashboard</p>
        <div className="mt-4">
          <label className="block text-xs uppercase tracking-wider text-[#8b949e]">API base URL</label>
          <input
            type="text"
            value={apiBaseInput}
            onChange={(e) => setApiBaseInput(e.target.value)}
            placeholder="Optional — leave empty to use current origin"
            className="mt-1 min-w-0 w-full max-w-xl rounded border border-[#2d3a4d] bg-[#1a2332] px-3 py-2 text-sm text-[#e6edf3] placeholder:text-[#8b949e]"
            title="Override the API base URL. Leave empty to use this page's origin (e.g. http://127.0.0.1:8000 or http://127.0.0.1:5173)."
          />
          <p className="mt-1 text-xs text-[#8b949e]">Leave empty to use this page&apos;s origin for API requests.</p>
        </div>
      </header>

      <main className="mt-6 flex flex-col gap-6">
        <Card title="Contacts" hint="Phone numbers in the directory menu.">
          <ContactsSection apiBase={apiBase} />
        </Card>
        <Card title="Recent Calls" hint="Calls sent/received via Twilio.">
          <CallsSection key={callsRefresh} apiBase={apiBase} />
        </Card>
        <Card title="Recent SMS" hint="Messages sent and to where.">
          <MessagesSection key={messagesRefresh} apiBase={apiBase} />
        </Card>
        <Card title="Test Call" hint="Start a call to a number; when they answer they hear the directory menu.">
          <TestCallSection apiBase={apiBase} onSuccess={() => setCallsRefresh((n) => n + 1)} />
        </Card>
        <Card title="Test SMS" hint="Send a test message from the Twilio number.">
          <TestSmsSection apiBase={apiBase} onSuccess={() => setMessagesRefresh((n) => n + 1)} />
        </Card>
      </main>
    </div>
  )
}
