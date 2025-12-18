def FIFO(queue):
    return queue.pop(0)

def MRV(queue):
    """
    Choose the one(Xn) with the smallest domain.
    """
    smallest_index = 0
    smallest_domain_size = len(queue[0][0].get_domain())

    # Go through the queue and find the smallest domain
    for i in range(len(queue)):
        Xm, Xn = queue[i]

        domain_size = len(Xm.get_domain())

        if domain_size < smallest_domain_size:
            smallest_domain_size = domain_size
            smallest_index = i

    # Remove and return it from the queue
    return queue.pop(smallest_index)

def Priority_To_Finalized_Neighbors(queue):
    """
    This heuristic chooses the arcs with fixed values
    ,because a fixed value quickly removes the invalid options.
    """
    best_index = 0

    for i in range(1, len(queue)):
        Xm_best, Xn_best = queue[best_index]
        Xm_current, Xn_current = queue[i]

        # Prefer arcs where Xn is finalized
        if Xn_current.is_finalized() and not Xn_best.is_finalized():
            best_index = i

        # If both have same finalized status, use smaller domain (MRV)
        elif Xn_current.is_finalized() == Xn_best.is_finalized():
            if len(Xm_current.get_domain()) < len(Xm_best.get_domain()):
                best_index = i

    return queue.pop(best_index)
