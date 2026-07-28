

class HTMLNode():
    def __init__(self, tag: str | None = None, \
                 value: str | None = None, \
                 children: list[HTMLNode] | None = None, \
                 props: dict | None = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        ret: str = ""
        if self.props is not None:
            for k in self.props:
                ret += f" {k}=\"{self.props.get(k)}\""
        return ret

    def __repr__(self):
        return f"HTMLNode(Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, \
                 value: str | None, \
                 props: dict | None = None) -> None:
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(Tag: {self.tag}, Value: {self.value}, Props: {self.props})"