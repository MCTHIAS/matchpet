class DominioException(Exception):
    """Classe base para exceções de regras de negócio."""
    pass

class ConcorrenciaSolicitacaoException(DominioException):
    """Lançada quando ocorre uma race condition (bloqueio otimista) ao atualizar uma solicitação."""
    pass

class TransicaoStatusInvalidaException(DominioException):
    """Lançada quando um fluxo de estado não permitido é tentado."""
    pass

class RegraNegocioException(DominioException):
    """Lançada quando uma validação de entidade ou regra corporativa falha."""
    pass