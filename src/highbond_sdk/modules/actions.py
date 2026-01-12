"""
Módulo de Actions (Ações) para o HighBond SDK.
"""
from typing import Optional, Dict, Any, List

from ..http_client import HighBondHTTPClient, PaginationMixin, ThreadingMixin
from ..config import PaginationConfig, ThreadingConfig
from ..utils import to_dataframe


class ActionsModule(PaginationMixin, ThreadingMixin):
    """Módulo para gerenciamento de Actions (Ações) no HighBond.
    
    Actions representam ações ou tarefas de remediação associadas a issues/findings,
    usadas para rastrear e gerenciar as atividades necessárias para resolver problemas identificados.
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
    
    @property
    def _org_endpoint(self) -> str:
        """Endpoint base para actions a nível de organização."""
        return f"/orgs/{self._org_id}/actions"
    
    def _issue_endpoint(self, issue_id: int) -> str:
        """Endpoint base para actions de uma issue."""
        return f"/orgs/{self._org_id}/issues/{issue_id}/actions"
    
    # ==================== LISTAGEM ====================
    
    def list_all(
        self,
        include: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None,
        max_pages: Optional[int] = None,
        return_pandas: bool = False
    ) -> List[Dict[str, Any]]:
        """Lista todas as actions da organização com paginação automática.
        
        Args:
            include: Relacionamentos para incluir.
            filters: Filtros adicionais.
            max_pages: Máximo de páginas a buscar.
            return_pandas: Se True, retorna um DataFrame; se False, retorna uma lista.
            
        Returns:
            Lista de actions ou DataFrame.
            
        Example:
            >>> for action in client.actions.list_all():
            ...     print(action['attributes']['title'])
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
        
        actions = list(self._paginate(self._org_endpoint, pagination, params))
        
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
        """Lista todas as actions de uma issue com paginação automática.
        
        Args:
            issue_id: ID da issue.
            include: Relacionamentos para incluir.
            filters: Filtros adicionais.
            max_pages: Máximo de páginas.
            return_pandas: Se True, retorna um DataFrame; se False, retorna uma lista.
            
        Returns:
            Lista de actions ou DataFrame.
            
        Example:
            >>> actions = client.actions.list_by_issue(issue_id=999)
            >>> for action in actions:
            ...     print(action['attributes']['title'])
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
            self._issue_endpoint(issue_id), pagination, params
        ))
        
        if return_pandas:
            return to_dataframe(actions)
        return actions
    
    def list_by_project(
        self,
        project_id: int,
        include: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None,
        return_pandas: bool = False
    ) -> List[Dict[str, Any]]:
        """Lista todas as actions de um projeto (buscando todas as issues e suas actions).
        
        Args:
            project_id: ID do projeto.
            include: Relacionamentos para incluir.
            filters: Filtros adicionais.
            return_pandas: Se True, retorna um DataFrame; se False, retorna uma lista.
            
        Returns:
            Lista de actions do projeto ou DataFrame.
        """
        from .issues import IssuesModule
        issues_module = IssuesModule(
            self._http_client,
            self._org_id,
            self._pagination_config,
            self._threading_config
        )
        issues = list(issues_module.list_by_project(project_id))
        actions = []
        for issue in issues:
            actions_issue = self.list_by_issue(
                issue_id=issue["id"],
                include=include,
                filters=filters
            )
            if isinstance(actions_issue, list):
                actions.extend(actions_issue)
        
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
        """Obtém uma action específica por ID.
        
        Args:
            action_id: ID da action.
            include: Relacionamentos para incluir.
            return_pandas: Se True, retorna um DataFrame; se False, retorna um dict.
            
        Returns:
            Dados da action ou DataFrame.
            
        Example:
            >>> action = client.actions.get(123)
            >>> print(action['data']['attributes']['title'])
        """
        endpoint = f"{self._org_endpoint}/{action_id}"
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
        """Obtém múltiplas actions em paralelo.
        
        Args:
            action_ids: Lista de IDs de actions.
            include: Relacionamentos para incluir.
            return_pandas: Se True, retorna um DataFrame; se False, retorna uma lista.
            
        Returns:
            Lista de dados de actions ou DataFrame.
        """
        def fetch_action(aid):
            response = self.get(aid, include)
            return response.get('data', response)
        
        actions = self._execute_parallel(
            fetch_action,
            action_ids,
            self._threading_config
        )
        
        if return_pandas:
            return to_dataframe(actions)
        return actions
    
    # ==================== CRIAÇÃO ====================
    
    def create(
        self,
        issue_id: int,
        title: str,
        description: Optional[str] = None,
        owner: Optional[str] = None,
        owner_user_uid: Optional[str] = None,
        due_date: Optional[str] = None,
        completed: Optional[bool] = None,
        completed_date: Optional[str] = None,
        position: Optional[int] = None,
        custom_attributes: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Cria uma nova action em uma issue.
        
        IMPORTANTE: Actions são criadas dentro de Issues.
        Endpoint: POST /orgs/{org_id}/issues/{issue_id}/actions
        
        Args:
            issue_id: ID da issue (obrigatório).
            title: Título da action (obrigatório, max 255 chars).
            description: Descrição detalhada da action (max 524288 chars).
            owner: Nome ou email do responsável (string).
            owner_user_uid: UID do usuário responsável (sobrescreve owner).
            due_date: Data limite (YYYY-MM-DD).
            completed: Se a action está completa (True/False).
            completed_date: Data de conclusão (YYYY-MM-DD).
            position: Ordem de exibição (1-2147483647).
            custom_attributes: Atributos customizados.
                Formato: [{"id": "42", "term": "Nome", "value": ["valor"]}]
            
        Returns:
            Dados da action criada.
            
        Example:
            >>> action = client.actions.create(
            ...     issue_id=999,
            ...     title="Implementar novo controle",
            ...     description="Descrição da ação de remediação",
            ...     owner="responsavel@empresa.com",
            ...     due_date="2024-12-31"
            ... )
            >>> 
            >>> # Ou usando owner_user_uid
            >>> action = client.actions.create(
            ...     issue_id=999,
            ...     title="Revisar documentação",
            ...     owner_user_uid="3NQ6XzAUxqJMnAQ7n4KF",
            ...     due_date="2024-06-30"
            ... )
        """
        attributes = {"title": title}
        
        optional_attrs = {
            "description": description,
            "owner": owner,
            "due_date": due_date,
            "completed": completed,
            "completed_date": completed_date,
            "position": position,
        }
        
        for key, value in optional_attrs.items():
            if value is not None:
                attributes[key] = value
        
        if custom_attributes:
            attributes["custom_attributes"] = custom_attributes
        
        payload = {
            "data": {
                "type": "actions",
                "attributes": attributes
            }
        }
        
        relationships = {}
        
        if owner_user_uid:
            relationships["owner_user"] = {
                "data": {"type": "users", "id": str(owner_user_uid)}
            }
        
        if relationships:
            payload["data"]["relationships"] = relationships
        
        return self._http_client.post(self._issue_endpoint(issue_id), payload)
    
    # ==================== ATUALIZAÇÃO ====================
    
    def update(
        self,
        action_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        owner: Optional[str] = None,
        owner_user_uid: Optional[str] = None,
        due_date: Optional[str] = None,
        completed: Optional[bool] = None,
        completed_date: Optional[str] = None,
        position: Optional[int] = None,
        custom_attributes: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Atualiza uma action existente.
        
        Endpoint: PATCH /orgs/{org_id}/actions/{action_id}
        
        Args:
            action_id: ID da action a atualizar.
            title: Novo título (max 255 chars).
            description: Nova descrição (max 524288 chars).
            owner: Nome ou email do responsável.
            owner_user_uid: UID do usuário responsável (sobrescreve owner).
            due_date: Data limite (YYYY-MM-DD).
            completed: Se a action está completa.
            completed_date: Data de conclusão (YYYY-MM-DD).
            position: Nova ordem de exibição (1-2147483647).
            custom_attributes: Atributos customizados.
            
        Returns:
            Dados da action atualizada.
            
        Example:
            >>> action = client.actions.update(
            ...     action_id=123,
            ...     completed=True,
            ...     completed_date="2024-06-15"
            ... )
        """
        attributes = {}
        
        optional_attrs = {
            "title": title,
            "description": description,
            "owner": owner,
            "due_date": due_date,
            "completed": completed,
            "completed_date": completed_date,
            "position": position,
        }
        
        for key, value in optional_attrs.items():
            if value is not None:
                attributes[key] = value
        
        if custom_attributes is not None:
            attributes["custom_attributes"] = custom_attributes
        
        payload = {
            "data": {
                "type": "actions",
                "id": str(action_id),
                "attributes": attributes
            }
        }
        
        if owner_user_uid:
            payload["data"]["relationships"] = {
                "owner_user": {
                    "data": {"type": "users", "id": str(owner_user_uid)}
                }
            }
        
        endpoint = f"{self._org_endpoint}/{action_id}"
        return self._http_client.patch(endpoint, payload)
    
    # ==================== EXCLUSÃO ====================
    
    def delete(self, action_id: int) -> Dict[str, Any]:
        """Exclui uma action.
        
        Args:
            action_id: ID da action a excluir.
            
        Returns:
            Resposta da API.
            
        Warning:
            Esta ação é irreversível.
            
        Example:
            >>> client.actions.delete(action_id=123)
        """
        endpoint = f"{self._org_endpoint}/{action_id}"
        return self._http_client.delete(endpoint)
