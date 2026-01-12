"""
Módulo de Actions (Ações) para o HighBond SDK.
"""
from typing import Optional, Dict, Any, List

from ..http_client import HighBondHTTPClient, PaginationMixin, ThreadingMixin
from ..config import PaginationConfig, ThreadingConfig
from ..utils import to_dataframe


class ActionsModule(PaginationMixin, ThreadingMixin):
    """Módulo para gerenciamento de Ações no HighBond.
    
    Ações representam tarefas, acompanhamentos e remediações relacionadas
    a issues (deficiências, achados de auditoria).
    
    IMPORTANTE: Ações são sempre criadas dentro de uma issue e acessadas
    através do endpoint /orgs/{org_id}/issues/{issue_id}/actions.
    """
    
    def __init__(
        self,
        http_client: HighBondHTTPClient,
        org_id: int,
        pagination_config: PaginationConfig,
        threading_config: ThreadingConfig
    ):
        """
        Args:
            http_client: Cliente HTTP configurado.
            org_id: ID da organização.
            pagination_config: Configuração de paginação.
            threading_config: Configuração de threading.
        """
        self._http_client = http_client
        self._org_id = org_id
        self._pagination_config = pagination_config
        self._threading_config = threading_config
    
    def _action_base_endpoint(self, action_id: int) -> str:
        """Endpoint para acessar ação por ID (para GET, PATCH, DELETE)."""
        return f"/orgs/{self._org_id}/actions/{action_id}"
    
    def _issue_actions_endpoint(self, issue_id: int) -> str:
        """Endpoint para listar e criar ações em uma issue."""
        return f"/orgs/{self._org_id}/issues/{issue_id}/actions"
    
    def _project_endpoint(self, project_id: int) -> str:
        """Endpoint base para issues de um projeto."""
        return f"/orgs/{self._org_id}/projects/{project_id}/issues"
    
    @property
    def _org_endpoint(self) -> str:
        """Endpoint base para issues a nível de organização."""
        return f"/orgs/{self._org_id}/issues"
    
    # ==================== LISTAGEM ====================
    
    def list_all(
        self,
        include: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None,
        max_pages: Optional[int] = None,
        return_pandas: bool = False
    ) -> List[Dict[str, Any]]:
        """Lista todas as ações da organização com paginação automática.
        
        Busca todas as issues da organização e depois todas as ações de cada issue,
        utilizando multithreading para otimização.
        
        Args:
            include: Relacionamentos para incluir.
            filters: Filtros adicionais.
            max_pages: Máximo de páginas a buscar (None = todas).
            return_pandas: Se True, retorna um DataFrame; se False, retorna uma lista.
            
        Returns:
            Lista de ações ou DataFrame.
            
        Example:
            >>> actions = client.actions.list_all()
            >>> print(f"Total de ações na org: {len(actions)}")
        """
        # Buscar todas as issues da organização
        pagination = PaginationConfig(
            page_size=self._pagination_config.page_size,
            max_pages=max_pages or self._pagination_config.max_pages
        )
        
        params = {}
        if include:
            params["include"] = ",".join(include)
        if filters:
            for key, value in filters.items():
                params[f"filter[{key}]"] = value
        
        issues = list(self._paginate(self._org_endpoint, pagination, params))
        issue_ids = [issue['id'] for issue in issues]
        
        if not issue_ids:
            # Se não houver issues, retornar vazio
            return [] if not return_pandas else to_dataframe([])
        
        # Buscar ações de todas as issues em paralelo
        def fetch_actions_for_issue(issue_id):
            return self.list_by_issue(issue_id, include=include, filters=filters, return_pandas=False)
        
        all_actions = self._execute_parallel(
            fetch_actions_for_issue,
            issue_ids,
            self._threading_config
        )
        
        # Flatten lista de listas
        actions = []
        for action_list in all_actions:
            if isinstance(action_list, list):
                actions.extend(action_list)
        
        if return_pandas:
            return to_dataframe(actions)
        return actions
    
    def list_by_project(
        self,
        project_id: int,
        include: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None,
        max_pages: Optional[int] = None,
        return_pandas: bool = False
    ) -> List[Dict[str, Any]]:
        """Lista todas as ações de um projeto com paginação automática.
        
        Busca todas as issues do projeto e depois todas as ações de cada issue,
        utilizando multithreading para otimização.
        
        Args:
            project_id: ID do projeto.
            include: Relacionamentos para incluir.
            filters: Filtros adicionais.
            max_pages: Máximo de páginas a buscar (None = todas).
            return_pandas: Se True, retorna um DataFrame; se False, retorna uma lista.
            
        Returns:
            Lista de ações ou DataFrame.
            
        Example:
            >>> actions = client.actions.list_by_project(project_id=546355)
            >>> print(f"Total de ações no projeto: {len(actions)}")
        """
        # Buscar todas as issues do projeto
        pagination = PaginationConfig(
            page_size=self._pagination_config.page_size,
            max_pages=max_pages or self._pagination_config.max_pages
        )
        
        params = {}
        if include:
            params["include"] = ",".join(include)
        if filters:
            for key, value in filters.items():
                params[f"filter[{key}]"] = value
        
        issues = list(self._paginate(
            self._project_endpoint(project_id), pagination, params
        ))
        issue_ids = [issue['id'] for issue in issues]
        
        if not issue_ids:
            # Se não houver issues, retornar vazio
            return [] if not return_pandas else to_dataframe([])
        
        # Buscar ações de todas as issues em paralelo
        def fetch_actions_for_issue(issue_id):
            return self.list_by_issue(issue_id, include=include, filters=filters, return_pandas=False)
        
        all_actions = self._execute_parallel(
            fetch_actions_for_issue,
            issue_ids,
            self._threading_config
        )
        
        # Flatten lista de listas
        actions = []
        for action_list in all_actions:
            if isinstance(action_list, list):
                actions.extend(action_list)
        
        if return_pandas:
            return to_dataframe(actions)
        return actions
    
    def list_by_issue(
        self,
        issue_id: int,
        include: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None,
        max_pages: Optional[int] = None,
        return_pandas: bool = False
    ) -> List[Dict[str, Any]]:
        """Lista todas as ações de uma issue com paginação automática.
        
        Args:
            issue_id: ID da issue.
            include: Relacionamentos para incluir.
            filters: Filtros adicionais.
            max_pages: Máximo de páginas a buscar (None = todas).
            return_pandas: Se True, retorna um DataFrame; se False, retorna uma lista.
            
        Returns:
            Lista de ações ou DataFrame.
            
        Example:
            >>> actions = client.actions.list_by_issue(issue_id=999)
            >>> print(f"Total de ações: {len(actions)}")
        """
        pagination = PaginationConfig(
            page_size=self._pagination_config.page_size,
            max_pages=max_pages or self._pagination_config.max_pages
        )
        
        params = {}
        if include:
            params["include"] = ",".join(include)
        if filters:
            for key, value in filters.items():
                params[f"filter[{key}]"] = value
        
        actions = list(self._paginate(
            self._issue_actions_endpoint(issue_id), pagination, params
        ))
        
        if return_pandas:
            return to_dataframe(actions)
        return actions
    
    # ==================== OBTENÇÃO ====================
    
    def get(
        self,
        action_id: int,
        include: Optional[List[str]] = None,
        return_pandas: bool = False
    ) -> Dict[str, Any]:
        """Obtém uma ação específica por ID.
        
        Args:
            action_id: ID da ação.
            include: Relacionamentos para incluir.
            return_pandas: Se True, retorna um DataFrame; se False, retorna um dict.
            
        Returns:
            Dados da ação ou DataFrame.
            
        Example:
            >>> action = client.actions.get(123)
            >>> print(action['data']['attributes']['title'])
        """
        endpoint = self._action_base_endpoint(action_id)
        params = {}
        
        if include:
            params["include"] = ",".join(include)
        
        response = self._http_client.get(endpoint, params if params else None)
        
        if return_pandas:
            data = response.get('data', {})
            return to_dataframe([data] if isinstance(data, dict) else data)
        return response
    
    def get_many(
        self,
        action_ids: List[int],
        include: Optional[List[str]] = None,
        return_pandas: bool = False
    ) -> List[Dict[str, Any]]:
        """Obtém múltiplas ações em paralelo.
        
        Args:
            action_ids: Lista de IDs de ações.
            include: Relacionamentos para incluir.
            return_pandas: Se True, retorna um DataFrame; se False, retorna uma lista.
            
        Returns:
            Lista de ações ou DataFrame.
            
        Example:
            >>> actions = client.actions.get_many([1, 2, 3])
            >>> for action in actions:
            ...     print(action['data']['attributes']['title'])
        """
        def fetch_action(aid):
            return self.get(aid, include=include, return_pandas=False)
        
        actions = self._execute_parallel(
            fetch_action,
            action_ids,
            self._threading_config
        )
        
        if return_pandas:
            return to_dataframe(actions)
        return actions
    
    def get_many_by_issue(
        self,
        issue_id: int,
        max_actions: Optional[int] = None,
        include: Optional[List[str]] = None,
        return_pandas: bool = False
    ) -> List[Dict[str, Any]]:
        """Obtém múltiplas ações de uma issue em paralelo.
        
        Busca todas as ações de uma issue com otimização por multithreading
        para cada ação individual via endpoint `/orgs/{org_id}/actions/{id}`.
        
        Args:
            issue_id: ID da issue.
            max_actions: Número máximo de ações a buscar (None = todas).
            include: Relacionamentos para incluir.
            return_pandas: Se True, retorna um DataFrame; se False, retorna uma lista.
            
        Returns:
            Lista de ações ou DataFrame.
            
        Example:
            >>> actions = client.actions.get_many_by_issue(issue_id=999)
            >>> print(f"Total de ações da issue: {len(actions)}")
        """
        # Primeiro, listar todas as ações da issue (minimal)
        actions_list = self.list_by_issue(
            issue_id=issue_id,
            include=None,
            return_pandas=False
        )
        
        if not actions_list:
            return [] if not return_pandas else to_dataframe([])
        
        # Limitar se necessário
        if max_actions is not None:
            actions_list = actions_list[:max_actions]
        
        # Buscar cada ação em paralelo com detalhes completos
        action_ids = [action['id'] for action in actions_list]
        detailed_actions = self.get_many(
            action_ids=action_ids,
            include=include,
            return_pandas=False
        )
        
        if return_pandas:
            return to_dataframe(detailed_actions)
        return detailed_actions
    
    


    # ==================== DELEÇÃO ====================

    def delete(self, action_id: int) -> Dict[str, Any]:
        """Deleta uma ação.
        
        Ações são deletadas através do endpoint `/orgs/{org_id}/actions/{id}`.
        
        Args:
            action_id: ID da ação a deletar (obrigatório).
            
        Returns:
            Resposta da API.
            
        Example:
            >>> response = client.actions.delete(123)
            >>> print("Ação deletada com sucesso")
        """
        endpoint = self._action_base_endpoint(action_id)
        return self._http_client.delete(endpoint)
