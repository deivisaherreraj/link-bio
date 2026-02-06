# Propuesta de tareas de corrección (revisión rápida)

## 1) Tarea para corregir un error tipográfico
**Tipo:** Typo/UI copy  
**Problema detectado:** En el texto de introducción aparece la frase "soluciones de altos impacto", que es gramaticalmente incorrecta en español.  
**Ubicación:** `website_frontend/website_frontend/views/header.py`  
**Propuesta:** Cambiar a "soluciones de alto impacto" y revisar el párrafo completo para unificar estilo y puntuación.  
**Criterios de aceptación:**
- El texto mostrado en la UI usa "alto impacto".
- No se introducen cambios de layout por longitud del texto.

## 2) Tarea para corregir una falla funcional
**Tipo:** Bug/backend resiliencia  
**Problema detectado:** `ConfigCatAPI.schedule()` asume que `self.configcat` existe; cuando `CONFIGCAT_SDK_KEY` no está configurada, el atributo no se inicializa y la ruta `/schedule` puede fallar por `AttributeError`.  
**Ubicación:** `website_frontend/website_frontend/api/ConfigCatAPI.py` y `website_frontend/website_frontend/api/api.py`  
**Propuesta:** Añadir manejo defensivo en `schedule()` (igual que en `avatar_status()`), devolviendo un valor por defecto seguro (por ejemplo `{}`) cuando no haya cliente ConfigCat.  
**Criterios de aceptación:**
- Sin `CONFIGCAT_SDK_KEY`, la ruta `/schedule` responde 200 con payload por defecto.
- Con `CONFIGCAT_SDK_KEY`, se mantiene el comportamiento actual.

## 3) Tarea para corregir discrepancia en documentación/comentarios
**Tipo:** Doc mismatch  
**Problema detectado:** En `website_frontend/README.md`, el badge tiene texto alternativo "FastAPI" pero el contenido del badge y la descripción del proyecto apuntan a Reflex. Esto genera inconsistencia documental.  
**Ubicación:** `website_frontend/README.md`  
**Propuesta:** Corregir el badge para que alt-text, etiqueta y enlace sean coherentes (Reflex o FastAPI, según corresponda realmente al proyecto).  
**Criterios de aceptación:**
- El badge refleja de forma consistente la tecnología correcta.
- No quedan referencias contradictorias en ese bloque.

## 4) Tarea para mejorar una prueba
**Tipo:** Testing improvement  
**Problema detectado:** No hay cobertura automatizada visible para la normalización de estado en `avatar_status()` ni para el caso sin SDK key.  
**Ubicación sugerida para pruebas:** `website_frontend/tests/test_configcat_api.py` (nuevo archivo)  
**Propuesta:** Agregar pruebas unitarias con mocks para:
- fallback cuando falta `CONFIGCAT_SDK_KEY`;
- normalización (`strip`, comillas, `lower`) de valores de ConfigCat;
- contrato de retorno de `schedule()` en escenarios sin cliente.

**Criterios de aceptación:**
- Tests ejecutan en CI/local sin requerir acceso real a ConfigCat.
- Fallan si se rompe la normalización/fallback y pasan en estado correcto.
