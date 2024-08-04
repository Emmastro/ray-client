import ray

# Initialize Ray
# ray.init(address='http://ec2-52-22-46-66.compute-1.amazonaws.com:8265')
ray.init()

@ray.remote
def fib(n):
    if n < 2:
        return n
    else:
        return ray.get(fib.remote(n - 1)) + ray.get(fib.remote(n - 2))

@ray.remote
def fib1(n):
    if n < 2:
        return n
    else:
        return ray.get(fib.remote(n - 1)) + ray.get(fib.remote(n - 2))


# Run the task
if __name__ == "__main__":
    futures = [fib.remote(5), fib.remote(10), fib1.remote(30)]
    results = ray.get(futures)
    print(results)
