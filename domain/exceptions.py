class DominioException(Exception):
    """Excecao base para violacoes de regras de negocio empresariais."""
    pass


class ConcorrenciaSolicitacaoException(DominioException):
    """Lancada quando outra transacao altera o estado da solicitacao simultaneamente."""
    pass


class TransicaoStatusInvalidaException(DominioException):
    """Lancada quando uma mudanca de estado viola o ciclo de vida definido no dominio."""
    pass


class RegraNegocioException(DominioException):
    """Lancada quando invariantes obrigatorios de uma entidade nao sao atendidos."""
    pass