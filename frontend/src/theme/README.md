# src/theme — Tema comprado

Este directorio contiene el tema Vue 3 comprado que sirve como base visual del sistema Kambio.

## ⚠️ Reglas

- **No modificar** los archivos de este directorio sin necesidad explícita.
- **No mezclar** lógica de negocio con el código del tema.
- Los módulos del sistema viven en `src/modules/`.
- Los módulos se integran con el tema usando los slots y layouts que el tema provee.

## Estructura esperada (una vez copiado el tema)

```
src/theme/
├── assets/          # Imágenes, fuentes, íconos del tema
├── layouts/         # Layouts base (sidebar, header, etc.)
│   ├── DefaultLayout.vue
│   └── AuthLayout.vue
└── components/      # Componentes UI genéricos del tema
```

## Siguiente paso

1. Copiar los archivos del tema comprado a este directorio.
2. Identificar los layouts disponibles.
3. Adaptar `LoginPage.vue` para usar el layout de autenticación del tema.
4. Adaptar `DashboardPage.vue` para usar el layout principal del tema.
