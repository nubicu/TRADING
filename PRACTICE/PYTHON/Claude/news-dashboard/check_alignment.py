import ast
with open('news.py') as f:
    content = f.read()
tree = ast.parse(content)
fetcher_keys = set()
category_keys = set()
for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == 'ALL_FETCHERS':
                for k in node.value.keys:
                    if isinstance(k, ast.Constant):
                        fetcher_keys.add(k.value)
            if isinstance(node.value, ast.Dict) and isinstance(target, ast.Name) and target.id == 'CATEGORIES':
                for v in node.value.values:
                    if isinstance(v, ast.List):
                        for el in v.elts:
                            if isinstance(el, ast.Constant):
                                category_keys.add(el.value)
missing = category_keys - fetcher_keys
if missing:
    print(f'Missing from ALL_FETCHERS: {sorted(missing)}')
else:
    print('✅ Perfect alignment')