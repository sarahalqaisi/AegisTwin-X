from __future__ import annotations

import networkx as nx

from .models import GraphPayload, SecurityPromise


NODE_COLORS = {
    "role": "#7c5cff",
    "endpoint": "#36c5f0",
    "resource": "#26d07c",
    "risk": "#ff5c70",
}


def build_security_graph(promises: list[SecurityPromise], vulnerable: bool) -> GraphPayload:
    graph = nx.DiGraph()
    for promise in promises:
        role = f"role:{promise.subject_role}"
        endpoint = f"endpoint:{promise.endpoint}"
        resource = f"resource:{promise.resource}"
        graph.add_node(role, label=promise.subject_role.title(), kind="role")
        graph.add_node(endpoint, label=promise.endpoint, kind="endpoint")
        graph.add_node(resource, label=promise.resource.title(), kind="resource")
        graph.add_edge(role, endpoint, label=promise.action, protected=True)
        graph.add_edge(endpoint, resource, label="accesses", protected=True)

    if vulnerable:
        risk = "risk:cross-account-access"
        graph.add_node(risk, label="Cross-account access", kind="risk")
        graph.add_edge("role:customer", risk, label="new path", protected=False)
        graph.add_edge(risk, "resource:invoice", label="exposes", protected=False)

    nodes = [
        {"id": node, **attrs, "color": NODE_COLORS[attrs["kind"]]}
        for node, attrs in graph.nodes(data=True)
    ]
    edges = [
        {"source": source, "target": target, **attrs}
        for source, target, attrs in graph.edges(data=True)
    ]
    return GraphPayload(nodes=nodes, edges=edges)

