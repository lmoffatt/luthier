## Análisis de contradicciones que entorpecen la implementación

El documento es un *draft 3 no aprobado* y muchas piezas están marcadas *Proposed* o *candidate*. Eso ya es un obstáculo práctico: si se implementa sobre principios no congelados, la implementación tendrá que inventar semántica silenciosa, violando W1 y W9. Pero además hay tensiones internas más fuertes. Las agrupo por gravedad para la implementación.

---

### 1. Contradicción nuclear: G0 (teoría de tipos booleana) vs G3 (leyes valoradas en costo)

**Dónde aparece:** G0, L2, L3, L4, L11, L15, L16, L21; G3 y su nota de `[0,∞)`.

**Tensión:**  
- G0 dice: tipo = proposición; valor = prueba; ley = proposición booleana; igualdad exacta; cociente por equivalencia.  
- G3 dice: ley valorada en `[0,∞)`, verdad graduada, incertidumbre bayesiana, tolerancia dada por la demanda.

**Por qué entorpece:**  
No se puede definir el kernel sin decidir si una ley devuelve `Bool` o `Cost`. Si devuelve `Cost`, entonces:
- L2 (“membership is a guarantee”) deja de ser una garantía booleana y pasa a ser evidencia graduada.
- L4 (“certified subtype from a predicate”) necesita un umbral: `Maybe` ya no alcanza; hace falta `Maybe` con tolerancia.
- L11 y L21 necesitan saber cuándo un certificado es `Bool` y cuándo `Cost`.
- El subtipado, la inhabitación y el cociente cambian de naturaleza.

**Salida mínima:**  
Separar dos capas:
- **Kernel exacto:** `≡`, `==` estructural, tipos como proposiciones booleanas.
- **Capa de usuario:** leyes con costo, juicios graduados, certificados con evidencia.  
La pertenencia a un tipo de usuario sería un juicio con grado, no una prueba booleana. Pero esto debe decidirse *antes* de implementar el checker.

---

### 2. Cociente vs distancia/tolerancia

**Dónde aparece:** L10, G3, L15, L16.

**Tensión:**  
L10 dice que las implementaciones de una función forman un cociente por “computar la misma función hasta la igualdad de la ley”. G3 introduce distancia y tolerancia. Una relación por tolerancia no es transitiva; por tanto, no define un cociente.

**Por qué entorpece:**  
- No se puede elegir un representante por costo si no hay clase de equivalencia bien definida.
- Los bridges entre representaciones y la optimización por error quedan sin base formal.
- L15 (“Real -> Float64”) necesita una noción de aproximación, no de igualdad exacta.

**Salida mínima:**  
Cociente solo por igualdad exacta. La distancia ordena representantes dentro de la clase. O bien se abandona el cociente y se usa una categoría enriquecida/espacio métrico, con certificado de error explícito. No se puede tener ambas cosas sin especificar la relación.

---

### 3. Leyes parciales vs tipo como garantía

**Dónde aparece:** L5, L2, L11, L14, W5, W6.

**Tensión:**  
L5 dice que una ley caracteriza, pero *no necesariamente determina* la operación; las leyes se acumulan. L2 dice que pertenecer a un tipo es una garantía. L11 introduce grados de evidencia. L14 dice que sin tipo con ley no se aplica un extern.

**Por qué entorpece:**  
- ¿Cuándo una implementación “habita” un tipo? ¿Basta con pasar las leyes acumuladas? ¿Qué garantía hay si las leyes son parciales?
- W5 dice que native y extern se validan por acuerdo, pero L5 dice que native no es oráculo. Si no hay suficientes leyes, el acuerdo no prueba nada.
- W6 exige tests que fallen cuando algo está mal, pero si las leyes no determinan la función, muchas implementaciones erróneas pueden pasar.

**Salida mínima:**  
Distinguir:
- **Tipo:** firma + leyes exigidas por la demanda.
- **Teoría:** leyes acumuladas, posiblemente parciales.
- **Inhabitación:** certificado graduado contra las leyes exigidas, no garantía absoluta.  
La garantía fuerte solo existe cuando hay una ley que determina la función hasta igualdad exacta.

---

### 4. Type checking estático vs demanda

**Dónde aparece:** L4, L13, L19, L20, L17.

**Tensión:**  
L4 dice que los tipos se verifican antes de construirse. L13 dice que el olvido está determinado por la demanda. L19 dice que la demanda determina el cómputo. L20 dice que los modelos se resuelven desde el scope y se pasan explícitamente. L17 dice que todo criterio es parámetro.

**Por qué entorpece:**  
No queda claro si el type checking es estático, demand-driven o mixto. El olvido, la resolución de modelos y la tolerancia dependen de la demanda. Si el tipo de una expresión depende de lo que se pide, no se puede verificar todo antes de ejecutar.

**Salida mínima:**  
Definir un type checking bidireccional con demandas:
- Tipos universales declarados estáticamente.
- Instanciación, olvido y resolución de modelos en elaboración bajo demanda.
- Separar verificación de tipo (estática) de certificación (dinámica).

---

### 5. Igualdad: niveles exactos vs igualdad con distancia

**Dónde aparece:** L16, L12, L21, G3.

**Tensión:**  
L16 distingue `:=`, `=`, `==`, `≡`. G3 introduce distancia en la igualdad observacional. L21 dice que el tipo del resultado de la ley de identidad dice si es `Bool` o `Cost`.

**Por qué entorpece:**  
- El kernel necesita una igualdad definicional decidible (`≡`).
- La capa de usuario necesita una igualdad proposicional (`=`) que puede ser graduada.
- Si se mezclan, no se puede implementar reducción, `==` estructural ni certificados.

**Salida mínima:**  
Kernel exacto: `≡` y `==` estructural.  
Capa de usuario: `=` proposicional y `≈` con costo.  
L21 usa el tipo del resultado para decidir qué certificado emitir.

---

### 6. DAG, `<-`, sesión y bloques

**Dónde aparece:** L9, L16, L19; sección 4 “What is open”.

**Tensión:**  
L9 dice que un programa es un DAG y que las sentencias conmutan. L16 introduce `<-` para rebinding. L19 dice que el plan va hacia atrás desde las acciones y luego hay una corrida forward. La sesión con bloques y la prohibición de `<-` en top level están pendientes.

**Por qué entorpece:**  
- Un DAG no puede tener múltiples asignaciones al mismo nombre sin versionado.
- Si `<-` importa, las sentencias no conmutan.
- La memoización por hash de código, inputs y modo ignora modelo, tolerancia y parámetros implícitos, lo que produce resultados incorrectos.

**Salida mínima:**  
SSA/versionado por bloques. `<-` crea una nueva versión. La memo key incluye todos los parámetros implícitos, modelo, tolerancia y modo. Definir la semántica de sesión antes de implementar el planner.

---

### 7. Holes, externos, efectos y bootstrap

**Dónde aparece:** L8, L14, L18, W5.

**Tensión:**  
L8 permite holes first-class. L14 dice que un extern sin tipo con ley no se aplica. W5 dice que se escribe native y extern para bootstrap. L18 dice que las definiciones no tienen efectos. Pero un extern de Python puede tener efectos.

**Por qué entorpece:**  
- No se puede arrancar un concepto nuevo si el extern requiere una ley que aún no existe.
- No se puede validar un extern con efectos como si fuera una definición pura.
- Los holes y los externos compiten por el mismo espacio: ¿un extern es un habitante de un hole o una definición?

**Salida mínima:**  
Separar:
- `external` puro = definición.
- `action external` = acción con efectos.
- Para bootstrap, permitir holes con ley provisional `assumed`, con control negativo W6, hasta que la ley se establezca.

---

### 8. Módulos, modelos y bridges

**Dónde aparece:** L20, L15, L10, L13.

**Tensión:**  
L20 dice que una función se declara en una teoría y es universal sobre sus modelos; los módulos son valores; los bridges se insertan por costo. L15 dice que `Real` se realiza en `Float64`. L10 dice que hay muchas paths. L13 dice que el olvido lo determina la demanda.

**Por qué entorpece:**  
- La resolución de modelos y la instanciación aplicativa de módulos no está formalizada.
- Los bridges automáticos requieren un álgebra de composición de errores que está en la sección abierta.
- Sin esa álgebra, el planner no puede insertar bridges ni elegir representantes.

**Salida mínima:**  
Formalizar teorías/modelos como records dependientes. Resolución explícita o inferida. Bridges como funciones certificadas con ley de coerción. Composición de costos (Lipschitz, `-log p`, independencia) antes de implementar el planner.

---

### 9. Certificados: identidad vs ley, y composición de costos

**Dónde aparece:** L11, L21, L15, L19.

**Tensión:**  
L11 dice que el certificado viaja hasheado sobre el cono de dependencias. L21 dice que el certificado de identidad y el de ley se guardan aparte, y que el de ley viaja por el de identidad. Si el hash incluye el código, cualquier reimplementación invalida el certificado de ley.

**Por qué entorpece:**  
- No se sabe cuándo un certificado de ley sigue siendo válido tras un cambio de implementación.
- La incertidumbre del costo no está representada.
- La memoización y la invalidación de certificados no están definidas.

**Salida mínima:**  
Dos hashes separados:
- Hash de descripción (tipo + leyes + parámetros + modelo).
- Hash de espécimen (código + inputs + seed).
El certificado de ley depende del de descripción; el de identidad certifica que el espécimen no cambió. La composición de costos debe formalizarse antes de emitir certificados graduados.

---

### 10. G4 vs W3/W1/W4: alcance y método

**Dónde aparece:** G4, W1, W3, W4, W15.

**Tensión:**  
G4 dice “expresivo sobre restrictivo: si hay más de una forma, todas deberían poder expresarse”. W3 dice “empezar minimal y agregar solo lo usado”. W1 dice “especificación antes de implementación”. W4 dice “la aplicación real impulsa el crecimiento”.

**Por qué entorpece:**  
No es una contradicción lógica, pero paraliza decisiones de alcance. Si G4 se toma como mandato de implementación temprana, se agregan features sin presión real. Si W3 se toma como mandato, no se puede cumplir G4.

**Salida mínima:**  
W3 como orden de trabajo. G4 como criterio de diseño cuando ya hay presión de la aplicación. W15 para detectar deadlocks entre principios.

---

## Prioridad de resolución

Para desbloquear la implementación, el orden debería ser:

1. **Decidir la relación G0/G3.** ¿Kernel booleano con capa graduada, o teoría de tipos graduada desde el inicio?
2. **Definir igualdad, cociente y tolerancia.** Sin esto no hay L10, L15, L16 ni L21.
3. **Definir type checking vs demanda.** ¿Qué se verifica estáticamente y qué se elabora bajo demanda?
4. **Definir DAG, `<-`, bloques y sesión.** Sin esto no hay planner ni memoización correcta.
5. **Definir externos, efectos y holes.** Sin esto no hay bootstrap ni integración con Python.
6. **Formalizar composición de costos y bridges.** Sin esto no hay L15, L20 ni optimización por error.

## Conclusión

Las contradicciones más entorpecedoras no están en W (metodología) sino en el núcleo semántico: **G0 vs G3**, **cociente vs distancia**, **garantía vs evidencia graduada**, **estático vs demanda** e **igualdad exacta vs igualdad con costo**. Mientras no se resuelvan, cualquier implementación tendrá que inventar reglas no escritas. Eso viola W1 y W9 y hace que el documento, hoy, sea una buena declaración de intenciones pero una base insuficiente para un kernel ejecutable.