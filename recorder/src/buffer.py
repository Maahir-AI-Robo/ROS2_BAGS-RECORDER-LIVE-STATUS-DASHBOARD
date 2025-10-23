class MessageBuffer:
    def __init__(self):
        self.buffer = {}
    
    def add_message(self, topic, message):
        if topic not in self.buffer:
            self.buffer[topic] = []
        self.buffer[topic].append(message)

    def get_aligned_batch(self, topic, batch_size):
        if topic in self.buffer:
            return self.buffer[topic][:batch_size]
        return []

    def get_occupancy(self, topic):
        return len(self.buffer.get(topic, []))

    def get_global_occupancy(self):
        return sum(len(messages) for messages in self.buffer.values())

    def clear_topic(self, topic):
        if topic in self.buffer:
            del self.buffer[topic]