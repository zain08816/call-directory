export interface Contact {
  id: number
  name: string
  phone: string
}

export interface CallRecord {
  sid: string
  from: string
  to: string
  status: string
  direction: string
  date_created: string | null
}

export interface MessageRecord {
  sid: string
  from: string
  to: string
  body: string
  status: string
  direction: string
  date_created: string | null
}

export interface TestCallResponse {
  sid: string
  from: string
  to: string
  status: string
}

export interface TestSmsResponse {
  ok: boolean
  to: string
}
