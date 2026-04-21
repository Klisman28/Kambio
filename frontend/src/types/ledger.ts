/**
 * Tipos del contrato de Libro Mayor y Balance — Kambio
 * Espejo del backend: app/schemas/ledger.py
 */

// ── Posición financiera ──────────────────────────────────────────────────────

/** Interpretación semántica del saldo neto de un cliente en una divisa. */
export type BalancePosition = 'CLIENT_OWES' | 'COMPANY_OWES' | 'SETTLED'

/** Posición financiera de un cliente en una sola divisa. */
export interface CurrencyBalance {
  /** Saldo con signo: positivo = cliente nos debe, negativo = nosotros le debemos. */
  raw_balance: number
  /** Valor absoluto del saldo, siempre >= 0. */
  absolute_balance: number
  /** Interpretación semántica del signo. */
  position: BalancePosition
  /** Etiqueta legible para UI: "El cliente debe" | "A favor del cliente" | "Saldado" */
  display_label: string
}

/** Saldo agregado del cliente por divisa. */
export interface BalanceOut {
  client_id: string
  mxn: CurrencyBalance
  gtq: CurrencyBalance
  /** Saldo GTQ convertido a MXN a la tasa referencial. Solo visual. */
  equivalent_in_mxn?: number | null
  /** Saldo MXN convertido a GTQ a la tasa referencial. Solo visual. */
  equivalent_in_gtq?: number | null
  /** Tasa enviada por el operador (MXN por 1 GTQ). No es saldo oficial. */
  reference_exchange_rate?: number | null
}

// ── Libro mayor ──────────────────────────────────────────────────────────────

export interface LedgerEntryOut {
  id: string
  transaction_id: string
  transaction_code: string
  transaction_type: string
  currency: 'MXN' | 'GTQ'
  direction: 'CREDIT' | 'DEBIT'
  amount: number
  balance_after: number
  created_at: string
  notes?: string | null
}

export interface LedgerResponse {
  client_id: string
  total: number
  skip: number
  limit: number
  entries: LedgerEntryOut[]
  balance: BalanceOut
}

// ── Ledger agrupado (nuevo endpoint: /ledger-summary) ─────────────────────────
// Una fila por transacción. Perspectiva empresa:
//   egreso  = CREDIT en ledger (empresa dio al cliente)
//   ingreso = DEBIT  en ledger (empresa recibió del cliente)

export interface LedgerGroupedRow {
  transaction_id: string
  date: string
  reference: string
  operation: string
  egreso_mxn: string | number
  egreso_gtq: string | number
  ingreso_mxn: string | number
  ingreso_gtq: string | number
  notes?: string | null
  status: string
}

export interface LedgerGroupedSummary {
  total_egreso_mxn: string | number
  total_ingreso_mxn: string | number
  total_egreso_gtq: string | number
  total_ingreso_gtq: string | number
  /** net = ingreso - egreso. Positivo → CLIENT_OWES, negativo → COMPANY_OWES */
  net_mxn: string | number
  net_gtq: string | number
  /** 'CLIENT_OWES' | 'COMPANY_OWES' | 'SETTLED' */
  net_mxn_label: string
  net_gtq_label: string
}

export interface LedgerGroupedResponse {
  client_id: string
  total: number
  skip: number
  limit: number
  /** Totales del rango completo (independiente de paginación) */
  summary: LedgerGroupedSummary
  /** Filas paginadas, 1 por transacción */
  rows: LedgerGroupedRow[]
}

/** Texto legible para net_mxn_label / net_gtq_label */
export function netLabelText(label: string): string {
  const m: Record<string, string> = {
    CLIENT_OWES:  'El cliente debe',
    COMPANY_OWES: 'A favor del cliente',
    SETTLED:      'Saldado',
  }
  return m[label] || label
}

/** Clase CSS según net label */
export function netLabelColor(label: string): string {
  if (label === 'CLIENT_OWES')  return 'text-emerald-600 dark:text-emerald-400'
  if (label === 'COMPANY_OWES') return 'text-red-600 dark:text-red-400'
  return 'text-muted'
}

/** Border class según net label (para tarjetas destacadas) */
export function netBorderClass(label: string): string {
  if (label === 'CLIENT_OWES')  return 'border-emerald-300 dark:border-emerald-800'
  if (label === 'COMPANY_OWES') return 'border-red-300 dark:border-red-800'
  return 'border-border'
}


// ── Helpers UI ───────────────────────────────────────────────────────────────

/** Clases CSS según la posición financiera del cliente. */
export function positionColorClass(position: BalancePosition): string {
  switch (position) {
    case 'CLIENT_OWES':  return 'text-emerald-600 dark:text-emerald-400'  // verde — el cliente nos debe
    case 'COMPANY_OWES': return 'text-red-600 dark:text-red-400'           // rojo — nosotros le debemos
    case 'SETTLED':      return 'text-muted'                               // gris — saldado
  }
}

/** Badge de estado según posición. */
export function positionBadgeClass(position: BalancePosition): string {
  switch (position) {
    case 'CLIENT_OWES':  return 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300'
    case 'COMPANY_OWES': return 'bg-red-50 text-red-700 dark:bg-red-950/40 dark:text-red-300'
    case 'SETTLED':      return 'bg-slate-100 text-slate-500 dark:bg-slate-800 dark:text-slate-400'
  }
}

/** Símbolo de divisa. */
export function currencySymbol(currency: 'MXN' | 'GTQ'): string {
  return currency === 'MXN' ? '$' : 'Q'
}

/** Formato monetario consistente. */
export function fmtAmount(val: number | string | null | undefined): string {
  if (val === null || val === undefined) return '0.00'
  return Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}
