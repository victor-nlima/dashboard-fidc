from typing import List, Dict, Optional
from abc import ABC, abstractmethod

from panel.dto.dashboard_dto import DashboardDTO

# exemplo de classe abstrata para criacao do métodos de consulta ao banco. Os retornos sao baseados no dto

class AbstractDashboardRepository(ABC):
    

    # @abstractmethod
    # def get_by_id(self) -> Optional[DashboardDTO]:
    #     """Listar registros de Financial Instrument"""
    #     pass

    def get_date(self) -> Optional[DashboardDTO]:
        pass

    @abstractmethod
    def create_data(self,data):
        pass