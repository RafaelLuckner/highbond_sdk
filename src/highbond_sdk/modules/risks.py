"""
Módulo de Riscos para o HighBond SDK.
"""
from typing import Optional, Dict, Any, List, Generator

from ..http_client import HighBondHTTPClient, PaginationMixin, ThreadingMixin
from ..config import PaginationConfig, ThreadingConfig


class RisksModule(PaginationMixin, ThreadingMixin):
    """Módulo para gerenciamento de Riscos no HighBond.
    
    Riscos representam ameaças potenciais aos objetivos da organização.
    Podem ser vinculados a projetos, objetivos e controles.
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
        """Endpoint base para riscos a nível de organização."""
        return f"/orgs/{self._org_id}/risks"
    
    def _project_endpoint(self, project_id: int) -> str:
        """Endpoint base para riscos de um projeto."""
        return f"/orgs/{self._org_id}/projects/{project_id}/risks"
    
    def _objective_endpoint(self, project_id: int, objective_id: int) -> str:
        """Endpoint base para riscos de um objetivo."""
        return (
            f"/orgs/{self._org_id}/projects/{project_id}"
            f"/objectives/{objective_id}/risks"
        )
    
    # ==================== LISTAGEM ====================
    
    def list(
        self,
        page: int = 1,
        page_size: int = 50,
        include: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Lista todos os riscos da organização com paginação manual.
        
        Args:
            page: Número da página (1-based).
            page_size: Itens por página (máximo 100).
            include: Relacionamentos para incluir (ex: ['controls', 'owner']).
            filters: Filtros adicionais.
            
        Returns:
            Resposta completa da API com data, meta e links.
            
        Example:
            >>> response = client.risks.list(page=1, page_size=25)
            >>> for risk in response['data']:
            ...     print(risk['attributes']['title'])
        """
        params = {
            "page[number]": self._encode_page_number(page),
            "page[size]": min(page_size, 100)
        }
        
        if include:
            params["include"] = ",".join(include)
        
        if filters:
            for key, value in filters.items():
                params[f"filter[{key}]"] = value
        
        return self._http_client.get(self._org_endpoint, params)
    
    def list_all(
        self,
        include: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None,
        max_pages: Optional[int] = None
    ) -> Generator[Dict[str, Any], None, None]:
        """Lista todos os riscos da organização com paginação automática.
        
        Args:
            include: Relacionamentos para incluir.
            filters: Filtros adicionais.
            max_pages: Máximo de páginas a buscar.
            
        Yields:
            Cada risco individualmente.
            
        Example:
            >>> for risk in client.risks.list_all():
            ...     print(risk['attributes']['title'])
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
        
        yield from self._paginate(self._org_endpoint, pagination, params)
    
    def list_by_project(
        self,
        project_id: int,
        page: int = 1,
        page_size: int = 50,
        include: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Lista riscos de um projeto específico.
        
        Args:
            project_id: ID do projeto.
            page: Número da página.
            page_size: Itens por página.
            include: Relacionamentos para incluir.
            filters: Filtros adicionais.
            
        Returns:
            Resposta completa da API.
            
        Example:
            >>> response = client.risks.list_by_project(123)
            >>> print(f"Total de riscos: {len(response['data'])}")
        """
        params = {
            "page[number]": self._encode_page_number(page),
            "page[size]": min(page_size, 100)
        }
        
        if include:
            params["include"] = ",".join(include)
        
        if filters:
            for key, value in filters.items():
                params[f"filter[{key}]"] = value
        
        return self._http_client.get(self._project_endpoint(project_id), params)
    
    def list_all_by_project(
        self,
        project_id: int,
        include: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None,
        max_pages: Optional[int] = None
    ) -> Generator[Dict[str, Any], None, None]:
        """Lista todos os riscos de um projeto com paginação automática.
        
        Args:
            project_id: ID do projeto.
            include: Relacionamentos para incluir.
            filters: Filtros adicionais.
            max_pages: Máximo de páginas.
            
        Yields:
            Cada risco individualmente.
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
        
        yield from self._paginate(
            self._project_endpoint(project_id), pagination, params
        )
    
    def list_by_objective(
        self,
        project_id: int,
        objective_id: int,
        page: int = 1,
        page_size: int = 50,
        include: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Lista riscos de um objetivo específico.
        
        Args:
            project_id: ID do projeto.
            objective_id: ID do objetivo.
            page: Número da página.
            page_size: Itens por página.
            include: Relacionamentos para incluir.
            
        Returns:
            Resposta completa da API.
        """
        params = {
            "page[number]": self._encode_page_number(page),
            "page[size]": min(page_size, 100)
        }
        
        if include:
            params["include"] = ",".join(include)
        
        endpoint = self._objective_endpoint(project_id, objective_id)
        return self._http_client.get(endpoint, params)
    
    # ==================== OBTENÇÃO ====================
    
    def get(
        self,
        risk_id: int,
        include: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Obtém um risco específico por ID.
        
        Args:
            risk_id: ID do risco.
            include: Relacionamentos para incluir.
            
        Returns:
            Dados do risco.
            
        Example:
            >>> risk = client.risks.get(456)
            >>> print(risk['data']['attributes']['title'])
        """
        endpoint = f"{self._org_endpoint}/{risk_id}"
        params = {}
        
        if include:
            params["include"] = ",".join(include)
        
        return self._http_client.get(endpoint, params if params else None)
    
    def get_many(
        self,
        risk_ids: List[int],
        include: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Obtém múltiplos riscos em paralelo.
        
        Args:
            risk_ids: Lista de IDs de riscos.
            include: Relacionamentos para incluir.
            
        Returns:
            Lista de dados de riscos.
        """
        def fetch_risk(rid):
            return self.get(rid, include)
        
        return self._execute_parallel(
            fetch_risk,
            risk_ids,
            self._threading_config
        )
    
    # ==================== CRIAÇÃO ====================
    
    def create(
        self,
        objective_id: int,
        description: str,
        title: Optional[str] = None,
        risk_id: Optional[str] = None,
        owner: Optional[str] = None,
        impact: Optional[str] = None,
        likelihood: Optional[str] = None,
        position: Optional[int] = None,
        custom_attributes: Optional[List[Dict[str, Any]]] = None,
        custom_factors: Optional[List[Dict[str, Any]]] = None,
        owner_user_uid: Optional[str] = None,
        framework_origin_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Cria um novo risco em um objetivo.
        
        IMPORTANTE: Riscos são criados dentro de Objectives, não diretamente em Projects.
        Endpoint: POST /orgs/{org_id}/objectives/{objective_id}/risks
        
        Args:
            objective_id: ID do objetivo (obrigatório).
            description: Descrição detalhada do risco (obrigatório, max 524288 chars).
            title: Título do risco (opcional, max 255 chars).
            risk_id: Código de referência do risco (max 255 chars).
            owner: Nome ou email do responsável (string, não envia notificação).
            impact: Classificação de impacto (ex: "High", "Medium", "Low" - depende da config do project type).
            likelihood: Probabilidade (ex: "High", "Medium", "Low" - depende da config do project type).
            position: Ordem de exibição (1-2147483647).
            custom_attributes: Lista de atributos customizados.
                Formato: [{"id": "42", "term": "Nome", "value": ["valor"]}]
            custom_factors: Lista de fatores de risco customizados.
                Formato: [{"id": "42", "term": "Fator", "value": ["valor"]}]
            owner_user_uid: UID do usuário responsável (sobrescreve owner, envia notificação).
            framework_origin_id: ID do risco equivalente em um framework associado.
            
        Returns:
            Dados do risco criado.
            
        Example:
            >>> risk = client.risks.create(
            ...     objective_id=456,
            ...     description="Descrição detalhada do risco de compliance",
            ...     title="Risco de Compliance",
            ...     impact="High",
            ...     likelihood="Medium",
            ...     owner="thomas@sodor.ca"
            ... )
        """
        attributes = {"description": description}
        
        optional_attrs = {
            "title": title,
            "risk_id": risk_id,
            "owner": owner,
            "impact": impact,
            "likelihood": likelihood,
            "position": position,
        }
        
        for key, value in optional_attrs.items():
            if value is not None:
                attributes[key] = value
        
        if custom_attributes:
            attributes["custom_attributes"] = custom_attributes
        
        if custom_factors:
            attributes["custom_factors"] = custom_factors
        
        payload = {
            "data": {
                "type": "risks",
                "attributes": attributes
            }
        }
        
        relationships = {}
        
        if owner_user_uid:
            relationships["owner_user"] = {
                "data": {"type": "users", "id": str(owner_user_uid)}
            }
        
        if framework_origin_id:
            relationships["framework_origin"] = {
                "data": {"type": "risks", "id": str(framework_origin_id)}
            }
        
        if relationships:
            payload["data"]["relationships"] = relationships
        
        endpoint = f"/orgs/{self._org_id}/objectives/{objective_id}/risks"
        return self._http_client.post(endpoint, payload)
    
    # ==================== ATUALIZAÇÃO ====================
    
    def update(
        self,
        risk_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        risk_id_ref: Optional[str] = None,
        owner: Optional[str] = None,
        impact: Optional[str] = None,
        likelihood: Optional[str] = None,
        position: Optional[int] = None,
        custom_attributes: Optional[List[Dict[str, Any]]] = None,
        custom_factors: Optional[List[Dict[str, Any]]] = None,
        owner_user_uid: Optional[str] = None
    ) -> Dict[str, Any]:
        """Atualiza um risco existente.
        
        Endpoint: PATCH /orgs/{org_id}/risks/{risk_id}
        
        Args:
            risk_id: ID do risco a atualizar.
            title: Novo título (max 255 chars).
            description: Nova descrição (max 524288 chars).
            risk_id_ref: Novo código de referência (campo risk_id na API).
            owner: Nome ou email do responsável.
            impact: Classificação de impacto (ex: "High", "Medium", "Low").
            likelihood: Probabilidade (ex: "High", "Medium", "Low").
            position: Nova ordem de exibição (1-2147483647).
            custom_attributes: Atributos customizados.
            custom_factors: Fatores de risco customizados.
            owner_user_uid: UID do usuário responsável (sobrescreve owner).
            
        Returns:
            Dados do risco atualizado.
            
        Example:
            >>> risk = client.risks.update(
            ...     risk_id=456,
            ...     title="Novo título do risco",
            ...     impact="Low"
            ... )
        """
        attributes = {}
        
        optional_attrs = {
            "title": title,
            "description": description,
            "risk_id": risk_id_ref,
            "owner": owner,
            "impact": impact,
            "likelihood": likelihood,
            "position": position,
        }
        
        for key, value in optional_attrs.items():
            if value is not None:
                attributes[key] = value
        
        if custom_attributes is not None:
            attributes["custom_attributes"] = custom_attributes
        
        if custom_factors is not None:
            attributes["custom_factors"] = custom_factors
        
        payload = {
            "data": {
                "type": "risks",
                "id": str(risk_id),
                "attributes": attributes
            }
        }
        
        if owner_user_uid:
            payload["data"]["relationships"] = {
                "owner_user": {
                    "data": {"type": "users", "id": str(owner_user_uid)}
                }
            }
        
        endpoint = f"{self._org_endpoint}/{risk_id}"
        return self._http_client.patch(endpoint, payload)
    
    # ==================== EXCLUSÃO ====================
    
    def delete(self, risk_id: int) -> Dict[str, Any]:
        """Exclui um risco.
        
        Args:
            risk_id: ID do risco a excluir.
            
        Returns:
            Resposta da API.
            
        Warning:
            Esta ação é irreversível.
        """
        endpoint = f"{self._org_endpoint}/{risk_id}"
        return self._http_client.delete(endpoint)
    
    def delete_many(self, risk_ids: List[int]) -> List[Dict[str, Any]]:
        """Exclui múltiplos riscos em paralelo.
        
        Args:
            risk_ids: Lista de IDs de riscos a excluir.
            
        Returns:
            Lista de respostas da API.
        """
        return self._execute_parallel(
            self.delete,
            risk_ids,
            self._threading_config
        )
    
    # ==================== RELACIONAMENTOS ====================
    
    def link_control(
        self,
        risk_id: int,
        control_id: int
    ) -> Dict[str, Any]:
        """Vincula um controle a um risco.
        
        Args:
            risk_id: ID do risco.
            control_id: ID do controle a vincular.
            
        Returns:
            Resposta da API.
        """
        endpoint = f"{self._org_endpoint}/{risk_id}/relationships/controls"
        payload = {
            "data": [
                {"type": "controls", "id": str(control_id)}
            ]
        }
        return self._http_client.post(endpoint, payload)
    
    def unlink_control(
        self,
        risk_id: int,
        control_id: int
    ) -> Dict[str, Any]:
        """Remove vínculo entre risco e controle.
        
        Args:
            risk_id: ID do risco.
            control_id: ID do controle a desvincular.
            
        Returns:
            Resposta da API.
        """
        endpoint = (
            f"{self._org_endpoint}/{risk_id}"
            f"/relationships/controls/{control_id}"
        )
        return self._http_client.delete(endpoint)
    
    def get_controls(
        self,
        risk_id: int,
        include: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Obtém controles vinculados a um risco.
        
        Args:
            risk_id: ID do risco.
            include: Relacionamentos para incluir.
            
        Returns:
            Lista de controles vinculados.
        """
        endpoint = f"{self._org_endpoint}/{risk_id}/controls"
        params = {}
        
        if include:
            params["include"] = ",".join(include)
        
        return self._http_client.get(endpoint, params if params else None)
