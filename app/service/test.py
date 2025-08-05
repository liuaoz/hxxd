import time


class Snowflake:
    def __init__(self, machine_id):
        self.machine_id = machine_id
        self.sequence = 0
        self.last_timestamp = 0

    def generate_id(self):
        timestamp = int(time.time() * 1000)
        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & 0xFFF  # 12位序列号
            if self.sequence == 0:
                timestamp = self.wait_next_millis()
        else:
            self.sequence = 0
        self.last_timestamp = timestamp
        return ((timestamp << 22) | (self.machine_id << 12) | self.sequence)

    def wait_next_millis(self):
        timestamp = int(time.time() * 1000)
        while timestamp <= self.last_timestamp:
            timestamp = int(time.time() * 1000)
        return timestamp


snowflake = Snowflake(machine_id=2)
print(snowflake.generate_id())  # 示例：1904060881234567890
