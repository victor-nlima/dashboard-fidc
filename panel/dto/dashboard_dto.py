
# Exemplo de saída dados. Deve ser ajustado após definicaos dos dados que serao exibidos.

class DashboardDTO:
  def __init__(self, id, creation_date,info=None):
    self.id = id
    self.creation_date = creation_date
    self.info = info

  def to_dict(self):
    return {
      "id": self.id,
      "creation_date": self.creation_date,
      "info": self.info
    }