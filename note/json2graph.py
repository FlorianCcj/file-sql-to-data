```
  recupere un json pour le decomposer en nodes et edge pour l afficher avec lynkurious
```
function getGraphFromJson(json):
  nodes = []
  edge = []
  init node1
  for key in json:
    if type(json[key]) === !object
      node1.data.key = json.key
    if type(json.key) === object:
      init node2
      init edge1 node1 -> node2
      edges.push(edge1)
      {nodesTmp, edgeTmp} = getGraphFromJson(object.key)
      nodes = [...nodes, ...nodeTmp]
      edges = [...edges, edgesTmp]
  nodes.push(node1)
  return {nodes, edges}

prout = getGraphFromJson(json)