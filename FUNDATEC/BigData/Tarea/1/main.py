from functions import init_spark


def main():
    spark, sc = init_spark()
    nums = sc.parallelize([1, 2, 3, 4])
    print(nums.map(lambda x: x * x).collect())


if __name__ == "__main__":
    main()
