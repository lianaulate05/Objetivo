from openpyxl import Workbook
from pathlib import Path

base = Path(r"C:\Users\liana.ulate\OneDrive - BABEL\Objetivos Babel\2026\Generar una guía práctica de prompts para actividades de QA, incluyendo al menos 3 ejemplos aplicados a tareas reales del rol tales\Objetivo")
out_dir = base / "CasosPrueba"
out_dir.mkdir(exist_ok=True)
out_file = out_dir / "HU-SM-WEB-001-CasosPrueba.xlsx"

wb = Workbook()
ws = wb.active
ws.title = "Casos de Prueba"
ws.append(["Titulo", "Accion", "Resultado Esperado"])

cases = [
    ("CP-001 Transferencia SINPE exitosa", "Precondición: Cliente autenticado, cuenta origen activa con saldo suficiente.", "La precondición queda establecida."),
    ("", "Seleccionar cuenta origen.", "Se presenta la opción de cuenta origen y queda seleccionada."),
    ("", "Ingresar teléfono destino válido y afiliado.", "El sistema acepta el formato y valida la afiliación del número."),
    ("", "Ingresar monto válido dentro del límite por transacción y observación opcional.", "El monto y la observación son aceptados y se calcula el resumen, comisión y total a debitar."),
    ("", "Confirmar la transferencia.", "Se valida saldo, límites y se procesa la operación con SINPE."),
    ("", "Revisar comprobante generado.", "Se emite comprobante con referencia, monto, comisión, total debitado y estado exitoso."),

    ("CP-002 Transferencia con OTP requerido", "Precondición: Cliente autenticado, monto mayor a ₡50.000 y OTP vigente.", "La precondición queda establecida."),
    ("", "Ingresar datos de transferencia con monto mayor a ₡50.000.", "El sistema identifica que requiere OTP."),
    ("", "Confirmar la operación.", "Se solicita OTP al usuario."),
    ("", "Ingresar OTP correcto dentro de 5 minutos.", "El OTP es aceptado y la operación continúa."),
    ("", "Finalizar la transacción.", "La transferencia se procesa correctamente y se genera comprobante."),

    ("CP-003 Fondos insuficientes", "Precondición: Cuenta origen activa con saldo menor al monto más comisión.", "La precondición queda establecida."),
    ("", "Ingresar teléfono destino válido y un monto mayor al saldo disponible.", "El sistema valida la cuenta y detecta déficit."),
    ("", "Confirmar la operación.", "Se bloquea la transacción y se muestra el mensaje SM001."),
    ("", "Verificar débito de la cuenta.", "No se realiza ningún débito ni se genera comprobante de éxito."),

    ("CP-004 Teléfono no afiliado", "Precondición: Usuario autenticado y teléfono destino no registrado como afiliado.", "La precondición queda establecida."),
    ("", "Ingresar un número no afiliado.", "El sistema valida el formato y la afiliación del teléfono."),
    ("", "Confirmar la operación.", "Se rechaza la operación y se muestra el mensaje SM002."),
    ("", "Revisar estado final.", "La transacción no se procesa y no se debita ninguna cuenta."),

    ("CP-005 OTP incorrecto", "Precondición: Cliente autenticado y la operación requiere OTP.", "La precondición queda establecida."),
    ("", "Ingresar datos válidos y confirmar.", "Se solicita OTP."),
    ("", "Ingresar OTP incorrecto.", "El sistema rechaza el OTP y muestra el mensaje SM003."),
    ("", "Intentar nuevamente.", "La operación sigue bloqueada hasta que el OTP sea correcto."),

    ("CP-006 OTP expirado", "Precondición: OTP generado para una operación que requiere autenticación.", "La precondición queda establecida."),
    ("", "Esperar vencimiento del OTP.", "El sistema considera que el OTP ya no es válido."),
    ("", "Ingresar OTP vencido.", "Se muestra el mensaje SM004 y la operación no continúa."),
    ("", "Solicitar nueva validación.", "Se debe regenerar el OTP para continuar con la operación."),

    ("CP-007 Límite diario excedido", "Precondición: Cliente con acumulado diario cercano o igual a ₡2.000.000.", "La precondición queda establecida."),
    ("", "Ingresar un monto que hace superar el límite diario.", "El sistema valida el acumulado diario vigente."),
    ("", "Confirmar la operación.", "Se rechaza la operación y se muestra el mensaje SM005."),
    ("", "Verificar la transacción.", "No se ejecuta el débito ni se genera comprobante exitoso."),

    ("CP-008 Límite por transacción excedido", "Precondición: Cliente autenticado y monto mayor al límite de la transacción.", "La precondición queda establecida."),
    ("", "Ingresar un monto superior a ₡500.000.", "El sistema identifica que supera el máximo permitido."),
    ("", "Confirmar la transferencia.", "Se rechaza la operación y se muestra el mensaje SM006."),
    ("", "Verificar registro.", "No se procesa la transacción ni se debita el monto."),

    ("CP-009 Servicio SINPE no disponible", "Precondición: Cliente autenticado con datos válidos y servicio SINPE temporalmente fuera de servicio.", "La precondición queda establecida."),
    ("", "Ingresar datos válidos y confirmar la operación.", "El sistema intenta enviar la solicitud a SINPE."),
    ("", "Observar respuesta de servicio no disponible.", "Se generan reintentos hasta 3 veces y luego se muestra el mensaje SM007."),
    ("", "Revisar estado de la operación.", "La operación queda fallida o pendiente según el estado final de confirmación."),

    ("CP-010 Cuenta bloqueada", "Precondición: Cuenta origen bloqueada por la entidad.", "La precondición queda establecida."),
    ("", "Seleccionar la cuenta origen bloqueada.", "El sistema identifica que la cuenta no puede realizar transferencias."),
    ("", "Intentar continuar con la operación.", "Se bloquea la acción y se muestra el mensaje SM008."),
    ("", "Verificar saldo y débito.", "No se realiza ningún débito ni procesamiento de transferencia."),

    ("CP-011 Sesión expirada antes de confirmar", "Precondición: Usuario autenticado y operación en curso.", "La precondición queda establecida."),
    ("", "Ingresar datos de la transferencia.", "El sistema presenta resumen y confirmación."),
    ("", "La sesión expira antes de la confirmación.", "Se cancela la operación y se muestra el mensaje SM009."),
    ("", "Verificar operación.", "La transacción no continúa ni se debita el saldo."),

    ("CP-012 Duplicidad por doble clic o reenvío", "Precondición: Operación en proceso sin confirmación final y con Idempotency Key activo.", "La precondición queda establecida."),
    ("", "Solicitar la transferencia para un mismo monto, teléfono y cuenta.", "El sistema registra la solicitud con Transaction ID e Idempotency Key."),
    ("", "Reintentar la misma acción por doble clic o reenvío.", "El sistema detecta duplicidad y evita un segundo débito."),
    ("", "Validar resultado final.", "Se procesa una sola transacción y se genera un único comprobante."),

    ("CP-013 Caso límite monto máximo", "Precondición: Cuenta origen activa con saldo suficiente y sin restricciones de riesgo.", "La precondición queda establecida."),
    ("", "Ingresar un monto exactamente igual a ₡500.000.", "El sistema acepta el valor como válido dentro del máximo permitido."),
    ("", "Confirmar la operación.", "La transferencia se procesa exitosamente y se debita el monto autorizado."),
    ("", "Comprobar comprobante.", "Se emite comprobante con el monto exacto autorizado."),

    ("CP-014 Caso límite máximo diario", "Precondición: Acumulado diario igual a ₡2.000.000 y sin excedentes.", "La precondición queda establecida."),
    ("", "Ingresar una nueva transferencia con monto que alcance el límite diario.", "El sistema valida el acumulado diario y detecta que ya se alcanzó el máximo."),
    ("", "Confirmar la operación.", "La transacción se rechaza con el mensaje SM005."),
    ("", "Verificar saldo.", "No se debita ni se genera comprobante de éxito."),

    ("CP-015 Validación previa al débito", "Precondición: Cliente autenticado con datos de transferencia incompletos o inválidos.", "La precondición queda establecida."),
    ("", "Ingresar teléfono con formato no válido o monto con más de dos decimales.", "El sistema valida el formato y los datos antes de continuar."),
    ("", "Intentar confirmar la operación.", "La transacción queda bloqueada y no se efectúa ningún débito."),
    ("", "Comprobar mensaje de error.", "Se muestra el mensaje apropiado según la validación fallida y la operación no se ejecuta."),
]

for row in cases:
    ws.append(list(row))

for cell in ws[1]:
    cell.font = cell.font.copy(bold=True)

ws.freeze_panes = "A2"
ws.column_dimensions["A"].width = 38
ws.column_dimensions["B"].width = 55
ws.column_dimensions["C"].width = 52

wb.save(out_file)
print(f"Archivo generado: {out_file}")
print(f"Existe: {out_file.exists()}")
print(f"Filas: {ws.max_row}")
print(f"Hoja: {ws.title}")
