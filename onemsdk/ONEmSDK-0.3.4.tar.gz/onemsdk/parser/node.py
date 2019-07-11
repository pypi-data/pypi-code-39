from __future__ import annotations

from typing import Dict, List, Union

from pydantic import BaseModel


class Node(BaseModel):
    tag: str
    attrs: Dict[str, str] = {}
    children: List[Union[Node, str]] = []

    def add_child(self, child: Union[Node, str]):
        self.children.append(child)


Node.update_forward_refs()
