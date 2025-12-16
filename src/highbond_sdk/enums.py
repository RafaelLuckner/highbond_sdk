
from enum import Enum

"""
Enumerações para o HighBond SDK.

NOTA IMPORTANTE:
A maioria dos campos da API HighBond utiliza strings configuráveis no project type,
não valores fixos. Os valores abaixo são EXEMPLOS comuns que podem variar de acordo
com a configuração da sua organização. Sempre verifique as opções disponíveis no
seu project type específico.
"""

# Adiciona enum faltante para documentação automática
class ObjectiveType(str, Enum):
    """Tipos possíveis de objetivo."""
    STRATEGIC = "strategic"
    OPERATIONAL = "operational"
    COMPLIANCE = "compliance"
    FINANCIAL = "financial"

# Adiciona enums faltantes para documentação automática
class ProjectState(str, Enum):
    """Estados possíveis de um projeto."""
    ACTIVE = "active"
    ARCHIVED = "archived"
    DRAFT = "draft"
    CLOSED = "closed"

class ProjectStatus(str, Enum):
    """Status possíveis de um projeto."""
    ON_TRACK = "on_track"
    AT_RISK = "at_risk"
    OFF_TRACK = "off_track"
    COMPLETED = "completed"


class Region(str, Enum):
    """Regiões disponíveis da API HighBond.
    
    Use estes valores para configurar a região correta:
    - US: Estados Unidos
    - EU: Europa  
    - AU: Austrália
    - CA: Canadá
    - SA: América do Sul
    """
    
    US = "us"
    EU = "eu"
    AU = "au"
    CA = "ca"
    SA = "sa"
    
    @classmethod
    def get_base_url(cls, region: "Region") -> str:
        """Retorna a URL base para a região."""
        if region == cls.SA:
            return "https://apis-sa.diligentoneplatform.com/v1"
        return f"https://apis-{region.value}.highbond.com/v1"


# ====================================================================
# EXEMPLOS DE VALORES COMUNS
# ====================================================================
# Os valores abaixo são exemplos. Verifique as opções configuradas
# no seu project type específico.
# ====================================================================

# Exemplos de valores para campo 'deficiency_type' em Issues:
# - "Deficiency"
# - "Significant Deficiency"
# - "Material Weakness"
# - "Best Practice"
# - "Observation"

# Exemplos de valores para campo 'severity' em Issues/Risks:
# - "High"
# - "Medium"  
# - "Low"
# - "Critical"

# Exemplos de valores para campo 'impact'/'likelihood' em Risks:
# - "High"
# - "Medium"
# - "Low"
# - "Very High"
# - "Very Low"

# Exemplos de valores para campo 'frequency' em Controls:
# - "Daily"
# - "Weekly"
# - "Monthly"
# - "Quarterly"
# - "Annually"
# - "As Needed"
# - "Semi-annually"

# Exemplos de valores para campo 'control_type' em Controls:
# - "Application/System Control"
# - "Manual Control"
# - "IT Dependent Manual Control"

# Exemplos de valores para campo 'prevent_detect' em Controls:
# - "Prevent"
# - "Detect"
# - "N/A"

# Exemplos de valores para campo 'method' em Controls:
# - "Management Review"
# - "Observation"
# - "Inquiry"
# - "Inspection"
# - "Recalculation"
# - "Reperformance"

# Exemplos de valores para campo 'status' em Controls:
# - "Key Control"
# - "Not Key Control"

# Exemplos de valores para campo 'remediation_status' em Issues:
# - "Opened"
# - "In Progress"
# - "Closed"
# - "Pending Verification"

from enum import Enum

"""
Enumerações para o HighBond SDK.

NOTA IMPORTANTE:
A maioria dos campos da API HighBond utiliza strings configuráveis no project type,
não valores fixos. Os valores abaixo são EXEMPLOS comuns que podem variar de acordo
com a configuração da sua organização. Sempre verifique as opções disponíveis no
seu project type específico.
"""

# Adiciona enum faltante para documentação automática
# Exemplos de valores para campo 'scope' em Issues:
# - "Local"
# - "Regional"
# - "Enterprise"

# Exemplos de valores para campo 'escalation' em Issues:
# - "Owner"
# - "Manager"
# - "Director"
# - "Executive"
# - "Board"


class SortOrder(str, Enum):
    """Ordem de classificação."""
    
    ASC = "asc"
    DESC = "desc"
