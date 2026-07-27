from textnode import TextNode, TextType

def main():
    node = TextNode('anchor text', TextType.LINK, 'https://google.com')
    print(node)

if __name__ == "__main__":
    main()