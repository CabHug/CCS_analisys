class NormalMap:
    def __init__(self):        
        self.professions_map = {
            # --- SALUD: ENFERMERÍA Y AUXILIARES ---
            "Auxiliar de enfermería": [
                "Auxiliar de enfermería",
                "Aux de enfermeria",
                "Aux enfermeria",
                "Aux. enfermeria",
                "Auxiliar de enefermeria",
                "Auxiliar de enfermer",
                "Auxiliar de enfermeria",
                "Enfermer@",
                "Enfermera",
                "Enfermera (o)",
                "Enfermero",
                "Auxiliar en salud"
            ],
            "Jefe de enfermería": [
                "Jefe de enfermería",
                "Enferemera jefe",
                "Enfermera jefe",
                "Enfermero jefe",
                "Jefe de enfermeria",
                "Jefe de urgencias"
            ],

            # --- SALUD: MEDICINA ---
            "Médico general": [
                "Médico general",
                "Medic@",
                "Medica",
                "Medica ",
                "Medica general",
                "Medico",
                "Medico ",
                "Medico general"
            ],
            "Médico especialista": [
                "Médico especialista",
                "Oncologo",
                "Ortopedista",
                "Cirujano",
                "Dermocosmiatra",
                "Gerontologo",
                "Ginecologia y obstetrica",
                "Ginecologo y obstetra",
                "Hematologo",
                "Infectologia pediatra",
                "Internista",
                "Medica anestesiologa",
                "Medico cirujano",
                "Medico especialista",
                "Medico familiar",
                "Medico internista",
                "Fonoaudiologa",
                "Ginecologa",
                "Ginecologo",
                "Oftalmologa",
                "Pediatra",
                "Anestesiologa",
                "Ginecolog@"
            ],

            # --- SALUD: ODONTOLOGÍA ---
            "Odontólogo general": [
                "Odontólogo general",
                "Odontologa",
                "Odontologo",
                "Odontologo ",
                "Odontolog@"
            ],
            "Odontólogo especialista": [
                "Ortodoncista"
            ],
            "Auxiliar de odontología": [
                "Auxiliar de odontologia",
                "Auxiliar en salud oral",
                "Tecnico en salud oral",
                "Auxiliar odontologa",
                "Higienista oral",
                "Auxiliar de higiene oral"
            ],

            # --- SALUD: FARMACIA ---
            "Regente de farmacia": [
                "Regente de farmacia",
                "Regente de farmacia ",
                "Regentede farmacia",
                "Tecnologa en regencia de farmacia"
            ],
            "Auxiliar de farmacia": [
                "Auxiliar de farmacia",
                "Auxiliar en servicios farmaceuticos",
                "Vendedor de medicamentos",
                "Vendedor farmacia"
            ],
            "Químico farmacéutico": [
                "Quimico farmaceutico"
            ],

            # --- SALUD: LABORATORIO Y DIAGNÓSTICO ---
            "Bacteriólogo/Microbiólogo": [
                "Bacteriólogo/Microbiólogo",
                "Bactereologo",
                "Bacteriologa",
                "Bacteriologo",
                "Bacterióloga",
                "Bacteriolog@",
                "Microbiologo"
            ],
            "Técnico de laboratorio clínico": [
                "Técnico de laboratorio clínico",
                "Aux. laboraorio",
                "Auxiliar de laboratorio clínico",
                "Auxiliar de laboratorio",
                "Citohistologa."
            ],
            "Técnico en radiología": [
                "Técnico en radiología",
                "Tecnico en radiologia",
                "Tecnologa en radiodiagnostico y radioterapia ",
                "Tecnología en radiodiagnóstico y radioterapia",
                "Tecnologa en radiologia",
                "Tecnologa en imagenologia",
                "Tecnologa en imágenes diagnosticas",
                "Tecnico en radiodiagnostico",
                "Tecnologa en imágenes diagnósticas",
                "Tecnologo en radiodiagnostico"
            ],

            # --- SALUD: TERAPIAS Y PSICOLOGÍA ---
            "Psicólogo": [
                "Psicólogo",
                "Psicolog@",
                "Psicologa",
                "Psicologo",
                "Pricolog@"
            ],
            "Fisioterapeuta": [
                "Fisioterapeuta"
            ],
            "Terapeuta respiratorio": [
                "Terapeuta respiratorio"
            ],
            "Terapeuta ocupacional": [
                "Terapeuta ocupacional"
            ],
            "Fonoaudiólogo": [
                "Fonoaudilog@"
            ],
            "Nutricionista": [
                "Nutricionista",
                "Nutricionista dietista",
                "Nutricionista y dietista",
                "Nuticionista",
                "Nutricionista y dietetica"
            ],
            "Optómetra": [
                "Optometra"
            ],
            "Trabajador social en salud": [
                "Trabajador social en salud",
                "Trabajadora social",
                "Trabajo social"
            ],

            # --- SALUD: ATENCIÓN PREHOSPITALARIA Y OTROS ---
            "Tecnólogo en atención prehospitalaria": [
                "Tecnólogo en atención prehospitalaria",
                "Camillero",
                "Conductor",
                "Conductor de ambulancia",
                "Conductor de vehiculos",
                "Tecnico profesional en atención prehospitalaria",
                "Socorrista",
                "Tecnico en apoyo de emergencias"
            ],
            "Instrumentador quirúrgico": [
                "Instrumentador quirúrgico",
                "Instrumentador",
                "Instrumentador quirugico",
                "Instrumentador quirurjico",
                "Instrumentadora",
                "Instrumentadora quirúrgica"
            ],
            "Promoción y Gestión en Salud": [
                "Promotora en salud",
                "Gestora comunitaria",
                "Tecnologo en promoción de la salud",
                "Tecnologo en promocion"
            ],
            "Estudiante": [
                "Estudiante",
                "Estudiante de farmacia",
                "Estudiante de medicina",
                "Estudiante de optometria"
            ],

            # --- ADMINISTRATIVO Y CONTABLE ---
            "Auxiliar administrativo": [
                "Auxiliar administrativo",
                "Auxiliar de cartera",
                "Auxiliar administrativo en salud",
                "Facturacion",
                "Auxiliar de facturacion",
                "Tecnica en administracion de emp",
                "Recepcionista",
                "Callcenter",
                "Coordinador de desarrollo",
                "Tecnico en administracion en salud"
            ],
            "Administrador de empresas": [
                "Administrador de empresas",
                "Administradora de empresas",
                "Admin de empresas",
                "Admon de empresas",
                "Administrador de negocios internacionales"
            ],
            "Contador público": [
                "Contador publico",
                "Contador",
                "Contadora"
            ],
            "Administrador público": [
                "Administradora publica",
                "Administrador publico"
            ],

            # --- INGENIERÍAS ---
            "Ingeniería de Sistemas y Electrónica": [
                "Tecnico en sistemas",
                "Ingeniero de sistemas",
                "Ing de sistemas",
                "Tecnico integral en sistemas",
                "Ingeniero electronico",
                "Ingeniera electronica",
                "Ing mecatronico"
            ],
            "Ingeniería Industrial": [
                "Ingeniero industrial"
            ],
            "Ingeniería Ambiental y Agroforestal": [
                "Ingeniera agroforesteal",
                "Ingeniero agroforestal",
                "Ingeniera ambiental"
            ],
            "Ingeniería Biomédica": [
                "Biomedico",
                "Ingeniero biomedico"
            ],
            "Ingeniero (Genérico)": [
                "Ingeniero"
            ],

            # --- DERECHO Y SOCIALES ---
            "Abogado": [
                "Abogado",
                "Abogada",
                "Abogad@"
            ],
            "Comunicador social": [
                "Comunicardor social"
            ],
            "Antropólogo": [
                "Antropologa"
            ],

            # --- EDUCACIÓN Y DEPORTE ---
            "Docente": [
                "Docente",
                "Etnoeducadora",
                "Orientador",
                "Atencion integral en primer infancia"
            ],
            "Educación Física y Deporte": [
                "Licenciado en educacion fisica",
                "Tecnico en preparacion fisica",
                "Preparador fisico",
                "Educador fisico"
            ],

            # --- OFICIOS Y OTROS ---
            "Esteticista": [
                "Esteticista",
                "Micropigmentadora",
                "Masajista"
            ],
            "Servicios generales": [
                "Auxiliar de servicios generales",
                "Servicios generales",
                "Op.ss.gg limpieza",
                "Tecnico hoteleria y servicios generales"
            ],
            "Vigilante": [
                "Vigilante"
            ],
            "Independiente": [
                "Independiente",
                "Comerciante",
                "Emprendedora"
            ],
            "Mercaderista": [
                "Mercaderista"
            ],
            "Conductor": [
                "Operados de vehiculos"
            ],
            "Seguridad y Salud en el Trabajo (SST)": [
                "Administradora en ss-t",
                "Coordinadora sst"
            ],
            "Logística": [
                "Distribuidora de med. bodega",
                "Apoyo logistico"
            ],
            "Zootecnista": [
                "Zootecnista"
            ],
            "Quiropráctico": [
                "Quiropractico"
            ],
            "Electricista": [
                "Tec. electrisista"
            ],
            "Técnico/Tecnólogo (Genérico)": [
                "Tecnologo",
                "Tecnico"
            ],
            "Empleado": [
                "Empleado",
                "Empleada"
            ],
            "Ama de casa": [
                "Ama de casa"
            ],
            "Bachiller": [
                "Bachiller"
            ],
            "Otros": [
                " físico matemático meteorólogo y entrenador"
            ]
        }

        self.created_by_map = {
                "Sebastian": [
                    "Bancolombia","Sebas"
                ],
                "Camilo": [
                    "Cami"
                ],
                "Nicolas": [
                    "Nico"
                ]
            }

        self.salesperson_map = {
                "Brayan": [
                    "Barayan","Bryan","<"
                ],
                "Francisco": [
                    "Franciso"
                ],
                "H. San Pedro": [
                    "San Pedro"
                ],
                "Nicolas": [
                    "Nico"
                ],
                "Sebastian": [
                    "Sebas"
                ]
            }

        self.payment_method_map = {
                "Nequi": [
                    "Nequi  ", "Nequi/Bancolombia", "I Nequi/Bancolombia"
                ],
                "Pendiente": [
                    "Debe 55","Debe45","Pendiente","Por Cancelar","Por Pagar",
                    "Saldo 40","Saldo 50","Temp","Temporal","Verificar"
                ],
                "Caja": [
                    "Efectivo","Efectivo "
                ],
                "Obsequio": [
                    "Obsequi"
                ]
            }

        self.modalidad_map = {
            "Actualizacion": [
                "Renovacion","Renovación" ],
            "Capacitación": [
                "Capacitacion", "Colaborador", "Temporal"]
            }

        self.courses_map = {
            # --- Llaves Originales Solicitadas ---
            "Acls": [
                "Acls"
            ],
            "Aclsn": [
                "Aclsn"
            ],
            "Admon de medicamentos": [
                "Admon de medicamentos"
            ],
            "Adulto mayor": [
                "Adulto mayor"
            ],
            "Aiepi": [
                "Aiepi"
            ],
            "Atención pre-hospitalaria": [
                "Atención pre-hospitalaria",
                "Mision medica"  # Relacionado con transporte/atención externa
            ],
            "Bls": [
                "Bls",
                "Rcp" # RCP suele ser parte de BLS, si prefieres separado, muévelo a una nueva llave
            ],
            "Brigada": [
                "Brigada",
                "Comando de incidentes"
            ],
            "Camillero": [
                "Camillero"
            ],
            "Citología": [
                "Citologia"
            ],
            "Clínica de heridas": [
                "Clínica de heridas",
                "Manejo de heridas"
            ],
            "Código verde": [
                "Código verde"
            ],
            "Conflicto armado": [
                "Conflicto armado"
            ],
            "Discapacidad": [
                "Discapacidad",
                "Atencion a personas con discapacidad",
                "Discapacidad de riesgos"
            ],
            "Donante": [
                "Donante",
                "Cuidado al paciente donante"
            ],
            "Duelo": [
                "Duelo"
            ],
            "Humanización": [
                "Humanización",
                "Humanizacion",
                "Atencion al cliente", # Relacionado con trato humano
                "Atencion al usuario"
            ],
            "Iami": [
                "Iami",
                "Lactante",
                "Plan decenal de lactancia materna y alimentación complementaria",
                "Neonatal", # Agrupado aquí por afinidad materno-infantil
                "Desnutricion"
            ],
            "Igualdad de género": [
                "Igualdad de género",
                "Igualdad de genero",
                "Lgbti"
            ],
            "Implante": [
                "Implante"
            ],
            "Manejo defensivo": [
                "Manejo defensivo",
                "Seguridad vial"
            ],
            "Manipulación de alimentos": [
                "Manipulación de alimentos",
                "Manipulacion",
                "Manipulacion de alimentos"
            ],
            "Ove": [
                "Ove"
            ],
            "Paciente": [
                "Paciente",
                "Adulto" # "Adulto" a secas suele referirse al paciente adulto general
            ],
            "Pai": [
                "Pai",
                "Vacunacion" # PAI es el programa de vacunación
            ],
            "Paliativos": [
                "Paliativos"
            ],
            "Poct": [
                "Poct"
            ],
            "Primeros auxilios": [
                "Primeros auxilios",
                "Primer respondiente",
                "Primeros auxilios para conductor de emergencias",
                "Stop the bleed"
            ],
            "Primeros auxilios p": [
                "Primeros auxilios p" # Generalmente Psicológicos
            ],
            "Químicos": [
                "Químicos",
                "Quimicos",
                "Sustancias"
            ],
            "Residuos": [
                "Residuos"
            ],
            "Salud mental": [
                "Salud mental",
                "Consumo", # Refiriéndose a consumo de sustancias/salud mental
                "Tabaco"
            ],
            "Toma de muestras": [
                "Toma de muestras"
            ],
            "Uci": [
                "Uci"
            ],
            "Violencia de género": [
                "Violencia de género",
                "Violencia de genero"
            ],
            "Violencia sexual": [
                "Violencia sexual"
            ],

            # --- Nuevas Llaves Creadas (No estaban en tu lista original) ---
            "Atención Primaria (PyP)": [
                "Aps",
                "Atencion primaria",
                "Pyp",
                "Pym"
            ],
            "Buenas Prácticas": [
                "Buenas practicas"
            ],
            "Código Rojo": [
                "Codigo rojo",
                "Codigo rojo y emergencias"
            ],
            "Consulta Externa": [
                "Consulta externa"
            ],
            "Covid": [
                "Covid"
            ],
            "Dea": [
                "Dea",
                "Uso y manejo del dea"
            ],
            "Exógena": [
                "Exogena"
            ],
            "Lavado de manos": [
                "Lavado de manos"
            ],
            "Liderazgo": [
                "Perfeccionamiento de liderazgo básico"
            ],
            "Pals": [
                "Pals" # Pediatric Advanced Life Support (Distinto a ACLS)
            ],
            "Radioprotección": [
                "Radioproteccion",
                "Radiologica"
            ],
            "Salvamento Acuático": [
                "Salvamento acuatico",
                "Salvamento acuatico "
            ],
            "Triage": [
                "Triage"
            ],
            "Vectores": [
                "Vectores"
            ]
        }
        


        