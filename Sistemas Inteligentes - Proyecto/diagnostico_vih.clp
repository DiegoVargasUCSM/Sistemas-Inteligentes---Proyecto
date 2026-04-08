;;; ============================================================
;;;  SISTEMA EXPERTO VIH — VERSION COMPLETA CORREGIDA
;;; ============================================================

;;; =========================
;;; PLANTILLAS
;;; =========================

(deftemplate paciente
   (slot nombre (type STRING))
   (slot edad (type INTEGER))
   (slot sexo (type SYMBOL) (allowed-values masculino femenino otro))
   (slot id (type INTEGER)))

(deftemplate sintoma
   (slot paciente-id (type INTEGER))
   (slot tipo (type SYMBOL)))

(deftemplate factor-riesgo
   (slot paciente-id (type INTEGER))
   (slot tipo (type SYMBOL)))

(deftemplate prueba-laboratorio
   (slot paciente-id (type INTEGER))
   (slot tipo (type SYMBOL))
   (slot resultado (type SYMBOL) (allowed-values positivo negativo indeterminado pendiente))
   (slot carga-viral (type INTEGER) (default 0))
   (slot cd4 (type INTEGER) (default 0)))

(deftemplate diagnostico
   (slot paciente-id (type INTEGER))
   (slot resultado (type SYMBOL))
   (slot etapa (type SYMBOL) (default no-aplica))
   (slot nivel-riesgo (type SYMBOL))
   (slot recomendacion (type STRING))
   (slot confianza (type INTEGER)))

(deftemplate alerta
   (slot paciente-id (type INTEGER))
   (slot mensaje (type STRING))
   (slot prioridad (type SYMBOL) (allowed-values baja media alta critica)))

(deftemplate reporte-generado
   (slot paciente-id))

;;; =========================
;;; SINTOMAS
;;; =========================

(defrule sintomas-fase-aguda
   (paciente (id ?id))
   (sintoma (paciente-id ?id) (tipo fiebre-prolongada))
   (sintoma (paciente-id ?id) (tipo linfadenopatia))
   (sintoma (paciente-id ?id) (tipo faringitis))
   =>
   (assert (alerta
      (paciente-id ?id)
      (mensaje "ALERTA: Triada clásica de síndrome retroviral agudo detectada.")
      (prioridad alta))))

(defrule sintoma-erupcion-cutanea
   (paciente (id ?id))
   (sintoma (paciente-id ?id) (tipo fiebre-prolongada))
   (sintoma (paciente-id ?id) (tipo erupcion-cutanea))
   =>
   (assert (alerta
      (paciente-id ?id)
      (mensaje "Erupción maculopapular con fiebre.")
      (prioridad alta))))

(defrule sintomas-constitucionales
   (paciente (id ?id))
   (sintoma (paciente-id ?id) (tipo perdida-peso))
   (sintoma (paciente-id ?id) (tipo sudoracion-nocturna))
   (sintoma (paciente-id ?id) (tipo fatiga-cronica))
   =>
   (assert (alerta
      (paciente-id ?id)
      (mensaje "Síntomas constitucionales persistentes.")
      (prioridad media))))

;;; =========================
;;; FACTORES DE RIESGO
;;; =========================

(defrule riesgo-alto-multiple
   (paciente (id ?id))
   (factor-riesgo (paciente-id ?id) (tipo relaciones-sin-proteccion))
   (factor-riesgo (paciente-id ?id) (tipo multiple-parejas))
   =>
   (assert (alerta
      (paciente-id ?id)
      (mensaje "Riesgo epidemiológico elevado.")
      (prioridad alta))))

(defrule riesgo-udi
   (paciente (id ?id))
   (factor-riesgo (paciente-id ?id) (tipo uso-drogas-iv))
   =>
   (assert (alerta
      (paciente-id ?id)
      (mensaje "Uso de drogas IV.")
      (prioridad critica))))

;;; =========================
;;; DIAGNOSTICO (CORREGIDO)
;;; =========================

(defrule diagnostico-confirmado
   (declare (salience 10))
   (paciente (id ?id))
   (prueba-laboratorio (paciente-id ?id) (tipo elisa-4ta-gen) (resultado positivo))
   (prueba-laboratorio (paciente-id ?id) (tipo western-blot) (resultado positivo))
   (not (diagnostico (paciente-id ?id)))
   =>
   (assert (diagnostico
      (paciente-id ?id)
      (resultado vih-confirmado)
      (nivel-riesgo confirmado)
      (recomendacion "VIH confirmado.")
      (confianza 99))))

;;; =========================
;;; ESTADIFICACION (FIX modify)
;;; =========================

(defrule estadio-1-vih
   (declare (salience 5))
   ?d <- (diagnostico (paciente-id ?id) (resultado vih-confirmado))
   (prueba-laboratorio (paciente-id ?id) (tipo conteo-cd4) (cd4 ?cd4&:(>= ?cd4 500)))
   =>
   (modify ?d
      (etapa estadio-1-CDC)
      (recomendacion "Estadio 1")))

(defrule estadio-3-sida
   (declare (salience 5))
   ?d <- (diagnostico (paciente-id ?id) (resultado vih-confirmado))
   (prueba-laboratorio (paciente-id ?id) (tipo conteo-cd4) (cd4 ?cd4&:(< ?cd4 200)))
   =>
   (modify ?d
      (resultado sida-estadio-3)
      (etapa estadio-3-SIDA)
      (nivel-riesgo critico)
      (recomendacion "SIDA confirmado"))
   (assert (alerta
      (paciente-id ?id)
      (mensaje "SIDA estadio 3")
      (prioridad critica))))

;;; =========================
;;; REPORTE FINAL (FIX)
;;; =========================

(defrule generar-reporte-final
   (declare (salience -10))
   (paciente (id ?id) (nombre ?nombre))
   (diagnostico (paciente-id ?id) (resultado ?resultado) (nivel-riesgo ?riesgo) (recomendacion ?rec))
   (not (reporte-generado (paciente-id ?id)))
   =>
   (printout t crlf
      "==============================" crlf
      " REPORTE FINAL " crlf
      "==============================" crlf
      "Paciente: " ?nombre crlf
      "Resultado: " ?resultado crlf
      "Riesgo: " ?riesgo crlf
      "Recomendacion: " ?rec crlf
      "==============================" crlf)

   (assert (reporte-generado (paciente-id ?id))))