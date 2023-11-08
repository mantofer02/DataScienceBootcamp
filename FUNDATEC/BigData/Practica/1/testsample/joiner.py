"""Toy join function to showcase spark functions."""

def join_dataframes(left, right, columns_left, columns_right):
    return left.join(right, left[ columns_left ] == right[ columns_right ] )
