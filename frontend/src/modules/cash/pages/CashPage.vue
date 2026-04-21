<template>
  <div class="px-5 py-6 space-y-6">

    <!-- Loading -->
    <div v-if="loadingCash" class="flex items-center justify-center py-20">
      <div class="flex flex-col items-center gap-3 text-muted">
        <svg class="animate-spin" xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
        <span class="text-sm">Consultando caja...</span>
      </div>
    </div>

    <!-- No hay caja abierta -->
    <div v-else-if="noSession || !currentSession" class="flex flex-col items-center justify-center py-20 gap-5">
      <div class="w-20 h-20 rounded-2xl bg-warning-light flex items-center justify-center shadow-sm">
        <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="text-warning-dark"><path d="M21 12V7H5a2 2 0 0 1 0-4h14v4"/><path d="M3 5v14a2 2 0 0 0 2 2h16v-5"/><path d="M18 12a2 2 0 0 0 0 4h4v-4Z"/></svg>
      </div>
      <div class="text-center">
        <h3 class="text-xl font-bold text-foreground mb-2">No hay caja abierta</h3>
        <p class="text-sm text-muted max-w-sm">Para registrar transacciones, primero abre una sesión indicando el saldo inicial en MXN y GTQ.</p>
      </div>
      <Button @click="showOpenModal = true" class="px-6 h-10 text-sm font-semibold shadow-md">Abrir Caja</Button>
    </div>

    <!-- ═══ CAJA ABIERTA ═══ -->
    <div v-else-if="currentSession && currentSession.status === 'open'" class="space-y-6">

      <!-- Banner Principal -->
      <div class="relative bg-card border border-border rounded-2xl shadow-sm overflow-hidden">
        <div class="absolute inset-y-0 left-0 w-1.5 bg-gradient-to-b from-primary to-primary-dark rounded-l-2xl"></div>
        <div class="pl-7 pr-6 py-5 flex items-center gap-4">
          <!-- Ícono -->
          <div class="w-12 h-12 rounded-xl bg-primary-light flex items-center justify-center text-primary flex-shrink-0">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="3" rx="2"/><line x1="8" x2="16" y1="21" y2="21"/><line x1="12" x2="12" y1="17" y2="21"/></svg>
          </div>
          <!-- Info -->
          <div class="min-w-0 flex-1">
            <div class="flex items-center gap-2 flex-wrap">
              <h2 class="text-base font-bold text-foreground">Caja Principal</h2>
              <span class="font-mono text-xs text-muted">#{{ currentSession.id.split('-')[0].toUpperCase() }}</span>
              <span class="inline-flex items-center gap-1 px-2 py-0.5 text-[10px] font-bold uppercase tracking-wide text-success-dark bg-success-light rounded-full">
                <span class="w-1.5 h-1.5 rounded-full bg-success-dark animate-pulse"></span>Aperturado
              </span>
            </div>
            <div class="flex flex-wrap gap-x-4 gap-y-0.5 mt-1">
              <p class="text-xs text-muted">Responsable: <span class="font-semibold text-foreground">{{ userName }}</span></p>
              <p class="text-xs text-muted">Apertura: <span class="font-medium text-foreground">{{ formatDateTime(currentSession.opened_at) }}</span></p>
            </div>
          </div>
          <!-- Botón Corte — alineado a la derecha del banner, estilo destructivo sutil -->
          <button @click="showCloseModal = true"
            class="flex-shrink-0 inline-flex items-center gap-2 px-4 h-9 text-sm font-semibold text-red-600 bg-transparent border border-red-200 hover:bg-red-50 hover:border-red-400 dark:border-red-900 dark:hover:bg-red-950/40 dark:text-red-400 active:scale-95 rounded-xl transition-all duration-150">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
            Corte de Caja
          </button>
        </div>
      </div>


      <!-- Acciones Rápidas (2 cards — sin Historial duplicado) -->
      <div>
        <h3 class="text-xs font-bold text-muted uppercase tracking-wider mb-3">Acciones Rápidas</h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div @click="$router.push('/transactions')"
            class="group bg-card border border-border rounded-xl p-5 shadow-sm hover:shadow-md hover:border-primary/40 transition-all duration-200 cursor-pointer flex items-center gap-4">
            <div class="w-11 h-11 rounded-xl bg-primary-light flex items-center justify-center text-primary group-hover:scale-110 transition-transform duration-200 flex-shrink-0">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/></svg>
            </div>
            <div>
              <p class="text-sm font-bold text-foreground">Nueva Transacción</p>
              <p class="text-xs text-muted mt-0.5">Registrar cambio de divisas</p>
            </div>
            <svg class="ml-auto text-muted group-hover:text-primary transition-colors" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 18 6-6-6-6"/></svg>
          </div>

          <div class="group bg-card border border-border rounded-xl p-5 shadow-sm hover:shadow-md hover:border-primary/40 transition-all duration-200 cursor-pointer flex items-center gap-4">
            <div class="w-11 h-11 rounded-xl bg-info-light flex items-center justify-center text-info group-hover:scale-110 transition-transform duration-200 flex-shrink-0">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/></svg>
            </div>
            <div>
              <p class="text-sm font-bold text-foreground">Retiro / Fondo</p>
              <p class="text-xs text-muted mt-0.5">Agregar o retirar efectivo</p>
            </div>
            <svg class="ml-auto text-muted group-hover:text-primary transition-colors" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 18 6-6-6-6"/></svg>
          </div>
        </div>
      </div>

      <!-- Resumen de Caja -->
      <div>
        <h3 class="text-xs font-bold text-muted uppercase tracking-wider mb-3">Resumen de Caja</h3>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">

          <!-- Saldo Apertura -->
          <div class="bg-card border border-border rounded-xl p-5 shadow-sm">
            <div class="flex items-center gap-2 mb-3">
              <div class="w-7 h-7 rounded-lg bg-slate-100 dark:bg-slate-800 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-muted"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
              </div>
              <p class="text-xs font-semibold text-muted uppercase tracking-wide">Saldo Apertura</p>
            </div>
            <p class="text-2xl font-bold font-mono text-foreground leading-tight">$ {{ formatCurrency(currentSession.opening_amount_mxn) }}</p>
            <p class="text-lg font-bold font-mono text-muted mt-1">Q {{ formatCurrency(currentSession.opening_amount_gtq) }}</p>
          </div>

          <!-- Movimiento Neto -->
          <div class="bg-card border border-border rounded-xl p-5 shadow-sm">
            <div class="flex items-center gap-2 mb-3">
              <div class="w-7 h-7 rounded-lg bg-slate-100 dark:bg-slate-800 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-muted"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>
              </div>
              <p class="text-xs font-semibold text-muted uppercase tracking-wide">Movimiento Neto</p>
            </div>
            <p class="text-2xl font-bold font-mono leading-tight" :class="cashMovement.mxn >= 0 ? 'text-success-dark' : 'text-error'">
              {{ cashMovement.mxn >= 0 ? '+' : '' }}$ {{ formatCurrency(cashMovement.mxn) }}
            </p>
            <p class="text-lg font-bold font-mono mt-1" :class="cashMovement.gtq >= 0 ? 'text-success-dark' : 'text-error'">
              {{ cashMovement.gtq >= 0 ? '+' : '' }}Q {{ formatCurrency(cashMovement.gtq) }}
            </p>
          </div>

          <!-- Saldo Esperado (destacado) -->
          <div class="relative bg-gradient-to-br from-primary-light/60 to-primary-light/20 border-2 border-primary rounded-xl p-5 shadow-md overflow-hidden">
            <div class="absolute top-0 right-0 w-20 h-20 bg-primary/5 rounded-full -translate-y-6 translate-x-6 pointer-events-none"></div>
            <div class="flex items-center gap-2 mb-3">
              <div class="w-7 h-7 rounded-lg bg-primary/20 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-primary-dark"><rect width="20" height="14" x="2" y="3" rx="2"/><line x1="8" x2="16" y1="21" y2="21"/><line x1="12" x2="12" y1="17" y2="21"/></svg>
              </div>
              <p class="text-xs font-semibold text-primary uppercase tracking-wide">Saldo en Caja</p>
            </div>
            <p class="text-2xl font-bold font-mono text-primary-dark leading-tight">$ {{ formatCurrency(currentSession.current_amount_mxn) }}</p>
            <p class="text-lg font-bold font-mono text-primary-dark mt-1">Q {{ formatCurrency(currentSession.current_amount_gtq) }}</p>
            <p class="text-[10px] text-primary/70 mt-2 font-medium">Calculado por el sistema</p>
          </div>

        </div>
      </div>

      <!-- Actividad Reciente -->
      <div class="bg-card border border-border rounded-xl shadow-sm overflow-hidden">
        <div class="px-5 py-4 border-b border-border flex justify-between items-center">
          <div class="flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-primary"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <h3 class="text-sm font-bold">Actividad Reciente</h3>
          </div>
          <router-link to="/transactions" class="inline-flex items-center gap-1 text-xs text-primary hover:text-primary-dark font-medium transition-colors">
            Ver todo <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m9 18 6-6-6-6"/></svg>
          </router-link>
        </div>

        <div v-if="recentTransactions.length > 0" class="divide-y divide-border">
          <div v-for="txn in recentTransactions" :key="txn.id"
            class="px-5 py-3.5 flex items-center justify-between hover:bg-slate-50 dark:hover:bg-slate-900/40 transition-colors">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
                :class="txn.status === 'ACTIVE' ? 'bg-success-light text-success-dark' : 'bg-slate-100 text-muted dark:bg-slate-800'">
                <svg v-if="txn.status === 'ACTIVE'" xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" x2="6" y1="6" y2="18"/><line x1="6" x2="18" y1="6" y2="18"/></svg>
              </div>
              <div>
                <p class="text-sm font-semibold text-foreground">
                  {{ typeLabel(txn.transaction_type) }}
                  <span class="font-mono text-xs text-muted font-normal">#{{ (txn.code?.split('-')[1] || txn.code || '').substring(0, 6).toUpperCase() }}</span>
                </p>
                <p class="text-xs text-muted">{{ timeAgo(txn.created_at) }}</p>
              </div>
            </div>
            <div class="text-right">
              <p v-if="Number(txn.amount_mxn) > 0" class="text-sm font-bold"
                :class="txn.status === 'ACTIVE' ? 'text-success-dark' : 'text-muted line-through'">
                +${{ formatCurrency(txn.amount_mxn) }}
              </p>
              <p v-if="Number(txn.amount_gtq) > 0" class="text-xs font-semibold mt-0.5"
                :class="txn.status === 'ACTIVE' ? 'text-info' : 'text-muted line-through'">
                +Q{{ formatCurrency(txn.amount_gtq) }}
              </p>
            </div>
          </div>
        </div>

        <div v-else class="flex flex-col items-center justify-center py-10 gap-2">
          <div class="w-10 h-10 rounded-xl bg-slate-100 dark:bg-slate-800 flex items-center justify-center mb-1">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="text-muted"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          </div>
          <p class="text-sm font-medium text-foreground">Sin actividad en este turno</p>
          <p class="text-xs text-muted">Las transacciones aparecerán aquí al registrarlas</p>
        </div>
      </div>

    </div><!-- /caja abierta -->

    <!-- Última caja cerrada -->
    <div v-else-if="currentSession && currentSession.status === 'closed'" class="flex flex-col items-center justify-center py-20 gap-5">
      <div class="w-20 h-20 rounded-2xl bg-primary-light flex items-center justify-center shadow-sm">
        <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="text-primary-dark"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>
      </div>
      <div class="text-center">
        <h3 class="text-xl font-bold text-foreground mb-1">Última caja cerrada</h3>
        <p class="text-sm text-muted">Cerrada el {{ formatDate(currentSession.closed_at!) }}</p>
      </div>
      <Button @click="showOpenModal = true" class="px-6 h-10 text-sm font-semibold shadow-md">Abrir Nueva Caja</Button>
    </div>

    <!-- ═══ MODAL ABRIR ═══ -->
    <Teleport to="body">
      <div v-if="showOpenModal" class="fixed inset-0 z-[9999] flex items-end sm:items-center justify-center bg-black/50 backdrop-blur-sm p-4">
        <div class="bg-card w-full max-w-md rounded-2xl shadow-2xl border border-border overflow-hidden">
          <div class="px-6 py-4 border-b border-border flex justify-between items-center">
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 rounded-lg bg-primary-light flex items-center justify-center text-primary">
                <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12V7H5a2 2 0 0 1 0-4h14v4"/><path d="M3 5v14a2 2 0 0 0 2 2h16v-5"/><path d="M18 12a2 2 0 0 0 0 4h4v-4Z"/></svg>
              </div>
              <h3 class="text-base font-bold">Abrir Caja</h3>
            </div>
            <button @click="showOpenModal = false" class="w-8 h-8 rounded-lg hover:bg-hover flex items-center justify-center text-muted hover:text-foreground transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" x2="6" y1="6" y2="18"/><line x1="6" x2="18" y1="6" y2="18"/></svg>
            </button>
          </div>
          <form @submit.prevent="handleOpen" class="p-6 space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div class="flex flex-col gap-1.5">
                <label class="text-xs font-semibold text-muted uppercase tracking-wide">MXN Inicial</label>
                <div class="relative">
                  <span class="absolute left-3 top-1/2 -translate-y-1/2 text-sm text-muted font-semibold select-none">$</span>
                  <input v-model.number="openForm.opening_amount_mxn" type="number" step="0.01" min="0" required
                    class="w-full h-10 pl-7 pr-3 text-sm bg-transparent border rounded-lg border-border text-foreground outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all" placeholder="0.00" />
                </div>
              </div>
              <div class="flex flex-col gap-1.5">
                <label class="text-xs font-semibold text-muted uppercase tracking-wide">GTQ Inicial</label>
                <div class="relative">
                  <span class="absolute left-3 top-1/2 -translate-y-1/2 text-sm text-muted font-semibold select-none">Q</span>
                  <input v-model.number="openForm.opening_amount_gtq" type="number" step="0.01" min="0" required
                    class="w-full h-10 pl-7 pr-3 text-sm bg-transparent border rounded-lg border-border text-foreground outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all" placeholder="0.00" />
                </div>
              </div>
            </div>
            <div class="flex justify-end gap-2 pt-1">
              <Button type="button" variant="outline" @click="showOpenModal = false" class="h-9 text-sm">Cancelar</Button>
              <Button type="submit" :disabled="formLoading" class="h-9 text-sm px-5 shadow-md">
                <svg v-if="formLoading" class="animate-spin mr-1.5" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
                {{ formLoading ? 'Abriendo...' : 'Confirmar Apertura' }}
              </Button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>

    <!-- ═══ MODAL CERRAR ═══ -->
    <Teleport to="body">
      <div v-if="showCloseModal" class="fixed inset-0 z-[9999] flex items-end sm:items-center justify-center bg-black/50 backdrop-blur-sm p-4">
        <div class="bg-card w-full max-w-md rounded-2xl shadow-2xl border border-border overflow-hidden">
          <div class="px-6 py-4 border-b border-border flex justify-between items-center">
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 rounded-lg bg-orange-100 flex items-center justify-center text-orange-600">
                <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="11" x="3" y="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              </div>
              <h3 class="text-base font-bold">Corte de Caja</h3>
            </div>
            <button @click="showCloseModal = false" class="w-8 h-8 rounded-lg hover:bg-hover flex items-center justify-center text-muted hover:text-foreground transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" x2="6" y1="6" y2="18"/><line x1="6" x2="18" y1="6" y2="18"/></svg>
            </button>
          </div>
          <form @submit.prevent="handleClose" class="p-6 space-y-4">
            <!-- Referencia del sistema -->
            <div class="bg-slate-50 dark:bg-slate-900 border border-border rounded-xl p-4">
              <p class="text-xs font-semibold text-muted uppercase tracking-wide mb-3">Saldo esperado por el sistema</p>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <p class="text-[10px] text-muted mb-0.5">MXN</p>
                  <p class="text-xl font-bold font-mono text-foreground">$ {{ formatCurrency(currentSession?.current_amount_mxn) }}</p>
                </div>
                <div>
                  <p class="text-[10px] text-muted mb-0.5">GTQ</p>
                  <p class="text-xl font-bold font-mono text-foreground">Q {{ formatCurrency(currentSession?.current_amount_gtq) }}</p>
                </div>
              </div>
            </div>
            <!-- Conteo físico -->
            <div class="grid grid-cols-2 gap-4">
              <div class="flex flex-col gap-1.5">
                <label class="text-xs font-semibold text-muted uppercase tracking-wide">Físico MXN <span class="text-error">*</span></label>
                <div class="relative">
                  <span class="absolute left-3 top-1/2 -translate-y-1/2 text-sm text-muted font-semibold select-none">$</span>
                  <input v-model.number="closeForm.closing_amount_mxn" type="number" step="0.01" min="0" required
                    class="w-full h-10 pl-7 pr-3 text-sm bg-transparent border rounded-lg border-border text-foreground outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all" placeholder="0.00" />
                </div>
              </div>
              <div class="flex flex-col gap-1.5">
                <label class="text-xs font-semibold text-muted uppercase tracking-wide">Físico GTQ <span class="text-error">*</span></label>
                <div class="relative">
                  <span class="absolute left-3 top-1/2 -translate-y-1/2 text-sm text-muted font-semibold select-none">Q</span>
                  <input v-model.number="closeForm.closing_amount_gtq" type="number" step="0.01" min="0" required
                    class="w-full h-10 pl-7 pr-3 text-sm bg-transparent border rounded-lg border-border text-foreground outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all" placeholder="0.00" />
                </div>
              </div>
            </div>
            <!-- Preview diferencia -->
            <div v-if="closeForm.closing_amount_mxn > 0 || closeForm.closing_amount_gtq > 0"
              class="rounded-xl px-4 py-3 border"
              :class="hasDifference ? 'border-amber-300 bg-amber-50 dark:bg-amber-950/30' : 'border-emerald-300 bg-emerald-50 dark:bg-emerald-950/30'">
              <p class="text-xs font-semibold mb-1.5" :class="hasDifference ? 'text-amber-700 dark:text-amber-400' : 'text-emerald-700 dark:text-emerald-400'">
                {{ hasDifference ? '⚠️ Diferencia detectada' : '✓ Cuadre exacto' }}
              </p>
              <div class="flex gap-6 font-mono font-bold text-sm">
                <span :class="closeDiffMxn === 0 ? 'text-muted' : closeDiffMxn > 0 ? 'text-emerald-600' : 'text-red-600'">
                  MXN: {{ closeDiffMxn >= 0 ? '+' : '' }}{{ formatCurrency(closeDiffMxn) }}
                </span>
                <span :class="closeDiffGtq === 0 ? 'text-muted' : closeDiffGtq > 0 ? 'text-emerald-600' : 'text-red-600'">
                  GTQ: {{ closeDiffGtq >= 0 ? '+' : '' }}{{ formatCurrency(closeDiffGtq) }}
                </span>
              </div>
            </div>
            <!-- Notas -->
            <div class="flex flex-col gap-1.5">
              <label class="text-xs font-semibold text-muted uppercase tracking-wide">Notas (opcional)</label>
              <textarea v-model="closeForm.notes" rows="2"
                class="w-full px-3 py-2 text-sm bg-transparent border rounded-lg border-border text-foreground outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all resize-none"
                placeholder="Justificación de diferencias si las hay"></textarea>
            </div>
            <div class="flex justify-end gap-2 pt-1">
              <Button type="button" variant="outline" @click="showCloseModal = false" class="h-9 text-sm">Cancelar</Button>
              <button type="submit" :disabled="formLoading"
                class="inline-flex items-center gap-2 px-5 h-9 text-sm font-semibold text-white bg-orange-500 hover:bg-orange-600 disabled:opacity-50 rounded-lg shadow-sm transition-all active:scale-95">
                <svg v-if="formLoading" class="animate-spin" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
                {{ formLoading ? 'Procesando...' : 'Confirmar Corte' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>

  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useCash } from '@/modules/cash/composables/useCash'
import { useTransactions } from '@/modules/transactions/composables/useTransactions'
import { useAuthStore } from '@/modules/auth/stores/authStore'
import { Button } from '@/theme/components/ui/button'

const { currentSession, loading: loadingCash, noSession, fetchCurrent, openCash, closeCash } = useCash()
const { transactions, loadTransactions } = useTransactions()
const authStore = useAuthStore()

const userName = computed(() => authStore.user?.full_name || 'Operador')

const showOpenModal = ref(false)
const showCloseModal = ref(false)
const formLoading = ref(false)

const openForm = reactive({ opening_amount_mxn: 0, opening_amount_gtq: 0, notes: '' })
const closeForm = reactive({ closing_amount_mxn: 0, closing_amount_gtq: 0, notes: '' })

onMounted(async () => {
  await fetchCurrent()
  if (currentSession.value && currentSession.value.status === 'open') {
    await loadTransactions()
  }
})

const sessionTxns = computed(() => {
  if (!currentSession.value) return []
  return transactions.value.filter(t => t.cash_session_id === currentSession.value!.id)
})

const recentTransactions = computed(() => sessionTxns.value.slice(0, 5))

const cashMovement = computed(() => {
  if (!currentSession.value) return { mxn: 0, gtq: 0 }
  return {
    mxn: Number(currentSession.value.current_amount_mxn || 0) - Number(currentSession.value.opening_amount_mxn || 0),
    gtq: Number(currentSession.value.current_amount_gtq || 0) - Number(currentSession.value.opening_amount_gtq || 0),
  }
})

const closeDiffMxn = computed(() => (closeForm.closing_amount_mxn || 0) - Number(currentSession.value?.current_amount_mxn || 0))
const closeDiffGtq = computed(() => (closeForm.closing_amount_gtq || 0) - Number(currentSession.value?.current_amount_gtq || 0))
const hasDifference = computed(() => Math.abs(closeDiffMxn.value) > 0.01 || Math.abs(closeDiffGtq.value) > 0.01)

const formatCurrency = (val?: string | number | null) => {
  if (val === undefined || val === null) return '0.00'
  return Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatDate = (dateString: string) => new Date(dateString).toLocaleDateString('es-ES')
const formatDateTime = (dateString: string) => {
  const d = new Date(dateString)
  return d.toLocaleDateString('es-ES', { weekday: 'short', day: '2-digit', month: 'short', year: 'numeric' }) + ', ' + d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
}
const timeAgo = (dateString: string) => new Date(dateString).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })

const typeLabel = (t: string) => {
  const ms: Record<string, string> = { SELL_MXN: 'Venta MXN', BUY_MXN: 'Compra MXN', SELL_GTQ: 'Venta GTQ', BUY_GTQ: 'Compra GTQ', PAYMENT: 'Pago', WITHDRAWAL: 'Retiro' }
  return ms[t] || t
}

async function handleOpen() {
  formLoading.value = true
  try {
    await openCash(openForm)
    showOpenModal.value = false
    await loadTransactions()
  } catch {
    // error notificado en el composable
  } finally {
    formLoading.value = false
  }
}

async function handleClose() {
  if (!currentSession.value) return
  formLoading.value = true
  try {
    await closeCash(currentSession.value.id, closeForm)
    showCloseModal.value = false
  } finally {
    formLoading.value = false
  }
}
</script>
