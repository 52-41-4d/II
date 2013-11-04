def rank_items(user_id) {
    m = [:]
    g.v(user_id).out('likes').in('likes').out('likes').groupCount(m)
    m.sort{a,b -> a.value <=> b.value}
    return m.values()
}
