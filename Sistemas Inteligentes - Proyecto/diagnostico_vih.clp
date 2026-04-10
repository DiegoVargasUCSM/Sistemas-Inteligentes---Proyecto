;;; ============================================================
;;;  SISTEMA EXPERTO — DIAGNÓSTICO VIH
;;;  CLIPS | Basado en criterios CDC/OMS
;;; ============================================================

;;; --- PLANTILLAS ---

(deftemplate paciente
   (slot id (type INTEGER))
   (slot nombre (type STRING))
   (slot edad (type INTEGER))
   (slot sexo (type SYMBOL) (allowed-values masculino femenino otro)))

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
   (slot confianza (type INTEGER) (default 0)))

(deftemplate alerta
   (slot paciente-id (type INTEGER))
   (slot mensaje (type STRING))
   (slot prioridad (type SYMBOL) (allowed-values baja media alta critica)))

(deftemplate reporte-generado
   (slot paciente-id (type INTEGER)))

;;; --- SÍNTOMAS AGUDOS ---

(defrule fase-aguda-triada
   (paciente (id ?id))
   (sintoma (paciente-id ?id) (tipo fiebre-prolongada))
   (sintoma (paciente-id ?id) (tipo linfadenopatia))
   (sintoma (paciente-id ?id) (tipo faringitis))
   =>
   (assert (alerta (paciente-id ?id) (prioridad alta)
      (mensaje "Triada síndrome retroviral agudo. Solicitar antígeno p24 y carga viral."))))

(defrule fase-aguda-erupcion
   (paciente (id ?id))
   (sintoma (paciente-id ?id) (tipo fiebre-prolongada))
   (sintoma (paciente-id ?id) (tipo erupcion-cutanea))
   =>
   (assert (alerta (paciente-id ?id) (prioridad alta)
      (mensaje "Erupción maculopapular con fiebre: compatible con síndrome retroviral agudo."))))

(defrule sintomas-constitucionales
   (paciente (id ?id))
   (sintoma (paciente-id ?id) (tipo perdida-peso))
   (sintoma (paciente-id ?id) (tipo sudoracion-nocturna))
   (sintoma (paciente-id ?id) (tipo fatiga-cronica))
   =>
   (assert (alerta (paciente-id ?id) (prioridad media)
      (mensaje "Síntomas constitucionales persistentes: posible progresión estadio B o C."))))

;;; --- FACTORES DE RIESGO ---

(defrule riesgo-multiple
   (paciente (id ?id))
   (factor-riesgo (paciente-id ?id) (tipo relaciones-sin-proteccion))
   (factor-riesgo (paciente-id ?id) (tipo multiple-parejas))
   =>
   (assert (alerta (paciente-id ?id) (prioridad alta)
      (mensaje "Múltiples parejas sin protección. Tamizaje prioritario."))))

(defrule riesgo-drogas-iv
   (paciente (id ?id))
   (factor-riesgo (paciente-id ?id) (tipo uso-drogas-iv))
   =>
   (assert (alerta (paciente-id ?id) (prioridad critica)
      (mensaje "Uso de drogas IV: riesgo muy alto. Prueba inmediata y derivación a reducción de daños."))))

(defrule riesgo-ocupacional
   (paciente (id ?id))
   (factor-riesgo (paciente-id ?id) (tipo exposicion-ocupacional))
   =>
   (assert (alerta (paciente-id ?id) (prioridad critica)
      (mensaje "Exposición ocupacional: iniciar PEP dentro de las 72 horas."))))

(defrule riesgo-transfusion
   (paciente (id ?id))
   (factor-riesgo (paciente-id ?id) (tipo transfusion-sangre))
   =>
   (assert (alerta (paciente-id ?id) (prioridad media)
      (mensaje "Antecedente de transfusión: descartar transmisión por hemoderivados."))))

(defrule riesgo-perinatal
   (paciente (id ?id))
   (factor-riesgo (paciente-id ?id) (tipo madre-vih-positiva))
   =>
   (assert (alerta (paciente-id ?id) (prioridad critica)
      (mensaje "Hijo/a de madre VIH+: protocolo diagnóstico pediátrico (PCR-ADN)."))))

;;; --- SEROLOGÍA Y DIAGNÓSTICO ---

(defrule elisa-positiva-sin-confirmacion
   (paciente (id ?id))
   (prueba-laboratorio (paciente-id ?id) (tipo elisa-4ta-gen) (resultado positivo))
   (not (prueba-laboratorio (paciente-id ?id) (tipo western-blot)))
   =>
   (assert (alerta (paciente-id ?id) (prioridad alta)
      (mensaje "ELISA reactiva: solicitar Western Blot o prueba diferenciación VIH-1/VIH-2."))))

(defrule vih-confirmado
   (paciente (id ?id))
   (prueba-laboratorio (paciente-id ?id) (tipo elisa-4ta-gen) (resultado positivo))
   (prueba-laboratorio (paciente-id ?id) (tipo western-blot) (resultado positivo))
   =>
   (assert (diagnostico (paciente-id ?id) (resultado vih-confirmado)
      (nivel-riesgo confirmado) (confianza 99)
      (recomendacion "VIH CONFIRMADO. Derivar a Infectología. Solicitar CD4, carga viral, genotipado y panel metabólico."))))

(defrule western-blot-indeterminado
   (paciente (id ?id))
   (prueba-laboratorio (paciente-id ?id) (tipo western-blot) (resultado indeterminado))
   =>
   (assert (alerta (paciente-id ?id) (prioridad alta)
      (mensaje "Western Blot indeterminado: PCR-ARN urgente. Repetir serología en 4-6 semanas.")))
   (assert (diagnostico (paciente-id ?id) (resultado indeterminado)
      (nivel-riesgo incierto) (confianza 50)
      (recomendacion "Resultado indeterminado. PCR-ARN urgente. Evitar conductas de riesgo."))))

(defrule elisa-negativa-ventana
   (paciente (id ?id))
   (prueba-laboratorio (paciente-id ?id) (tipo elisa-4ta-gen) (resultado negativo))
   (factor-riesgo (paciente-id ?id) (tipo exposicion-reciente))
   =>
   (assert (alerta (paciente-id ?id) (prioridad alta)
      (mensaje "Período ventana posible: repetir prueba a las 6 semanas y 3 meses."))))

(defrule vih-descartado
   (paciente (id ?id))
   (prueba-laboratorio (paciente-id ?id) (tipo elisa-4ta-gen) (resultado negativo))
   (not (factor-riesgo (paciente-id ?id) (tipo exposicion-reciente)))
   (not (factor-riesgo (paciente-id ?id) (tipo uso-drogas-iv)))
   =>
   (assert (diagnostico (paciente-id ?id) (resultado no-vih)
      (nivel-riesgo bajo) (confianza 95)
      (recomendacion "Prueba negativa sin factores activos. Mantener prevención y repetir tamizaje anual."))))

;;; --- ESTADIFICACIÓN CDC ---

(defrule estadio-1
   ?diag <- (diagnostico (paciente-id ?id) (resultado vih-confirmado))
   (prueba-laboratorio (paciente-id ?id) (tipo conteo-cd4) (cd4 ?cd4&:(>= ?cd4 500)))
   =>
   (modify ?diag (etapa estadio-1-CDC)
      (recomendacion "Estadio 1 (CD4>=500): inmunidad preservada. Iniciar TAR. Control cada 3-6 meses.")))

(defrule estadio-2
   (prueba-laboratorio (paciente-id ?id) (tipo conteo-cd4)
      (cd4 ?cd4&:(and (>= ?cd4 200) (< ?cd4 500))))
   (diagnostico (paciente-id ?id) (resultado vih-confirmado))
   =>
   (assert (alerta (paciente-id ?id) (prioridad alta)
      (mensaje "CD4 200-499 (Estadio 2): iniciar TAR y profilaxis para infecciones oportunistas."))))

(defrule estadio-3-sida
   ?diag <- (diagnostico (paciente-id ?id) (resultado vih-confirmado))
   (prueba-laboratorio (paciente-id ?id) (tipo conteo-cd4) (cd4 ?cd4&:(< ?cd4 200)))
   =>
   (modify ?diag (resultado sida-estadio-3) (etapa estadio-3-SIDA)
      (nivel-riesgo critico) (confianza 99)
      (recomendacion "SIDA (CD4<200): TAR urgente, profilaxis cotrimoxazol, panel infecciones oportunistas."))
   (assert (alerta (paciente-id ?id) (prioridad critica)
      (mensaje "SIDA ESTADIO 3: CD4<200. Riesgo crítico. Hospitalización y TAR urgente."))))

;;; --- ENFERMEDADES DEFINITORIAS ---

(defrule neumonia-pcp
   (paciente (id ?id))
   (sintoma (paciente-id ?id) (tipo neumonia-pcp))
   (diagnostico (paciente-id ?id) (resultado vih-confirmado))
   =>
   (assert (alerta (paciente-id ?id) (prioridad critica)
      (mensaje "PCP: trimetoprim-sulfametoxazol IV. Considerar corticoides."))))

(defrule toxoplasmosis
   (paciente (id ?id))
   (sintoma (paciente-id ?id) (tipo toxoplasmosis))
   (diagnostico (paciente-id ?id) (resultado vih-confirmado))
   =>
   (assert (alerta (paciente-id ?id) (prioridad critica)
      (mensaje "Toxoplasmosis cerebral: TC/RM urgente. Pirimetamina + sulfadiazina."))))

(defrule candidiasis-esofagica
   (paciente (id ?id))
   (sintoma (paciente-id ?id) (tipo candidiasis-esofagica))
   (diagnostico (paciente-id ?id) (resultado vih-confirmado))
   =>
   (assert (alerta (paciente-id ?id) (prioridad critica)
      (mensaje "Candidiasis esofágica: fluconazol sistémico. Endoscopía si no hay respuesta."))))

(defrule sarcoma-kaposi
   (paciente (id ?id))
   (sintoma (paciente-id ?id) (tipo sarcoma-kaposi))
   (diagnostico (paciente-id ?id) (resultado vih-confirmado))
   =>
   (assert (alerta (paciente-id ?id) (prioridad critica)
      (mensaje "Sarcoma de Kaposi: Oncología + Infectología. Quimioterapia según extensión. TAR prioritario."))))

;;; --- CARGA VIRAL ---

(defrule carga-viral-indetectable
   (paciente (id ?id))
   (prueba-laboratorio (paciente-id ?id) (tipo carga-viral-pcr) (carga-viral ?cv&:(< ?cv 50)))
   (diagnostico (paciente-id ?id) (resultado vih-confirmado))
   =>
   (assert (alerta (paciente-id ?id) (prioridad baja)
      (mensaje "Carga viral <50 cop/mL (indetectable). U=U confirmado. Continuar TAR."))))

(defrule carga-viral-alta
   (paciente (id ?id))
   (prueba-laboratorio (paciente-id ?id) (tipo carga-viral-pcr) (carga-viral ?cv&:(> ?cv 100000)))
   =>
   (assert (alerta (paciente-id ?id) (prioridad critica)
      (mensaje "Carga viral >100,000 cop/mL: inicio/ajuste urgente de TAR."))))

(defrule falla-virologica
   (paciente (id ?id))
   (prueba-laboratorio (paciente-id ?id) (tipo carga-viral-pcr) (carga-viral ?cv&:(> ?cv 200)))
   (factor-riesgo (paciente-id ?id) (tipo en-tratamiento-tar))
   =>
   (assert (alerta (paciente-id ?id) (prioridad alta)
      (mensaje "Falla virológica: CV detectable bajo TAR. Evaluar adherencia, resistencias y cambio de esquema."))))

;;; --- PREVENCIÓN ---

(defrule candidato-prep
   (paciente (id ?id))
   (prueba-laboratorio (paciente-id ?id) (tipo elisa-4ta-gen) (resultado negativo))
   (factor-riesgo (paciente-id ?id) (tipo relaciones-sin-proteccion))
   (factor-riesgo (paciente-id ?id) (tipo multiple-parejas))
   =>
   (assert (alerta (paciente-id ?id) (prioridad media)
      (mensaje "Candidato a PrEP: serología negativa con alto riesgo. Indicar tenofovir/emtricitabina."))))

(defrule its-activa
   (paciente (id ?id))
   (sintoma (paciente-id ?id) (tipo its-activa))
   (not (diagnostico (paciente-id ?id) (resultado vih-confirmado)))
   =>
   (assert (alerta (paciente-id ?id) (prioridad alta)
      (mensaje "ITS activa: riesgo VIH aumentado x10. Tamizaje VIH obligatorio."))))

;;; --- REPORTE FINAL ---

(defrule reporte-final
   (paciente (id ?id) (nombre ?nombre))
   (diagnostico (paciente-id ?id) (resultado ?res) (nivel-riesgo ?riesgo) (recomendacion ?rec))
   (not (reporte-generado (paciente-id ?id)))
   =>
   (assert (reporte-generado (paciente-id ?id)))
   (printout t crlf
      "======================================================" crlf
      "       SISTEMA EXPERTO VIH — REPORTE FINAL           " crlf
      "======================================================" crlf
      " Paciente    : " ?nombre crlf
      " ID          : " ?id crlf
      " Resultado   : " ?res crlf
      " Nivel riesgo: " ?riesgo crlf
      " Recomendacion: " ?rec crlf
      "======================================================" crlf))

;;; ============================================================
;;;  CASOS DE PRUEBA (descomentar uno a la vez, luego (reset)(run))
;;; ============================================================

;;; CASO 1 — VIH confirmado con SIDA
(deffacts caso-1
(paciente (id 1) (nombre "Juan Perez") (edad 34) (sexo masculino))
(factor-riesgo (paciente-id 1) (tipo relaciones-sin-proteccion))
(factor-riesgo (paciente-id 1) (tipo multiple-parejas))
(sintoma (paciente-id 1) (tipo fiebre-prolongada))
(sintoma (paciente-id 1) (tipo perdida-peso))
(sintoma (paciente-id 1) (tipo sudoracion-nocturna))
(prueba-laboratorio (paciente-id 1) (tipo elisa-4ta-gen) (resultado positivo))
(prueba-laboratorio (paciente-id 1) (tipo western-blot) (resultado positivo))
(prueba-laboratorio (paciente-id 1) (tipo conteo-cd4) (cd4 150))
(prueba-laboratorio (paciente-id 1) (tipo carga-viral-pcr) (carga-viral 250000)))

;;; CASO 2 — Candidato a PrEP
;; (deffacts caso-2
;;    (paciente (id 2) (nombre "Maria Garcia") (edad 28) (sexo femenino))
;;    (factor-riesgo (paciente-id 2) (tipo relaciones-sin-proteccion))
;;    (factor-riesgo (paciente-id 2) (tipo multiple-parejas))
;;    (prueba-laboratorio (paciente-id 2) (tipo elisa-4ta-gen) (resultado negativo)))

;;; CASO 3 — Exposición ocupacional (PEP urgente)
;; (deffacts caso-3
;;    (paciente (id 3) (nombre "Carlos Lima") (edad 41) (sexo masculino))
;;    (factor-riesgo (paciente-id 3) (tipo exposicion-ocupacional))
;;    (prueba-laboratorio (paciente-id 3) (tipo elisa-4ta-gen) (resultado negativo))
;;    (factor-riesgo (paciente-id 3) (tipo exposicion-reciente)))
