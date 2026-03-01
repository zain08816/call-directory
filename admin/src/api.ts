import type { Contact, CallRecord, MessageRecord, TestCallResponse, TestSmsResponse } from './types'

async function request<T>(baseUrl: string, url: string, options?: RequestInit): Promise<T> {
  const base = baseUrl.replace(/\/$/, '')
  const res = await fetch(base + url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  })
  const isJson = res.headers.get('content-type')?.includes('application/json')
  const data = isJson ? await res.json() : {}
  if (!res.ok) {
    const msg = typeof data.detail === 'string' ? data.detail : data.detail?.message ?? `${res.status} ${res.statusText}`
    throw new Error(msg)
  }
  return data as T
}

export function createApi(baseUrl: string) {
  return {
    getContacts: () => request<Contact[]>(baseUrl, '/api/contacts'),
    getCalls: (limit = 50) => request<CallRecord[]>(baseUrl, '/api/calls?limit=' + limit),
    getMessages: (limit = 50) => request<MessageRecord[]>(baseUrl, '/api/messages?limit=' + limit),
    testCall: (to: string) =>
      request<TestCallResponse>(baseUrl, '/api/test/call', { method: 'POST', body: JSON.stringify({ to }) }),
    testSms: (to: string, body: string) =>
      request<TestSmsResponse>(baseUrl, '/api/test/sms', { method: 'POST', body: JSON.stringify({ to, body }) }),
  }
}

export type Api = ReturnType<typeof createApi>
