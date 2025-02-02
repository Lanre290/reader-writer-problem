import threading
import time
import random

# Semaphore to control writer access (ensures only one writer at a time)
writer_semaphore = threading.Semaphore(1)

# Mutex (lock) to manage the reader count safely
reader_mutex = threading.Lock()

# Shared resource (simulated database or file) and the count of active readers
shared_data = "Initial Data"
reader_count = 0

def reader(reader_id):
    """
    Function executed by reader threads. Each reader attempts to read the shared data.
    """
    global reader_count
    
    while True:
        time.sleep(random.randint(1, 3))  # Simulate random reading intervals
        
        # Entry section: Safely update the reader count
        reader_mutex.acquire()
        reader_count += 1
        if reader_count == 1:
            writer_semaphore.acquire()  # First reader locks the writer out
        reader_mutex.release()
        
        # Critical section: Reading the shared resource
        print(f"Reader {reader_id} is reading: {shared_data}")
        time.sleep(random.uniform(0.5, 2))  # Simulate time spent reading
        
        # Exit section: Safely update the reader count
        reader_mutex.acquire()
        reader_count -= 1
        if reader_count == 0:
            writer_semaphore.release()  # Last reader unlocks the writer
        reader_mutex.release()

def writer(writer_id):
    """
    Function executed by writer threads. Each writer updates the shared data exclusively.
    """
    global shared_data
    
    while True:
        time.sleep(random.randint(2, 5))  # Simulate random writing intervals
        
        # Entry section: Gain exclusive access to write
        writer_semaphore.acquire()
        
        # Critical section: Updating the shared resource
        shared_data = f"Updated by Writer {writer_id}"
        print(f"Writer {writer_id} has started writing: {shared_data}")
        time.sleep(random.uniform(1, 3))  # Simulate writing time
        
        # Exit section: Release the lock for other writers/readers
        print(f"Writer {writer_id} has finished writing.")
        writer_semaphore.release()

# Number of reader and writer threads to create
num_readers = 3
num_writers = 2

# Creating reader and writer threads
reader_threads = [threading.Thread(target=reader, args=(i,)) for i in range(num_readers)]
writer_threads = [threading.Thread(target=writer, args=(i,)) for i in range(num_writers)]

# Starting all threads
for t in reader_threads + writer_threads:
    t.start()

# Joining all threads (optional, since they run indefinitely)
for t in reader_threads + writer_threads:
    t.join()
