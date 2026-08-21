def make_huffman_code(probabilities):
    probs = tuple(float(p) for p in probabilities)

    if len(probs) == 0:
        return tuple()

    if any(p < 0 for p in probs):
        raise ValueError("Probabilities must be nonnegative.")

    if sum(probs) <= 0:
        raise ValueError("At least one probability must be positive.")

    nodes = [(p, i, i) for i, p in enumerate(probs)]

    def build_tree(nodes):
        if len(nodes) == 1:
            return nodes[0][2]

        nodes = sorted(nodes, key=lambda x: (x[0], x[1]))

        w1, k1, t1 = nodes[0]
        w2, k2, t2 = nodes[1]

        merged = (w1 + w2, min(k1, k2), (t1, t2))

        return build_tree(nodes[2:] + [merged])

    tree = build_tree(nodes)
    codes = [None] * len(probs)

    def assign_code(tree, prefix):
        if isinstance(tree, int):
            codes[tree] = tuple(prefix)
            return

        left, right = tree
        assign_code(left, prefix + [0])
        assign_code(right, prefix + [1])

    assign_code(tree, [])

    if len(probs) == 1:
        codes[0] = (0,)

    return tuple(codes)


p = (0.3, 0.2, 0.4, 0.05, 0.05)
print(make_huffman_code(p))