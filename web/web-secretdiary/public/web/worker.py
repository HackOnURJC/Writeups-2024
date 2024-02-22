from redis import Redis
from rq import Worker, Queue

if __name__ == '__main__':
    conn = Redis(host="redis")
    worker = Worker(Queue(connection=conn), connection=conn)
    worker.work()
