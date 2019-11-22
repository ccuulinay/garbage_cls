import networkx as nx
import logging


def parse_path_list_into_uvd(ops_ls):
    uvd_list = []
    for item in ops_ls:
        if len(item) == 0:
            pass
        elif len(item) == 1:
            pass
        else:
            if item[-1] == "SMLP":
                item = item[:-1]
                v, u = item[-2], item[-1]
                name = "is_sample_of"
                uvd_list.append([u, v, name, "valid", "->".join([u, name, v])])
            for parent, child in zip(item, item[1:]):
                name = "set_relation"
                uvd_list.append([child, parent, name, "子类", "->".join([child, name, parent])])
                uvd_list.append([parent, child, name, "父类", "->".join([parent, name, child])])
    return uvd_list


def build_garbage_MDG(ops_df):
    """
    Using different edges presenting relationship.


    nx.from_pandas_edgelist(..) is first add edge with (source, target) along with default key,
    and using the return key as key to update edge's attribute which will ignre my "key" in edge_attr.

    g = nx.from_pandas_edgelist(
        ops_df, "source", "target", edge_attr=["name", "value", "key"]
        , create_using=nx.MultiDiGraph()

    So I would iterate through using g.add_edge.
    """
    g = nx.MultiDiGraph()
    for item in ops_df.itertuples():
        s = getattr(item, "source")
        t = getattr(item, "target")
        n = getattr(item, "name")
        v = getattr(item, "value")
        k = getattr(item, "key")
        g.add_edge(s, t, name=n, value=v, key=k)

    return g


def build_garbage_DG(ops_ls):
    """
    Using edge attributes to present a relationship
    """
    garbage_graph = nx.DiGraph()
    for item in ops_ls:
        if len(item) == 0:
            pass
        elif len(item) == 1:
            garbage_graph.add_node(item[0])
        else:
            if item[-1] == "SMLP":
                item = item[:-1]
                sc, sample = item[-2], item[-1]
                garbage_graph.add_edge(sample, sc, is_sample="Y")
            for parent, child in zip(item, item[1:]):
                garbage_graph.add_edge(child, parent, set_relation="子类")
                garbage_graph.add_edge(parent, child, set_relation="父类")
    return garbage_graph


def get_in_edges_from_dg(ops_g, watch_node_name, watch_edge_attr, watch_edge_attr_val):
    target_node_names = [
        n[0] for n in ops_g.in_edges(watch_node_name, data=watch_edge_attr) if n[-1] == watch_edge_attr_val
    ]
    return target_node_names


def get_out_edges_from_dg(ops_g, watch_node_name, watch_edge_attr, watch_edge_attr_val):
    target_node_names = [
        n[1] for n in ops_g.out_edges(watch_node_name, data=watch_edge_attr) if n[-1] == watch_edge_attr_val
    ]
    return target_node_names


def get_in_edges_from_mdg(ops_g, watch_node_name, watch_edge_name, watch_edge_val, **kwargs):
    """
    Sample usage:

    ops_g = gz_garbage_graph
    watch_node_name = "骨头贝壳"
    watch_edge_attr = "set_relation"
    watch_edge_attr_val = "子类"
    print(get_in_edges_from_dg(ops_g, watch_node_name, watch_edge_attr, watch_edge_attr_val))

    """
    if ops_g.is_multigraph() & ops_g.is_directed():
        target_node_names = [
            n[0] for n in ops_g.in_edges(watch_node_name, data=True) if
            (n[-1].get("name") == watch_edge_name) and (n[-1].get("value") == watch_edge_val)
        ]
        return target_node_names
    else:
        raise Exception("Input graph is either not a directed graph nor multi graph.")


def get_out_edges_from_mdg(ops_g, watch_node_name, watch_edge_name, watch_edge_val, **kwargs):
    if ops_g.is_multigraph() & ops_g.is_directed():
        target_node_names = [
            n[1] for n in ops_g.out_edges(watch_node_name, data=True) if
            (n[-1].get("name") == watch_edge_name) and (n[-1].get("value") == watch_edge_val)
        ]
        return target_node_names
    else:
        raise Exception("Input graph is either not a directed graph nor multi graph.")


def get_root_domain(ops_g, node_name):
    # Check if given node_name is in the grahp
    if ops_g.has_node(node_name):
        pass
    else:
        logging.error("{} is not in graph.".format(node_name))
        return
        # Check if given node_name is root domain:
    node_attr = ops_g.nodes[node_name]
    if "is_root_domain" in node_attr.keys():
        if node_attr['is_root_domain']:
            return node_name

    # Get out edges
    else:
        parent_node = get_out_edges_from_mdg(
            ops_g, node_name, "set_relation", "子类"
        )[0]
        return get_root_domain(ops_g, parent_node)

