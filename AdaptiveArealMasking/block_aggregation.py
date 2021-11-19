from shapely.geometry import Polygon, Point


def block_aggregation(blocks, k_anonymity):
    aggregated_blocks = [[]]
    current_blocks = [[]]
    for i in range(1, len(blocks)):
        current_blocks.append([blocks[i][0], blocks[i][1]])

    aggregation = True
    while aggregation:
        # get the block with the smallest count of addresses
        smallest_block_id = get_smallest_block(current_blocks)
        # check if the smallest block is small enough to continue aggregation
        block_disclosure = current_blocks[smallest_block_id][1]
        if int(block_disclosure) > k_anonymity:
            aggregation = False
            break
        # get the surrounding blocks
        surrounding_blocks = get_surrounding_blocks(current_blocks, smallest_block_id)
        # get the smallest from the surrounding blocks
        smallest_surrounding_id = get_smallest_block(surrounding_blocks)
        # aggregate both blocks
        polygon1 = current_blocks[smallest_block_id][0]
        polygon2 = current_blocks[smallest_surrounding_id][0]
        polygon = polygon1.union(polygon2)
        # update the lists
        address_count = block_disclosure + current_blocks[smallest_surrounding_id][1]
        updated_blocks = [[]]
        for i in range(1, len(current_blocks)):
            if (i != smallest_block_id) and (i != smallest_surrounding_id):
                updated_blocks.append([current_blocks[i][0], current_blocks[i][1]])
        updated_blocks.append([polygon, address_count])
        current_blocks = updated_blocks

    for i in range(1, len(current_blocks)):
        aggregated_blocks.append([current_blocks[i][0],current_blocks[i][1]])

    return aggregated_blocks


def get_smallest_block(blocks):
    # this function gets id in the list of the block with the smallest count of addresses
    minimum = 100000
    smallest = 0
    for i in range(1, len(blocks)):
        count = blocks[i][1]
        if int(count) <= minimum:
            minimum = int(count)
            smallest = i

    return smallest


def get_surrounding_blocks(blocks, block_id):
    # for one block in a list of blocks, get the ones that touch that block
    surrounding_blocks = [[]]
    polygon = blocks[block_id][0]
    j = 0
    for i in range(1, len(blocks)):
        if i == block_id:
            continue
        polygon_i = blocks[i][0]
        if polygon.touches(polygon_i):
            j = j + 1
            surrounding_blocks.append([polygon_i, blocks[i][1]])

    return surrounding_blocks
