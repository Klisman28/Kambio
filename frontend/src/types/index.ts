// Tipos globales del sistema Kambio

export type UserRole = 'admin' | 'operator' | 'viewer'

export interface User {
  id: string
  email: string
  full_name: string
  role: UserRole
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export interface LoginRequest {
  email: string
  password: string
}

// Placeholder — extender en Fase 1
export interface Client {
  id: string
  full_name: string
  phone?: string
  email?: string
  notes?: string
  is_active: boolean
  created_at: string
  updated_at: string
}

// Placeholder — extender en Fase 1
export interface Transaction {
  id: string
  client_id: string
  user_id: string
  type: 'ENTRADA' | 'SALIDA'
  monto_mxn?: number
  monto_gtq?: number
  comision: number
  tipo_cambio_pactado?: number
  status: 'ACTIVA' | 'ANULADA'
  notes?: string
  created_at: string
}
